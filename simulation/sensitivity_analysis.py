import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import butter, filtfilt

# ============================================================
# 1. HARDWARE PARAMETERS (Spinner Build)
# ============================================================

I0 = 1.0e-3          # kg·m²
kappa = 1.0e-4       # N·m/rad
gamma = 3.16e-9      # damping for Q ≈ 100,000

omega0 = np.sqrt(kappa / I0)
f0 = omega0 / (2*np.pi)
T0 = 2*np.pi / omega0

print(f"Natural frequency f0 = {f0:.5f} Hz, T0 = {T0:.2f} s, Q ≈ {omega0*I0/gamma:.0f}")

# ============================================================
# 2. MODULATION PARAMETERS
# ============================================================

f_spin = 1.0/1000.0                 # Spinner frequency
f_sid = 1.0/(23.9345*3600.0)        # Sidereal frequency
alpha_list = np.logspace(-12, -9, 10)  # Sweep of modulation amplitudes
phi = 0.0

# ============================================================
# 3. SIMULATION SETTINGS
# ============================================================

duration = 2*3600.0                  # 2 hours for testing
fs = 0.5                             # Hz sampling
t_eval = np.arange(0, duration, 1/fs)
dt = 1/fs

y0 = [1e-6, 0.0]                     # initial [theta, theta_dot]
noise_density = 1e-8                  # rad/√Hz
noise_rms_per_sample = noise_density * np.sqrt(fs / 2)  # Nyquist correction

# ============================================================
# 4. EPSILON(t) — TIME-DEPENDENT MODULATION
# ============================================================

def epsilon_total(t, alpha):
    """Fractional inertia modulation matching README (f_spin + f_sid)."""
    return alpha * np.cos(2*np.pi*(f_spin + f_sid)*t + phi)

# ============================================================
# 5. EQUATION OF MOTION
# ============================================================

def airm_eom(t, y, alpha):
    theta, theta_dot = y
    eps = epsilon_total(t, alpha)
    theta_ddot = (-gamma*theta_dot - kappa*theta) / (I0*(1 + eps))
    return [theta_dot, theta_ddot]

# ============================================================
# 6. SIMULATION FUNCTION
# ============================================================

def run_simulation(alpha):
    sol = solve_ivp(
        lambda t, y: airm_eom(t, y, alpha),
        [0, duration],
        y0,
        t_eval=t_eval,
        method='RK45',
        rtol=1e-6,
        atol=1e-8,
        max_step=10.0
    )
    theta = sol.y[0]
    theta_noisy = theta + noise_rms_per_sample * np.random.randn(len(theta))
    return theta_noisy

# ============================================================
# 7. DEMODULATION & QUADRATURE EXTRACTION
# ============================================================

def quadrature_demod(theta_noisy):
    cos_ref = np.cos(2*np.pi*f0*t_eval)
    sin_ref = np.sin(2*np.pi*f0*t_eval)
    I = theta_noisy * cos_ref
    Q = -theta_noisy * sin_ref
    # Low-pass filter
    b, a = butter(6, 0.003 / (fs / 2), 'low')
    I_low = filtfilt(b, a, I)
    Q_low = filtfilt(b, a, Q)
    phase = np.unwrap(np.arctan2(Q_low, I_low))
    # Detrend linear drift
    slope, intercept = np.polyfit(t_eval, phase, 1)
    phase_detrended = phase - (slope * t_eval + intercept)
    delta_f = np.gradient(phase_detrended, dt) / (2*np.pi)
    return delta_f

# ============================================================
# 8. MATCHED FILTER / MODULATION POWER
# ============================================================

def extract_modulation_power(delta_f, target_freq):
    cos_temp = np.cos(2*np.pi*target_freq*t_eval)
    sin_temp = np.sin(2*np.pi*target_freq*t_eval)
    cos_temp /= np.sqrt(np.mean(cos_temp**2))
    sin_temp /= np.sqrt(np.mean(sin_temp**2))
    a = np.mean(delta_f * cos_temp)
    b = np.mean(delta_f * sin_temp)
    return np.sqrt(a**2 + b**2)

# ============================================================
# 9. RUN SWEEP OVER ALPHAS
# ============================================================

f_target = f_spin + f_sid
mod_amps = []
null_mean, null_std = [], []

for alpha in alpha_list:
    theta_noisy = run_simulation(alpha)
    delta_f = quadrature_demod(theta_noisy)
    amp = extract_modulation_power(delta_f, f_target)
    mod_amps.append(amp)

# Null estimate (alpha=0)
for _ in range(5):
    theta_null = run_simulation(0)
    delta_f_null = quadrature_demod(theta_null)
    null_amp = extract_modulation_power(delta_f_null, f_target)
    null_mean.append(null_amp)

null_mean = np.mean(null_mean)
null_std = np.std(null_mean)

# GO/NO-GO decision
SNR = np.array(mod_amps)/ (null_std + 1e-30)
go_alpha = alpha_list[np.argmax(SNR > 10)] if np.any(SNR > 10) else None

print("\n===== SPINNER SENSITIVITY ANALYSIS =====")
print(f"Target frequency f+ = {f_target:.6e} Hz")
print(f"Null mean = {null_mean:.2e}, null std = {null_std:.2e}")
print(f"Sweep amplitudes: {alpha_list}")
print(f"Measured modulation amplitudes: {mod_amps}")
print(f"SNR = {SNR}")
print(f"GO decision: alpha_min = {go_alpha}")

# ============================================================
# 10. PLOT RESULTS
# ============================================================

plt.figure(figsize=(10,5))
plt.loglog(alpha_list, mod_amps, 'o-', label='Simulation')
plt.loglog(alpha_list, alpha_list*f0/2, '--', label='Theory')
plt.xlabel('alpha')
plt.ylabel('Modulation amplitude [Hz]')
plt.title('Spinner Sensitivity Sweep (f_spin + f_sid)')
plt.grid(True, which='both', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
