#!/usr/bin/env python3
"""
AIRM Falsification Test — Frequency Discrimination (Gate 0)
==========================================================

This script enforces the primary Tier-1 falsification requirement:
the analysis pipeline must recover a coherent signal ONLY at the
correct, model-predicted frequency and collapse at nearby frequencies.

This is a NUMERICAL validation only.
No physical claims are made.

PASS condition:
    A(f_false) / A(f_true) < 0.1

Failure INVALIDATES all sensitivity and GO/NO-GO claims.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import butter, filtfilt

# ----------------------------
# Reproducibility
# ----------------------------
np.random.seed(0)

# ----------------------------
# Physical Parameters
# ----------------------------
I0 = 1.0e-3          # kg·m^2
kappa = 1.0e-4       # N·m/rad
gamma = kappa / 1e5  # damping → Q ≈ 1e5

omega0 = np.sqrt(kappa / I0)
f0 = omega0 / (2 * np.pi)

# ----------------------------
# Modulation Parameters
# ----------------------------
alpha = 1.0e-11      # injected test amplitude
phi = 0.0

f_spin = 1.0 / 1000.0
f_sid  = 1.0 / (23.9345 * 3600.0)

f_true = f_spin + f_sid
delta = 0.02                 # 2% frequency offset
f_false = f_true * (1 + delta)

# ----------------------------
# Simulation Settings
# ----------------------------
duration = 48 * 3600.0        # 48 hours
fs = 1.0                      # Hz
dt = 1.0 / fs

t = np.arange(0, duration, dt)
y0 = [1e-6, 0.0]

noise_density = 1.0e-8        # rad / sqrt(Hz)
noise_rms = noise_density * np.sqrt(fs / 2.0)

num_realizations = 10

# Edge trimming (remove filter transients)
trim_s = 600.0                # 10 minutes
mask = (t >= trim_s) & (t <= (duration - trim_s))
t_trim = t[mask]

# ----------------------------
# Model Definition
# ----------------------------
def epsilon(t):
    return alpha * np.cos(2 * np.pi * f_true * t + phi)

def eom(t, y):
    theta, theta_dot = y
    eps = epsilon(t)
    theta_ddot = (-gamma * theta_dot - kappa * theta) / (I0 * (1 + eps))
    return [theta_dot, theta_ddot]

# ----------------------------
# Coherent Amplitude Extractor
# ----------------------------
def coherent_amplitude(x, freq, t):
    c = np.cos(2 * np.pi * freq * t)
    s = np.sin(2 * np.pi * freq * t)

    c /= np.sqrt(np.mean(c**2))
    s /= np.sqrt(np.mean(s**2))

    a = np.mean(x * c)
    b = np.mean(x * s)

    return np.sqrt(a**2 + b**2)

# ----------------------------
# Falsification Loop
# ----------------------------
amps_true = []
amps_false = []

# Low-pass filter (matches main pipeline)
cutoff = 0.003  # Hz
b, a = butter(6, cutoff / (fs / 2), 'low')

for _ in range(num_realizations):

    sol = solve_ivp(
        eom,
        [0, duration],
        y0,
        t_eval=t,
        rtol=1e-9,
        atol=1e-12
    )

    theta = sol.y[0]

    # Add measurement noise
    theta += noise_rms * np.random.randn(len(theta))

    # Quadrature demodulation at carrier f0
    I = theta * np.cos(2 * np.pi * f0 * t)
    Q = -theta * np.sin(2 * np.pi * f0 * t)

    I = filtfilt(b, a, I)
    Q = filtfilt(b, a, Q)

    # Phase → frequency deviation
    phase = np.unwrap(np.arctan2(Q, I))
    trend = np.polyfit(t, phase, 1)
    phase -= np.polyval(trend, t)

    delta_f = np.gradient(phase, dt) / (2 * np.pi)
    delta_f = delta_f[mask]

    # Extract amplitudes
    amps_true.append(coherent_amplitude(delta_f, f_true, t_trim))
    amps_false.append(coherent_amplitude(delta_f, f_false, t_trim))

# ----------------------------
# Results
# ----------------------------
A_true = np.mean(amps_true)
A_false = np.mean(amps_false)
ratio = A_false / (A_true + 1e-30)

print("\n=== FALSIFICATION TEST — GATE 0 ===")
print(f"Recovered amplitude @ f_true :  {A_true:.3e} Hz")
print(f"Recovered amplitude @ f_false: {A_false:.3e} Hz")
print(f"False / True ratio           : {ratio:.3e}")

if ratio < 0.1:
    print("✅ PASS: Frequency discrimination confirmed (Gate 0 PASSED)")
else:
    print("⛔ FAIL: Pipeline insufficiently selective (Gate 0 FAILED)")
