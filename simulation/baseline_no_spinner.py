import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import welch

# ============================================================
# 1. HARDWARE PARAMETERS (EDIT THESE TO MATCH YOUR BUILD)
# ============================================================

I0 = 1.0e-3          # kg·m^2   (moment of inertia)
kappa = 1.0e-4       # N·m/rad  (torsion constant)
gamma = 1.0e-9       # N·m·s/rad (damping)

omega0 = np.sqrt(kappa / I0)
T0 = 2 * np.pi / omega0

print(f"Natural period T0 = {T0:.2f} s")

# ============================================================
# 2. MODULATION PARAMETERS (DISCOVERY CHANNEL)
# ============================================================

alpha = 1.0e-10      # anisotropic inertia coupling (sweep this)
beta = 0.0           # control coupling (MUST be zero for discovery)

f_spin = 1.0 / 1000.0
f_sid = 1.0 / (23.9345 * 3600.0)

# ============================================================
# 3. EPSILON(t) — LOCKED FORM
# ============================================================

def epsilon_phys(t):
    return alpha * np.cos(2 * np.pi * f_spin * t)

def epsilon_control(t):
    return 0.0        # MUST remain zero for core tests

def epsilon_total(t):
    return epsilon_phys(t) + epsilon_control(t)

# ============================================================
# 4. EQUATION OF MOTION (AUTHORITATIVE)
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
# 5. TIME AXIS (MULTI-DAY RUN)
# ============================================================

duration = 48 * 3600          # seconds
fs = 1.0                      # Hz (sampling rate)
t_eval = np.arange(0, duration, 1/fs)

# Initial conditions
y0 = [1e-6, 0.0]               # rad, rad/s

# ============================================================
# 6. SOLVE DYNAMICS
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

noise_rms = 1.0e-8             # rad (per sample)
theta_noisy = theta + noise_rms * np.random.randn(len(theta))

# ============================================================
# 8. SPECTRAL ANALYSIS
# ============================================================

f, Pxx = welch(
    theta_noisy,
    fs=fs,
    nperseg=2**14,
    scaling='density'
)

target_freq = f_spin + f_sid
idx_target = np.argmin(np.abs(f - target_freq))

# Noise estimate near target
band = (f > target_freq - 1e-5) & (f < target_freq + 1e-5)
noise_power = np.median(Pxx[band])
signal_power = Pxx[idx_target]

snr = signal_power / noise_power

print("\n===== AIRM SIMULATION REPORT =====")
print(f"alpha = {alpha:.1e}")
print(f"Target frequency = {target_freq:.6e} Hz")
print(f"Signal power = {signal_power:.2e}")
print(f"Noise power = {noise_power:.2e}")
print(f"SNR = {snr:.2f}")

# ============================================================
# 9. PLOTS
# ============================================================

plt.figure(figsize=(12, 5))

plt.semilogy(f, Pxx, 'k', lw=0.5)
plt.axvline(f_spin, color='blue', ls='--', label='Spin')
plt.axvline(target_freq, color='red', ls='--', label='Spin ± Sidereal')

plt.xlim(f_spin - 5e-4, f_spin + 5e-4)
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD [rad^2/Hz]")
plt.title(f"AIRM PSD — SNR ≈ {snr:.1f}")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()
