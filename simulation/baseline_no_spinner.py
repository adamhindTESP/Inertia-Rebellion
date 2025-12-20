#!/usr/bin/env python3
"""
Baseline No-Spinner Simulation — Deliberate NO-GO
================================================

Purpose:
- Demonstrate that without controlled rotation, no clean detection
  channel exists for a hypothetical inertial-anisotropy signal.
- Establish the numerical noise floor.
- Motivate the necessity of the spinner-enabled configuration.

This script:
- Injects NO modulation (ε(t) = 0)
- Performs NO frequency translation
- Produces NO coherent signal at the target sideband

A low SNR here is expected and REQUIRED.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import welch

# Reproducibility
np.random.seed(0)

# ============================================================
# 1. HARDWARE PARAMETERS (MATCH MAIN SIMULATIONS)
# ============================================================

I0 = 1.0e-3          # kg·m^2   (moment of inertia)
kappa = 1.0e-4       # N·m/rad  (torsion constant)
Q = 1.0e5            # quality factor

gamma = kappa / Q   # damping coefficient

omega0 = np.sqrt(kappa / I0)
f0 = omega0 / (2 * np.pi)
T0 = 2 * np.pi / omega0

print(f"Natural period T0 = {T0:.2f} s")

# ============================================================
# 2. MODULATION PARAMETERS (DEFINED BUT UNUSED)
# ============================================================

# Defined for comparison with spinner-enabled case
f_spin = 1.0 / 1000.0
f_sid  = 1.0 / (23.9345 * 3600.0)

# Hypothetical target frequency (NOT populated here)
f_target = f_spin + f_sid

# ============================================================
# 3. FRACTIONAL INERTIA MODULATION (BASELINE)
# ============================================================

def epsilon_total(t):
    """No modulation in baseline no-spinner case."""
    return 0.0

# ============================================================
# 4. EQUATION OF MOTION
# ============================================================

def airm_eom(t, y):
    theta, theta_dot = y
    eps = epsilon_total(t)

    theta_ddot = (
        -gamma * theta_dot
        -kappa * theta
    ) / (I0 * (1.0 + eps))

    return [theta_dot, theta_ddot]

# ============================================================
# 5. TIME AXIS (LONG INTEGRATION)
# ============================================================

duration = 48 * 3600          # seconds
fs = 1.0                      # Hz
dt = 1.0 / fs
t_eval = np.arange(0, duration, dt)

y0 = [1e-6, 0.0]              # initial conditions

# ============================================================
# 6. INTEGRATE DYNAMICS
# ============================================================

sol = solve_ivp(
    airm_eom,
    [0, duration],
    y0,
    t_eval=t_eval,
    method="RK45",
    rtol=1e-9,
    atol=1e-12
)

theta = sol.y[0]

# ============================================================
# 7. ADD READOUT NOISE (OPTICAL LEVER MODEL)
# ============================================================

noise_rms = 1.0e-8             # rad per sample
theta_noisy = theta + noise_rms * np.random.randn(len(theta))

# ============================================================
# 8. SPECTRAL ANALYSIS (PSD)
# ============================================================

f, Pxx = welch(
    theta_noisy,
    fs=fs,
    nperseg=2**14,
    scaling="density"
)

idx_target = np.argmin(np.abs(f - f_target))

band = (f > f_target - 1e-5) & (f < f_target + 1e-5)
noise_power = np.median(Pxx[band])
signal_power = Pxx[idx_target]

snr = signal_power / noise_power

print("\n===== BASELINE NO-SPINNER REPORT =====")
print("This configuration is EXPECTED to be NO-GO")
print("--------------------------------------")
print(f"Hypothetical target frequency = {f_target:.6e} Hz")
print(f"Signal power = {signal_power:.2e}")
print(f"Noise power  = {noise_power:.2e}")
print(f"SNR          = {snr:.2f}")

# ============================================================
# 9. PLOT
# ============================================================

plt.figure(figsize=(12, 5))

plt.semilogy(f, Pxx, "k", lw=0.6)
plt.axvline(f_target, color="red", ls="--", label="Hypothetical f_spin + f_sid")

plt.xlim(f_target - 5e-4, f_target + 5e-4)
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD [rad²/Hz]")
plt.title("Baseline No-Spinner PSD (Deliberate NO-GO)")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()
