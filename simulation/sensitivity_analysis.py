#!/usr/bin/env python3
"""
AIRM Sensitivity Simulations — sensitivity_analysis.py
-----------------------------------------------------
Spinner-enabled sensitivity study + null baseline + falsification check.

What this script does (and does NOT do):
- Simulates a torsion pendulum with an externally prescribed fractional inertia modulation:
    I(t) = I0 * (1 + epsilon(t)),  epsilon(t) = alpha * cos(2*pi*f_target*t + phi)
- Adds measurement noise using a one-sided ASD convention (rad/sqrt(Hz))
- Runs IQ demod at f0 -> phase unwrap -> dphi/dt -> delta_f(t)
- Estimates recovered modulation amplitude via coherent projection at f_target
- Sweeps alpha and computes SNR vs null distribution
- Writes run outputs to simulation/runs/<RUN_ID>/

No claims of new physics. This is a sensitivity + validation tool only.
"""

from __future__ import annotations

import os
import json
import math
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Tuple, Dict, List

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import butter, filtfilt

# Optional plotting (script still works without it)
try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False


# ----------------------------- Config -----------------------------

@dataclass
class SimConfig:
    # Hardware parameters
    I0: float = 1.0e-3          # kg*m^2
    kappa: float = 1.0e-4       # N*m/rad
    Q: float = 1.0e5            # dimensionless (sets damping)

    # Modulation parameters
    f_spin: float = 1.0 / 1000.0
    f_sid: float = 1.0 / (23.9345 * 3600.0)
    phi: float = 0.0
    delta_false_frac: float = 0.02  # 2% wrong-frequency test

    # Simulation / sampling
    duration_s: float = 48.0 * 3600.0
    fs_hz: float = 2.0
    theta0_rad: float = 1.0e-6
    theta_dot0: float = 0.0

    # Noise model (one-sided ASD convention)
    noise_asd_rad_sqrt_hz: float = 1.0e-8  # rad/sqrt(Hz)

    # Analysis
    lp_cutoff_hz: float = 0.01
    lp_order: int = 6
    trim_s: float = 600.0  # trim edges / startup transient

    # Monte Carlo
    n_realizations: int = 10

    # Alpha sweep
    alpha_min: float = 1.0e-14
    alpha_max: float = 1.0e-10
    alpha_points: int = 13  # logspace points

    # Run metadata
    run_tag: str = "sim"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


# -------------------------- Derived params --------------------------

def derived_params(cfg: SimConfig) -> Dict[str, float]:
    gamma = cfg.kappa / cfg.Q  # N*m*s/rad  (since Q = kappa / gamma)
    f0 = math.sqrt(cfg.kappa / cfg.I0) / (2.0 * math.pi)
    f_target = cfg.f_spin + cfg.f_sid
    f_false = f_target * (1.0 + cfg.delta_false_frac)
    dt = 1.0 / cfg.fs_hz

    # One-sided ASD [rad/sqrt(Hz)] -> discrete per-sample RMS:
    # sigma = ASD * sqrt(fs/2)
    noise_rms = cfg.noise_asd_rad_sqrt_hz * math.sqrt(cfg.fs_hz / 2.0)

    # Sampling sanity: keep well above Nyquist with margin
    min_fs = max(4.0 * f0, 1.0)
    if cfg.fs_hz < min_fs:
        raise ValueError(
            f"fs_hz={cfg.fs_hz} too low for f0≈{f0:.6f} Hz. "
            f"Use fs_hz >= {min_fs:.2f} Hz."
        )

    if 2.0 * cfg.trim_s >= cfg.duration_s:
        raise ValueError("trim_s too large relative to duration_s.")

    return {
        "gamma": gamma,
        "f0": f0,
        "f_target": f_target,
        "f_false": f_false,
        "dt": dt,
        "noise_rms_per_sample": noise_rms,
        "min_fs_recommended": min_fs,
    }


# ----------------------------- Model -----------------------------

def epsilon_total(t: float, alpha: float, f_target: float, phi: float) -> float:
    return alpha * math.cos(2.0 * math.pi * f_target * t + phi)

def airm_eom(t: float, y: np.ndarray, alpha: float, cfg: SimConfig, dp: Dict[str, float]) -> List[float]:
    theta, theta_dot = float(y[0]), float(y[1])
    eps = epsilon_total(t, alpha, dp["f_target"], cfg.phi)
    theta_ddot = (-dp["gamma"] * theta_dot - cfg.kappa * theta) / (cfg.I0 * (1.0 + eps))
    return [theta_dot, theta_ddot]

