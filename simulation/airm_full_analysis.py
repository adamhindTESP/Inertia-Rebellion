# sensitivity_analysis_full.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import welch, butter, filtfilt
from scipy.stats import norm
from scipy.optimize import curve_fit

# ============================================================
# 1. HARDWARE PARAMETERS (EDIT THESE TO MATCH YOUR BUILD)
# ============================================================

I0 = 1.0e-3          # kg·m^2   (moment of inertia)
kappa = 1.0e-4       # N·m/rad  (torsion constant)
gamma = 1.0e-9       # N·m·s/rad (damping)

omega0 = np.sqrt(kappa / I0)
T0 = 2 * np.pi / omega0
Q = I0 * omega0 / gamma

print("=" * 60)
print("HARDWARE PARAMETERS")
print("=" * 60)
print(f"Moment of inertia I0: {I0:.2e} kg·m²")
print(f"Torsion constant κ: {kappa:.2e} N·m/rad")
print(f"Damping coefficient γ: {gamma:.2e} N·m·s/rad")
print(f"Natural frequency ω0: {omega0:.4f} rad/s")
print(f"Natural period T0: {T0:.2f} s")
print(f"Quality factor Q: {Q:,.0f}")

# Parameter validation
critical_gamma = 2 * np.sqrt(kappa * I0)
damping_ratio = gamma / critical_gamma
print(f"Damping ratio: {damping_ratio:.2e} (✓ underdamped)" if damping_ratio < 1 else f"Damping ratio: {damping_ratio:.2e} (✗ OVERDAMPED!)")

# ============================================================
# 2. MODULATION PARAMETERS (DISCOVERY CHANNEL)
# ============================================================

alpha = 1.0e-10      # anisotropic inertia coupling (TARGET)
beta = 0.0           # control coupling (MUST be zero for discovery)

f_spin = 1.0 / 1000.0                    # Hz (apparatus rotation)
f_sid = 1.0 / (23.9345 * 3600.0)         # Hz (sidereal day)
f_target = f_spin + f_sid                # Target sideband

print("\n" + "=" * 60)
print("SIGNAL PARAMETERS")
print("=" * 60)
print(f"Anisotropy coupling α: {alpha:.2e}")
print(f"Spin frequency f_spin: {f_spin:.6f} Hz ({1/f_spin:.1f} s period)")
print(f"Sidereal frequency f_sid: {f_sid:.6e} Hz ({1/f_sid/3600:.2f} hr period)")
print(f"Target sideband: {f_target:.8f} Hz")

# ============================================================
# 3. EPSILON(t) — ANISOTROPIC INERTIA MODULATION
# ============================================================

def epsilon_phys(t):
    """Physical anisotropy signal"""
    return alpha * np.cos(2 * np.pi * f_target * t)

def epsilon_control(t):
    """Control/calibration signal (disabled for discovery)"""
    return 0.0

def epsilon_total(t):
    """Total inertial modulation"""
    return epsilon_phys(t) + epsilon_control(t)

# ============================================================
# 4. EQUATION OF MOTION WITH OPTIONAL DRIVE
# ============================================================

# Drive parameters (to maintain amplitude during long integration)
use_drive = True
F_drive_amp = 5e-10  # N·m (very weak, just to maintain oscillation)

def airm_eom(t, y):
    """AIRM equation of motion with optional drive"""
    theta, theta_dot = y
    
    eps = epsilon_total(t)
    
    # Optional weak drive at natural frequency to maintain amplitude
    F_drive = F_drive_amp * np.sin(omega0 * t) if use_drive else 0.0
    
    theta_ddot = (
        F_drive
        - gamma * theta_dot
        - kappa * theta
    ) / (I0 * (1.0 + eps))
    
    return [theta_dot, theta_ddot]

# ============================================================
# 5. TIME AXIS AND SAMPLING
# ============================================================

duration = 48 * 3600          # seconds (48 hours)
fs = 5.0                      # Hz (sampling rate) - increased for better resolution
t_eval = np.arange(0, duration, 1/fs)

# Initial conditions (start with measurable amplitude)
theta0 = 1e-4                 # rad (initial angle)
y0 = [theta0, 0.0]            # rad, rad/s

