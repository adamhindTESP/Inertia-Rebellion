# ============================================================
# Inertia Rebellion - Tightened Falsification Test
# ============================================================

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import butter, filtfilt

# ----------------- Hardware Parameters -----------------
I0 = 1.0e-3          # kg·m²
kappa = 1.0e-4       # N·m/rad
gamma = kappa / 1e5  # damping for Q ≈ 10^5
f0 = np.sqrt(kappa / I0) / (2 * np.pi)

# ----------------- Modulation Parameters -----------------
f_spin = 1.0 / 1000.0
f_sid = 1.0 / (23.9345 * 3600.0)
phi = 0.0

# Frequencies
f_true = f_spin + f_sid
delta = 0.02                # 2% offset for false test
f_false = f_true * (1 + delta)

# ----------------- Simulation Settings -----------------
duration = 48 * 3600.0      # 48 hours
fs = 1.0                     # Hz
t_eval = np.arange(0, duration, 1/fs)
dt = 1/fs
y0 = [1e-6, 0.0]            # initial conditions
noise_density = 1.0e-8      # rad/√Hz
num_realizations = 10        # average to reduce noise

# ----------------- Core Functions -----------------
def epsilon_total(t, alpha):
    return alpha * np.cos(2 * np.pi * (f_spin + f_sid) * t + phi)

def airm_eom(t, y, alpha):
    theta, theta_dot = y
    eps = epsilon_total(t, alpha)
    theta_ddot = (-gamma * theta_dot - kappa * theta) / (I0 * (1.0 + eps))
    return [theta_dot, theta_ddot]

def run_simulation(alpha):
    sol = solve_ivp(
        lambda t, y: airm_eom(t, y, alpha),
        [0, duration],
        y0,
        t_eval=t_eval,
        method="RK45",
        rtol=1e-9,
        atol=1e-12
    )
    theta = sol.y[0]
    return theta

def extract_modulation_power(delta_f, target_freq):
    cos_temp = np.cos(2 * np.pi * target_freq * t_eval)
    sin_temp = np.sin(2 * np.pi * target_freq * t_eval)
    cos_temp /= np.sqrt(np.mean(cos_temp**2))
    sin_temp /= np.sqrt(np.mean(sin_temp**2))
    a = np.mean(delta_f * cos_temp)
    b = np.mean(delta_f * sin_temp)
    return np.sqrt(a**2 + b**2)

# ----------------- Run Falsification Test -----------------
alpha = 1e-11  # GO-level modulation

amps_true = []
amps_false = []

for _ in range(num_realizations):
    theta = run_simulation(alpha)
    # Add noise
    theta_noisy = theta + noise_density * np.sqrt(fs) * np.random.randn(len(theta))

    # Demodulate at f0
    cos_ref = np.cos(2 * np.pi * f0 * t_eval)
    sin_ref = np.sin(2 * np.pi * f0 * t_eval)
    I = theta_noisy * cos_ref
    Q = -theta_noisy * sin_ref

    # Low-pass filter (tight)
    cutoff = 0.003
    b, a = butter(6, cutoff / (fs / 2), 'low')
    I_low = filtfilt(b, a, I)
    Q_low = filtfilt(b, a, Q)

    # Phase and detrend
    phase = np.unwrap(np.arctan2(Q_low, I_low))
    slope, intercept = np.polyfit(t_eval, phase, 1)
    phase_detrended = phase - (slope * t_eval + intercept)
    dphase_dt = np.gradient(phase_detrended, dt)
    delta_f = dphase_dt / (2 * np.pi)

    # Extract modulation amplitudes
    amps_true.append(extract_modulation_power(delta_f, f_true))
    amps_false.append(extract_modulation_power(delta_f, f_false))

# Average results
amp_true_avg = np.mean(amps_true)
amp_false_avg = np.mean(amps_false)
ratio = amp_false_avg / (amp_true_avg + 1e-30)

# Print results
print("Tightened Falsification Test Results")
print(f"True frequency amplitude:  {amp_true_avg:.2e} Hz")
print(f"False frequency amplitude: {amp_false_avg:.2e} Hz")
print(f"False / True ratio:        {ratio:.3e}")

if ratio < 0.1:
    print("✅ PASS: Signal collapses under frequency offset.")
else:
    print("⛔ FAIL: Signal persists under frequency offset.")