def run_theta(alpha: float, cfg: SimConfig, dp: Dict[str, float], t_eval: np.ndarray) -> np.ndarray:
    y0 = [cfg.theta0_rad, cfg.theta_dot0]
    sol = solve_ivp(
        lambda t, y: airm_eom(t, y, alpha, cfg, dp),
        [0.0, cfg.duration_s],
        y0,
        t_eval=t_eval,
        method="RK45",
        rtol=1e-9,
        atol=1e-12,
    )
    return sol.y[0]


# ----------------------------- Analysis -----------------------------

def matched_amp(x: np.ndarray, t: np.ndarray, f_ref: float) -> float:
    c = np.cos(2.0 * np.pi * f_ref * t)
    s = np.sin(2.0 * np.pi * f_ref * t)

    # Normalize templates to unit RMS so amplitude is comparable across durations
    c /= np.sqrt(np.mean(c * c))
    s /= np.sqrt(np.mean(s * s))

    a = float(np.mean(x * c))
    b = float(np.mean(x * s))
    return math.sqrt(a * a + b * b)

def process_one_realization(alpha: float, cfg: SimConfig, dp: Dict[str, float], rng: np.random.Generator) -> Tuple[float, float]:
    """
    Returns:
      amp_true  - recovered amplitude at f_target (Hz)
      amp_false - recovered amplitude at f_false  (Hz)
    """
    dt = dp["dt"]
    t_eval = np.arange(0.0, cfg.duration_s, dt)

    theta = run_theta(alpha, cfg, dp, t_eval)

    # Add measurement noise (discrete samples)
    theta_noisy = theta + dp["noise_rms_per_sample"] * rng.standard_normal(theta.shape)

    # IQ demod at f0
    cos_ref = np.cos(2.0 * np.pi * dp["f0"] * t_eval)
    sin_ref = np.sin(2.0 * np.pi * dp["f0"] * t_eval)
    I = theta_noisy * cos_ref
    Q = -theta_noisy * sin_ref

    # Low-pass filter to isolate baseband
    b, a = butter(cfg.lp_order, cfg.lp_cutoff_hz / (cfg.fs_hz / 2.0), btype="low")
    I_lp = filtfilt(b, a, I)
    Q_lp = filtfilt(b, a, Q)

    # Trim to avoid filtfilt edge artifacts + startup transient
    mask = (t_eval >= cfg.trim_s) & (t_eval <= (cfg.duration_s - cfg.trim_s))
    t = t_eval[mask]
    I_lp = I_lp[mask]
    Q_lp = Q_lp[mask]

    # Phase -> detrend -> delta_f
    phase = np.unwrap(np.arctan2(Q_lp, I_lp))
    slope, intercept = np.polyfit(t, phase, 1)
    phase_dt = phase - (slope * t + intercept)
    dphase_dt = np.gradient(phase_dt, dt)
    delta_f = dphase_dt / (2.0 * np.pi)

    amp_true = matched_amp(delta_f, t, dp["f_target"])
    amp_false = matched_amp(delta_f, t, dp["f_false"])
    return amp_true, amp_false


# ----------------------------- Main sweep -----------------------------