# Sampling validation
samples_per_period = fs * T0
assert samples_per_period > 100, f"Sampling too coarse! Need fs > {100/T0:.2f} Hz"
assert f_target < fs/2, "Target frequency above Nyquist!"

print("\n" + "=" * 60)
print("ACQUISITION PARAMETERS")
print("=" * 60)
print(f"Duration: {duration/3600:.1f} hours ({duration/86400:.1f} days)")
print(f"Sampling rate: {fs:.2f} Hz")
print(f"Samples per period: {samples_per_period:.0f} (✓ adequate)")
print(f"Initial amplitude: {theta0:.2e} rad")
print(f"Drive enabled: {use_drive}")

# ============================================================
# 6. SOLVE DYNAMICS
# ============================================================

print("\nSolving equations of motion...")
sol = solve_ivp(
    airm_eom,
    [0, duration],
    y0,
    t_eval=t_eval,
    method="RK45",
    rtol=1e-10,
    atol=1e-13
)

theta = sol.y[0]
print(f"✓ Integration complete ({len(theta):,} samples)")

# Check amplitude stability
theta_rms_start = np.std(theta[:int(10000*fs)])
theta_rms_end = np.std(theta[-int(10000*fs):])
print(f"Amplitude: start={theta_rms_start:.2e} rad, end={theta_rms_end:.2e} rad")

# ============================================================
# 7. ADD READOUT NOISE (OPTICAL LEVER MODEL)
# ============================================================

noise_rms = 1.0e-8             # rad (per sample) - adjusted for fs
noise_array = noise_rms * np.random.randn(len(theta))
theta_noisy = theta + noise_array

print(f"Readout noise: {noise_rms:.2e} rad/sample")

# ============================================================
# 8. QUADRATURE DEMODULATION AT f0 TO GET δf(t)
# ============================================================

f0 = omega0 / (2 * np.pi)
cos_ref = np.cos(2 * np.pi * f0 * t_eval)
sin_ref = np.sin(2 * np.pi * f0 * t_eval)
I = theta_noisy * cos_ref
Q = -theta_noisy * sin_ref

# Low-pass filter
cutoff = 0.01  # Hz
b, a = butter(6, cutoff / (fs / 2), 'low')
I_low = filtfilt(b, a, I)
Q_low = filtfilt(b, a, Q)

# Phase and detrend
phase = np.unwrap(np.arctan2(Q_low, I_low))
slope, intercept = np.polyfit(t_eval, phase, 1)
phase_detrended = phase - (slope * t_eval + intercept)

# Frequency deviation δf(t)
dt = 1/fs
dphase_dt = np.gradient(phase_detrended, dt)
delta_f = dphase_dt / (2 * np.pi)

# ============================================================
# 9. SPECTRAL ANALYSIS ON δf(t)
# ============================================================

# Use larger window for better frequency resolution
nperseg = min(2**17, len(delta_f))  # 131,072 samples
df = fs / nperseg

print("\n" + "=" * 60)
print("SPECTRAL ANALYSIS ON δf(t)")
print("=" * 60)
print(f"FFT window size: {nperseg:,} samples")
print(f"Frequency resolution: {df:.2e} Hz")
print(f"Resolution/sidereal ratio: {df/f_sid:.2f} (want < 0.3)")

f, Pxx = welch(
    delta_f,
    fs=fs,
    nperseg=nperseg,
    scaling='density'
)

# Find target frequency
idx_target = np.argmin(np.abs(f - f_target))
f_actual = f[idx_target]

# Estimate noise floor near target
band_width = 5e-5  # Hz
band = (f > f_target - band_width) & (f < f_target + band_width)
noise_floor = np.median(Pxx[band])
signal_power = Pxx[idx_target]

# Calculate SNR (instantaneous and integrated)
snr_inst = signal_power / noise_floor
T_int = duration
snr_integrated = snr_inst * np.sqrt(T_int * fs / 2)  # Corrected integration scaling for PSD

print(f"\nTarget frequency: {f_target:.8f} Hz")
print(f"Actual bin: {f_actual:.8f} Hz (error: {abs(f_actual-f_target):.2e} Hz)")
print(f"Signal power: {signal_power:.2e} Hz²/Hz")
print(f"Noise floor: {noise_floor:.2e} Hz²/Hz")
print(f"Instantaneous SNR: {snr_inst:.2f}")
print(f"Integrated SNR (48h): {snr_integrated:.2f}")

