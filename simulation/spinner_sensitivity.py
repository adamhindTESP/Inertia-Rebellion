import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import butter, filtfilt

# ============================================================
# 1. HARDWARE PARAMETERS (TARGET BUILD VALUES)
# ============================================================

I0 = 1.0e-3          # kg·m² (moment of inertia)
kappa = 1.0e-4       # N·m/rad (torsion constant)
gamma = kappa / 1e5  # approximate damping for Q ≈ 10^5

omega0 = np.sqrt(kappa / I0)
f0 = omega0 / (2 * np.pi)
T0 = 2 * np.pi / omega0

print(f"Natural frequency f0 = {f0:.4f} Hz")
print(f"Natural period T0 = {T0:.2f} s")
print(f"Q ≈ {omega0 * I0 / gamma:.0f}")

# ============================================================
# 2. MODULATION PARAMETERS (SPINNER + SIDEREAL)
# ============================================================

f_spin = 1.0 / 1000.0             # 1 rev / 1000 s
f_sid = 1.0 / (23.9345 * 3600.0)  # sidereal frequency
phi = 0.0                          # phase offset

f_plus = f_spin + f_sid
f_minus = f_spin - f_sid

# ============================================================
# 3. SIMULATION SETTINGS
# ============================================================

duration = 48 * 3600.0        # seconds (48 hours)
fs = 1.0                      # Hz sampling
t_eval = np.arange(0, duration, 1/fs)
dt = 1/fs

y0 = [1e-6, 0.0]              # initial conditions [theta, theta_dot]
noise_density = 1.0e-8        # rad/√Hz
noise_rms_per_sample = noise_density * np.sqrt(fs)

# ============================================================
# 4. EPSILON(t) — INERTIA MODULATION
# ============================================================

def epsilon_total(t, alpha):
    """Time-dependent fractional inertia modulation."""
    return alpha * np.cos(2 * np.pi * (f_spin + f_sid) * t + phi)

def airm_eom(t, y, alpha):
    """ODE: torsion pendulum with small anisotropic modulation."""
    theta, theta_dot = y
    eps = epsilon_total(t, alpha)
    theta_ddot = (-gamma * theta_dot - kappa * theta) / (I0 * (1.0 + eps))
    return [theta_dot, theta_ddot]

# ============================================================
# 5. SIMULATION & DEMODULATION
# ============================================================

def run_simulation(alpha):
    """Solve dynamics and demodulate the frequency modulation."""
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
    theta_noisy = theta + noise_rms_per_sample * np.random.randn(len(theta))

    # Quadrature demodulation at f0
    cos_ref = np.cos(2 * np.pi * f0 * t_eval)
    sin_ref = np.sin(2 * np.pi * f0 * t_eval)
    I = theta_noisy * cos_ref
    Q = -theta_noisy * sin_ref

    # Low-pass filter to isolate slow modulation
    cutoff = 0.01  # Hz
    b, a = butter(6, cutoff / (fs / 2), 'low')
    I_low = filtfilt(b, a, I)
    Q_low = filtfilt(b, a, Q)

    # Phase and detrend
    phase = np.unwrap(np.arctan2(Q_low, I_low))
    slope, intercept = np.polyfit(t_eval, phase, 1)
    phase_detrended = phase - (slope * t_eval + intercept)

    # Frequency deviation δf(t)
    dphase_dt = np.gradient(phase_detrended, dt)
    delta_f = dphase_dt / (2 * np.pi)

    return delta_f

def extract_modulation_power(delta_f, target_freq):
    """Project δf onto known modulation frequency for optimal detection."""
    cos_temp = np.cos(2 * np.pi * target_freq * t_eval)
    sin_temp = np.sin(2 * np.pi * target_freq * t_eval)

    # Normalize
    cos_temp /= np.sqrt(np.mean(cos_temp**2))
    sin_temp /= np.sqrt(np.mean(sin_temp**2))

    a = np.mean(delta_f * cos_temp)
    b = np.mean(delta_f * sin_temp)

    mod_amp = np.sqrt(a**2 + b**2)
    return mod_amp

# ============================================================
# 6. SENSITIVITY SWEEP
# ============================================================

alphas = np.logspace(-13, -9, 9)
mod_amps = []

# Baseline null statistics
null_amps_plus = [extract_modulation_power(run_simulation(0.0), f_plus) for _ in range(10)]
null_mean_plus = np.mean(null_amps_plus)
null_std_plus = np.std(null_amps_plus)

print(f"\nNull background (+ channel): {null_mean_plus:.2e} ± {null_std_plus:.2e} Hz")

# Sweep
for alpha in alphas:
    delta_f = run_simulation(alpha)
    amp_plus = extract_modulation_power(delta_f, f_plus)
    mod_amps.append(amp_plus)

mod_amps = np.array(mod_amps)
snrs = (mod_amps - null_mean_plus) / (null_std_plus + 1e-20)

# Decision
alpha_min = min(alphas[snrs > 10]) if any(snrs > 10) else max(alphas)

print("\n=== GO / NO-GO DECISION ===")
if alpha_min <= 1e-10:
    print("✅ GO — α_min ≤ 10^-10. Build the apparatus.")
else:
    print("⛔ NO-GO — α_min > 10^-10. Pivot or refine simulation.")

# ============================================================
# 7. PLOT RESULTS
# ============================================================

plt.figure(figsize=(10, 6))
plt.loglog(alphas, mod_amps, 'o-', label='Recovered δf (Hz)')
plt.loglog(alphas, alphas*f0/2, '--', label='Theory: α × f0 / 2')
plt.axvline(1e-10, color='green', ls=':', label='GO gate')
plt.xlabel('α (dimensionless)')
plt.ylabel('Modulation amplitude δf (Hz)')
plt.title('AIRM Sensitivity Sweep — Spinner-enabled Demodulation')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