def run_sensitivity(cfg: SimConfig) -> Dict[str, object]:
    dp = derived_params(cfg)

    run_id = f"{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{cfg.run_tag}"
    base_dir = os.path.join(os.path.dirname(__file__), "runs", run_id)
    ensure_dir(base_dir)

    rng = np.random.default_rng(0)

    # Alpha grid
    alphas = np.logspace(np.log10(cfg.alpha_min), np.log10(cfg.alpha_max), cfg.alpha_points)

    # Null distribution (alpha=0)
    null_true = []
    null_false = []
    for _ in range(cfg.n_realizations):
        a_true, a_false = process_one_realization(0.0, cfg, dp, rng)
        null_true.append(a_true)
        null_false.append(a_false)

    null_true = np.array(null_true, dtype=float)
    null_mu = float(np.mean(null_true))
    null_sigma = float(np.std(null_true, ddof=1)) if len(null_true) > 1 else float(np.std(null_true))

    # Sweep
    rows = []
    for alpha in alphas:
        amps_true = []
        amps_false = []
        for _ in range(cfg.n_realizations):
            a_true, a_false = process_one_realization(float(alpha), cfg, dp, rng)
            amps_true.append(a_true)
            amps_false.append(a_false)

        amps_true = np.array(amps_true, dtype=float)
        amps_false = np.array(amps_false, dtype=float)

        mean_true = float(np.mean(amps_true))
        std_true = float(np.std(amps_true, ddof=1)) if len(amps_true) > 1 else float(np.std(amps_true))

        # SNR vs NULL (use null_sigma; guard zero)
        denom = null_sigma if null_sigma > 0 else (std_true if std_true > 0 else 1e-30)
        snr = (mean_true - null_mu) / denom

        # Falsification ratio (false/true) from means
        mean_false = float(np.mean(amps_false))
        ratio_false_true = mean_false / (mean_true + 1e-30)

        rows.append({
            "alpha": float(alpha),
            "mean_amp_true_hz": mean_true,
            "std_amp_true_hz": std_true,
            "mean_amp_false_hz": mean_false,
            "false_over_true": ratio_false_true,
            "snr_vs_null": float(snr),
        })

        print(
            f"alpha={alpha:.2e} | amp_true={mean_true:.3e} Hz | "
            f"SNR_vs_null={snr:.2f} | false/true={ratio_false_true:.3f}"
        )

    # Decide GO/NO-GO at target alpha (default: compare last point)
    go_snr_threshold = 10.0
    best = max(rows, key=lambda r: r["snr_vs_null"])
    go = bool(best["snr_vs_null"] >= go_snr_threshold)

    # Save outputs
    meta = {
        "run_id": run_id,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "config": asdict(cfg),
        "derived": dp,
        "null": {
            "null_mu_hz": null_mu,
            "null_sigma_hz": null_sigma,
            "n": int(cfg.n_realizations),
        },
        "decision": {
            "go_threshold_snr": go_snr_threshold,
            "best_alpha": best["alpha"],
            "best_snr_vs_null": best["snr_vs_null"],
            "go": go,
        },
    }

    with open(os.path.join(base_dir, "run_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    # CSV
    csv_path = os.path.join(base_dir, "alpha_sweep.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("alpha,mean_amp_true_hz,std_amp_true_hz,mean_amp_false_hz,false_over_true,snr_vs_null\n")
        for r in rows:
            f.write(
                f"{r['alpha']:.16e},{r['mean_amp_true_hz']:.16e},{r['std_amp_true_hz']:.16e},"
                f"{r['mean_amp_false_hz']:.16e},{r['false_over_true']:.16e},{r['snr_vs_null']:.16e}\n"
            )

    # Plot (optional)
    if HAS_MPL:
        al = np.array([r["alpha"] for r in rows], dtype=float)
        snr = np.array([r["snr_vs_null"] for r in rows], dtype=float)
        ftr = np.array([r["false_over_true"] for r in rows], dtype=float)

        plt.figure()
        plt.semilogx(al, snr)
        plt.axhline(go_snr_threshold, linestyle="--")
        plt.xlabel("alpha")
        plt.ylabel("SNR vs null")
        plt.title("AIRM Sensitivity Sweep")
        plt.grid(True, which="both")
        plt.tight_layout()
        plt.savefig(os.path.join(base_dir, "snr_sweep.png"), dpi=160)

        plt.figure()
        plt.semilogx(al, ftr)
        plt.axhline(0.1, linestyle="--")
        plt.xlabel("alpha")
        plt.ylabel("false/true ratio")
        plt.title("Falsification Check (Lower is better)")
        plt.grid(True, which="both")
        plt.tight_layout()
        plt.savefig(os.path.join(base_dir, "falsification_ratio.png"), dpi=160)

    # Final printout
    print("\n--- SUMMARY ---")
    print(f"run_id: {run_id}")
    print(f"f0={dp['f0']:.6f} Hz | fs={cfg.fs_hz:.3f} Hz | dt={dp['dt']:.3f} s")
    print(f"noise_asd={cfg.noise_asd_rad_sqrt_hz:.2e} rad/sqrt(Hz)")
    print(f"noise_rms_per_sample={dp['noise_rms_per_sample']:.2e} rad")
    print(f"null_mu={null_mu:.3e} Hz | null_sigma={null_sigma:.3e} Hz")
    print(f"BEST: alpha={best['alpha']:.2e} | SNR_vs_null={best['snr_vs_null']:.2f} | false/true={best['false_over_true']:.3f}")
    print("DECISION:", "GO" if go else "NO-GO")
    print(f"outputs: {base_dir}")

    return {"meta": meta, "rows": rows, "output_dir": base_dir}


if __name__ == "__main__":
    cfg = SimConfig()
    run_sensitivity(cfg)