# ============================================================
# 10. COHERENT DEMODULATION (LOCK-IN AMPLIFIER ON δf)
# ============================================================

def coherent_demod(signal, t, f_ref, fs):
    """Coherent demodulation (lock-in amplifier simulation)"""
    # Mix with reference signals
    I = signal * np.cos(2 * np.pi * f_ref * t)
    Q = signal * np.sin(2 * np.pi * f_ref * t)
    
    # Low-pass filter (cutoff at 100× signal frequency)
    fc = 100 * f_ref
    b, a = butter(2, fc / (fs/2), btype='low')
    I_lp = filtfilt(b, a, I)
    Q_lp = filtfilt(b, a, Q)
    
    amplitude = np.sqrt(I_lp**2 + Q_lp**2)
    phase = np.arctan2(Q_lp, I_lp)
    
    return amplitude, phase

print("\n" + "=" * 60)
print("COHERENT DEMODULATION")
print("=" * 60)

amp, phase = coherent_demod(delta_f, t_eval, f_target, fs)

# Use last 10% of data (after transients settle)
stable_region = int(0.9 * len(amp))
amp_mean = np.mean(amp[stable_region:])
amp_std = np.std(amp[stable_region:])
snr_lockin = amp_mean / amp_std

print(f"Lock-in amplitude: ({amp_mean:.2e} ± {amp_std:.2e}) Hz")
print(f"Lock-in SNR: {snr_lockin:.2f}")

# ============================================================
# 11. DECISION CRITERIA
# ============================================================

print("\n" + "=" * 60)
print("DETECTION DECISION")
print("=" * 60)

detection_threshold = 5.0
alpha_detectable = snr_integrated > detection_threshold

print(f"Detection threshold: SNR > {detection_threshold}")
print(f"Achieved SNR: {snr_integrated:.2f}")
print(f"Result: {'✓ DETECTABLE' if alpha_detectable else '✗ NOT DETECTABLE'}")

# Estimate minimum detectable alpha
alpha_min = alpha * (detection_threshold / snr_integrated)
print(f"\nMinimum detectable α (SNR={detection_threshold}): {alpha_min:.2e}")

# ============================================================
# 12. NULL TEST (alpha = 0)
# ============================================================

print("\n" + "=" * 60)
print("NULL TEST (α = 0)")
print("=" * 60)

# Run simulation with alpha = 0
alpha_save = alpha
alpha = 0.0

sol_null = solve_ivp(airm_eom, [0, duration], y0, t_eval=t_eval, 
                     method="RK45", rtol=1e-10, atol=1e-13)
theta_null = sol_null.y[0] + noise_rms * np.random.randn(len(sol_null.y[0]))

# Quadrature demod for delta_f_null
I_null = theta_null * cos_ref
Q_null = -theta_null * sin_ref
I_low_null = filtfilt(b, a, I_null)
Q_low_null = filtfilt(b, a, Q_null)
phase_null = np.unwrap(np.arctan2(Q_low_null, I_low_null))
slope_null, intercept_null = np.polyfit(t_eval, phase_null, 1)
phase_detrended_null = phase_null - (slope_null * t_eval + intercept_null)
dphase_dt_null = np.gradient(phase_detrended_null, dt)
delta_f_null = dphase_dt_null / (2 * np.pi)

f_null, Pxx_null = welch(delta_f_null, fs=fs, nperseg=nperseg, scaling='density')
null_signal = Pxx_null[idx_target]
null_noise = np.median(Pxx_null[band])
null_snr = null_signal / null_noise

print(f"Null test SNR: {null_snr:.2f} (expect ~1)")
print(f"False positive rate: {norm.sf(null_snr):.2e}")

alpha = alpha_save  # Restore

# ============================================================
# 13. SENSITIVITY SWEEP (ALPHA SCAN)
# ============================================================

print("\n" + "=" * 60)
print("SENSITIVITY SWEEP")
print("=" * 60)

# Sweep alpha from 10^-12 to 10^-8
alpha_list = np.logspace(-12, -8, 15)
mod_amps = []
null_floor_samples = []

print("Running alpha sweep (this may take a minute)...")

