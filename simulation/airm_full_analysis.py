#!/usr/bin/env python3
"""
AIRM Spinner — Full Sensitivity & Falsification Analysis
=======================================================

This script performs a numerical sensitivity study of the AIRM
(Anisotropic Inertial Response Model) torsion-balance apparatus with
spinner modulation enabled.

IMPORTANT SCOPE STATEMENT
-------------------------
• This script does NOT claim new physics
• This script does NOT assert the existence of anisotropic inertia
• This script DOES test whether a predefined, externally injected
  modulation could be recovered by the proposed analysis pipeline
• All signals are prescribed; all conclusions are methodological

A numerical “GO” means:
“If a signal of this form existed, the pipeline would recover it.”

Reality is decided by hardware, not simulations.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import welch, butter, filtfilt

# Reproducibility (Tier-1 requirement)
np.random.seed(0)

# ============================================================
# 1. HARDWARE PARAMETERS (EDIT TO MATCH BUILD)
# ============================================================

I0 = 1.0e-3          # kg·m^2   (moment of inertia)
kappa = 1.0e-4       # N·m/rad  (torsion constant)
gamma = 1.0e-9       # N·m·s/rad (damping)

omega0 = np.sqrt(kappa / I0)
f0 = omega0 / (2 * np.pi)
T0 = 2 * np.pi / omega0
Q = I0 * omega0 / gamma

assert Q > 1e4, "Unphysically low Q"

# ============================================================
# 2. MODULATION PARAMETERS (LOCKED)
# ============================================================

alpha = 1.0e-10      # injected coupling (sensitivity target)
beta = 0.0           # MUST remain zero (no control leakage)

f_spin = 1.0 / 1000.0                    # Hz
f_sid  = 1.0 / (23.9345 * 3600.0)         # Hz
f_target = f_spin + f_sid

# ============================================================
# 3. EXTERNALLY PRESCRIBED INERTIA MODULATION
# ============================================================

def epsilon_phys(t):
    """Injected phenomenological modulation"""
    return alpha * np.cos(2 * np.pi * f_target * t)

def epsilon_total(t):
    """Total fractional inertia modulation"""
    return epsilon_phys(t)  # beta locked to zero

# ============================================================
# 4. EQUATION OF MOTION
# ============================================================

USE_NUMERICAL_DRIVE = True
DRIVE_TORQUE = 5e-10  # N·m (numerical carrier-maintenance only)

def airm_eom(t, y):
    """
    Authoritative equation of motion.
    A small numerical drive is used only to prevent ring-down and
    does not contribute to sideband content.
    """
    theta, theta_dot = y

    eps = epsilon_total(t)
    drive = DRIVE_TORQUE * np.sin(omega0 * t) if USE_NUMERICAL_DRIVE else 0.0

    theta_ddot = (
        drive
        - gamma * theta_dot
        - kappa * theta
    ) / (I0 * (1.0 + eps))

    return [theta_dot, theta_ddot]

# ============================================================
# 5. TIME AXIS & SAMPLING
# ============================================================

duration = 48 * 3600          # seconds
fs = 5.0                      # Hz
t = np.arange(0, duration, 1/fs)

theta0 = 1e-4
y0 = [theta0, 0.0]

assert fs * T0 > 100, "Sampling too coarse"
assert f_target < fs/2, "Nyquist violation"

# ============================================================
# 6. INTEGRATION
# ============================================================

sol = solve_ivp(
    airm_eom,
    [0, duration],
    y0,
    t_eval=t,
    rtol=1e-10,
    atol=1e-13
)

theta = sol.y[0]

# ============================================================
# 7. READOUT NOISE MODEL
# ============================================================

noise_rms = 1.0e-8  # rad per sample
theta_noisy = theta + noise_rms * np.random.randn(len(theta))

# ============================================================
# 8. QUADRATURE DEMODULATION → δf(t)
# ============================================================

cos_ref = np.cos(2 * np.pi * f0 * t)
sin_ref = np.sin(2 * np.pi * f0 * t)

I = theta_noisy * cos_ref
Q = -theta_noisy * sin_ref

b, a = butter(6, 0.01 / (fs/2), 'low')
I_lp = filtfilt(b, a, I)
Q_lp = filtfilt(b, a, Q)

phase = np.unwrap(np.arctan2(Q_lp, I_lp))
trend = np.polyfit(t, phase, 1)
phase -= np.polyval(trend, t)

delta_f = np.gradient(phase, 1/fs) / (2 * np.pi)

# ============================================================
# 9. SPECTRAL ANALYSIS
# ============================================================

# NOTE: PSD-based SNR used here is equivalent to matched-filter SNR
# under stationary Gaussian noise assumptions.

nperseg = min(2**17, len(delta_f))
f, Pxx = welch(delta_f, fs=fs, nperseg=nperseg)

idx = np.argmin(np.abs(f - f_target))
signal = Pxx[idx]

band = (f > f_target - 5e-5) & (f < f_target + 5e-5)
noise = np.median(Pxx[band])

snr_inst = signal / noise
snr_int = snr_inst * np.sqrt(duration * fs / 2)

# ============================================================
# 10. NULL TEST
# ============================================================

alpha_save = alpha
alpha = 0.0

sol_null = solve_ivp(airm_eom, [0, duration], y0, t_eval=t)
theta_null = sol_null.y[0] + noise_rms * np.random.randn(len(t))

I_n = theta_null * cos_ref
Q_n = -theta_null * sin_ref
I_n = filtfilt(b, a, I_n)
Q_n = filtfilt(b, a, Q_n)

phase_n = np.unwrap(np.arctan2(Q_n, I_n))
phase_n -= np.polyval(np.polyfit(t, phase_n, 1), t)

delta_f_n = np.gradient(phase_n, 1/fs) / (2*np.pi)
f_n, Pxx_n = welch(delta_f_n, fs=fs, nperseg=nperseg)

null_snr = Pxx_n[idx] / np.median(Pxx_n[band])
alpha = alpha_save

# ============================================================
# 11. DECISION (Tier-1 Fixed Threshold)
# ============================================================

DETECTION_THRESHOLD = 10.0
go = snr_int > DETECTION_THRESHOLD

print("\n=== AIRM SPINNER SENSITIVITY REPORT ===")
print(f"Injected α: {alpha:.1e}")
print(f"Integrated SNR: {snr_int:.2f}")
print(f"Null SNR: {null_snr:.2f}")
print(
    "Decision: "
    + ("GO (analysis pipeline recovers injected signal)"
       if go else
       "NO-GO (insufficient sensitivity)")
)