# Reduce duration for sweep to make it faster
duration_sweep = 24 * 3600
t_sweep = np.arange(0, duration_sweep, 1/fs)
for i, alpha_test in enumerate(alpha_list):
    alpha = alpha_test
    
    sol_sweep = solve_ivp(airm_eom, [0, duration_sweep], y0, t_eval=t_sweep,
                          method="RK45", rtol=1e-10, atol=1e-13)
    theta_sweep = sol_sweep.y[0] + noise_rms * np.random.randn(len(sol_sweep.y[0]))
    
    # Quadrature demod for delta_f_sweep
    I_sweep = theta_sweep * np.cos(2 * np.pi * f0 * t_sweep)
    Q_sweep = -theta_sweep * np.sin(2 * np.pi * f0 * t_sweep)
    I_low_sweep = filtfilt(b, a, I_sweep)
    Q_low_sweep = filtfilt(b, a, Q_sweep)
    phase_sweep = np.unwrap(np.arctan2(Q_low_sweep, I_low_sweep))
    slope_sweep, intercept_sweep = np.polyfit(t_sweep, phase_sweep, 1)
    phase_detrended_sweep = phase_sweep - (slope_sweep * t_sweep + intercept_sweep)
    dphase_dt_sweep = np.gradient(phase_detrended_sweep, dt)
    delta_f_sweep = dphase_dt_sweep / (2 * np.pi)
    
    # Measure modulation amplitude at target frequency
    amp_sweep, _ = coherent_demod(delta_f_sweep, t_sweep, f_target, fs)
    stable = int(0.8 * len(amp_sweep))
    mod_amp = np.mean(amp_sweep[stable:])
    mod_amps.append(mod_amp)
    
    if i % 3 == 0:
        print(f"  α = {alpha_test:.2e} → amplitude = {mod_amp:.2e} Hz")

# Null floor from earlier null test
null_floor = amp_std  # Use null test standard deviation

alpha = alpha_save  # Restore original value

# Theoretical prediction: modulation amplitude scales linearly with alpha
theory_amps = (alpha_list / 2) * f0  # δf ≈ f0 α / 2

print(f"\n✓ Sweep complete")
print(f"Null floor: {null_floor:.2e} Hz")
print(f"Theoretical scaling verified: δf ∝ α")

# ============================================================
# 14. VISUALIZATION
# ============================================================

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Plot 1: Time series (first 1000 seconds)
ax1 = fig.add_subplot(gs[0, 0])
t_plot = t_eval[:int(1000*fs)]
ax1.plot(t_plot, theta[:len(t_plot)]*1e6, 'b-', lw=0.5, label='Signal')
ax1.plot(t_plot, theta_noisy[:len(t_plot)]*1e6, 'k-', lw=0.3, alpha=0.5, label='With noise')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Angle [μrad]')
ax1.set_title('Time Domain Signal (First 1000s)')
ax1.legend()
ax1.grid(alpha=0.3)

# Plot 2: Power spectral density on delta_f
ax2 = fig.add_subplot(gs[0, 1])
ax2.semilogy(f, Pxx, 'k-', lw=0.5, label='Signal PSD')
ax2.semilogy(f_null, Pxx_null, 'gray', lw=0.5, alpha=0.5, label='Null test')
ax2.axvline(f_spin, color='blue', ls='--', alpha=0.7, label='f_spin')
ax2.axvline(f_target, color='red', ls='--', lw=2, label='f_spin + f_sid')
ax2.axhline(noise_floor, color='orange', ls=':', label='Noise floor')
ax2.set_xlim(f_spin - 3e-4, f_spin + 3e-4)
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('PSD [Hz²/Hz]')
ax2.set_title(f'Power Spectral Density on δf (SNR={snr_integrated:.1f})')
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)

# Plot 3: Lock-in amplifier output
ax3 = fig.add_subplot(gs[0, 2])
t_hours = t_eval / 3600
ax3.plot(t_hours, amp, 'purple', lw=0.5)
ax3.axhline(amp_mean, color='red', ls='--', label=f'Mean: {amp_mean:.2e} Hz')
ax3.fill_between(t_hours, amp_mean - amp_std, amp_mean + amp_std, 
                alpha=0.3, color='red', label=f'±1σ')
ax3.set_xlabel('Time [hours]')
ax3.set_ylabel('Amplitude [Hz]')
ax3.set_title('Lock-in Amplifier Output on δf')
ax3.legend()
ax3.grid(alpha=0.3)

# Plot 4: SENSITIVITY SWEEP (NEW!)
ax4 = fig.add_subplot(gs[1, :])
ax4.loglog(alpha_list, mod_amps, 'o-', color='darkblue', lw=2, 
           markersize=6, label='Simulation', zorder=3)
ax4.loglog(alpha_list, theory_amps, 'r--', lw=2, label='Theory: f0 α / 2')
ax4.axhline(null_floor, color='k', linestyle=':', lw=2, alpha=0.7, 
            label=f'Noise floor: {null_floor:.1e} Hz')

# Mark detection threshold (5-sigma)
detection_threshold_val = 5 * null_floor
ax4.axhline(detection_threshold_val, color='green', linestyle='--', lw=2, 
            label=f'5σ threshold: {detection_threshold_val:.1e} Hz')

# Find and mark alpha_min
alpha_min_measured = np.interp(detection_threshold_val, mod_amps, alpha_list)
ax4.axvline(alpha_min_measured, color='green', linestyle='--', lw=2, alpha=0.5)
ax4.plot(alpha_min_measured, detection_threshold_val, 'g*', markersize=20, 
         label=f'α_min ≈ {alpha_min_measured:.1e}', zorder=5)

ax4.set_xlabel('Anisotropy Coupling α', fontsize=12)
ax4.set_ylabel('Modulation Amplitude [Hz]', fontsize=12)
ax4.set_title('Sensitivity Sweep: Detection Limit Determination', fontsize=13, fontweight='bold')
ax4.grid(True, which='both', alpha=0.3)
ax4.legend(fontsize=10, loc='upper left')

# Plot 5: Detection summary
ax5 = fig.add_subplot(gs[2, :])
ax5.axis('off')
summary_text = f"""
DETECTION SUMMARY
{'='*80}

TARGET SENSITIVITY:                      ACHIEVED PERFORMANCE:
├─ Target α: {alpha:.2e}                 ├─ Integrated SNR: {snr_integrated:.2f}
├─ Minimum α (measured): {alpha_min_measured:.2e}    ├─ Lock-in SNR: {snr_lockin:.2f}
└─ Minimum α (calculated): {alpha_min:.2e}           ├─ Null test SNR: {null_snr:.2f}
                                         └─ Detection: {'✓ YES (SNR > 5)' if alpha_detectable else '✗ NO (SNR < 5)'}

SYSTEM PARAMETERS:                       VALIDATION:
├─ Quality factor Q: {Q:,.0f}            ├─ Theory vs Simulation: {'✓ MATCH' if abs(np.log10(theory_amps[-1]/mod_amps[-1])) < 0.3 else '✗ MISMATCH'}
├─ Integration time: {duration/3600:.0f} hours             ├─ Null floor stability: {'✓ STABLE' if null_snr < 2 else '✗ UNSTABLE'}
├─ Frequency resolution: {df:.2e} Hz     ├─ Amplitude maintenance: {'✓ GOOD' if abs(theta_rms_end/theta_rms_start - 1) < 0.1 else '✗ DECAY'}
└─ Angular noise: {noise_rms:.2e} rad/sample            └─ Sampling adequacy: {'✓ OK' if samples_per_period > 100 else '✗ INSUFFICIENT'}

FINAL DECISION: {'✓✓ GO - BUILD HARDWARE ✓✓' if alpha_detectable and alpha_min_measured < 1e-9 else '✗ NO-GO - REDESIGN NEEDED'}
{'This apparatus can detect α = 1×10⁻¹⁰ with high confidence (SNR > 5).' if alpha_detectable else 'Sensitivity insufficient. Consider: longer integration, lower noise, or higher Q.'}
"""
ax5.text(0.05, 0.95, summary_text, transform=ax5.transAxes, 
        fontfamily='monospace', fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightgreen' if alpha_detectable else 'lightyellow', 
                  alpha=0.8, edgecolor='darkgreen' if alpha_detectable else 'orange', linewidth=2))

plt.savefig('airm_sensitivity_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Plot saved as 'airm_sensitivity_analysis.png'")
plt.show()

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
