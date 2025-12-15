# Methods for AIRM Sensitivity Simulations

This document describes the methodology used in the torsion-pendulum sensitivity simulations. It is intended to clarify assumptions, analysis steps, and observables for reproducibility and independent review.

---

## 1. Overview

The simulations evaluate the detectability of small, time-dependent modulations in the effective inertia of a torsional oscillator.  
They are **not intended to demonstrate new physics**; the purpose is to establish the sensitivity limits of the measurement and analysis pipeline.

Two configurations are simulated:

1. **Baseline (no spinner):** static orientation, no applied modulation.
2. **Spinner-enabled:** controlled, time-dependent modulation at known frequencies (`f_spin ± f_sid`).

---

## 2. Model Equations

The torsion pendulum dynamics are modeled as a damped harmonic oscillator with a small, time-dependent fractional modulation of the inertia:

\[
\theta''(t) + \frac{\gamma}{I_0} \theta'(t) + \frac{\kappa}{I_0(1+\epsilon(t))} \theta(t) = 0
\]

Where:

- \( \theta(t) \) = angular displacement [rad]  
- \( I_0 \) = nominal moment of inertia [kg·m²]  
- \( \kappa \) = torsion constant [N·m/rad]  
- \( \gamma \) = damping coefficient [N·m·s/rad]  
- \( \epsilon(t) \) = small, prescribed fractional modulation  

> **Important:** \( \epsilon(t) \) is phenomenological and does **not** assume a physical mechanism. In the spinner-enabled configuration, it is sinusoidal at the combined spin and sidereal frequencies.

---

## 3. Numerical Methods

- The system of ordinary differential equations is solved using `scipy.integrate.solve_ivp` with the RK45 solver.  
- Relative and absolute tolerances are set to ensure high precision (`rtol=1e-9`, `atol=1e-12`).  
- Time step is uniform (`dt = 1 s`) for a total duration of 48 hours, sufficient to resolve sidereal timescales.

### Noise Model

- Readout noise is included as additive Gaussian noise with RMS amplitude \( 1 \times 10^{-8} \) rad per sample.  
- This models realistic optical-lever sensitivity in a torsion pendulum apparatus.

---

## 4. Analysis Procedure

1. **Baseline (NO-GO)**
   - Compute the power spectral density (PSD) using Welch’s method.
   - Identify target frequencies corresponding to hypothetical modulation.
   - Establish the null noise floor.

2. **Spinner-enabled (Sensitivity)**
   - Demodulate the angular displacement at the nominal resonance frequency (`f0`) using quadrature projection.  
   - Apply low-pass filtering to isolate slow modulation (`cutoff = 0.01 Hz`).  
   - Extract phase and compute instantaneous frequency deviation δf(t).  
   - Project δf(t) onto the known modulation frequencies (`f_spin ± f_sid`) to obtain recovered modulation amplitude.  
   - Sweep coupling strength α to determine minimum detectable signal (SNR > 10).

---

## 5. Decision Criteria

- **GO / NO-GO Threshold:**  
  - A signal is considered detectable (GO) if the recovered modulation amplitude exceeds the null background by at least 10 standard deviations (SNR > 10).  
  - Otherwise, the configuration is considered null-limited (NO-GO).

---

## 6. Reproducibility

- All parameters, initial conditions, and noise assumptions are explicitly defined in the scripts:
  - `baseline_no_spinner.py`  
  - `spinner_sensitivity.py`  
- Independent users can reproduce the simulations and analysis using Python 3.x with standard scientific libraries (`numpy`, `scipy`, `matplotlib`).

---

## 7. Limitations

- ε(t) is purely phenomenological and does **not** represent any known physical interaction.  
- Simulations assume idealized linear dynamics; real hardware may have additional nonlinearities or environmental couplings.  
- Results are conditional on the specified noise, damping, and Q-factor assumptions.  

---

## 8. References / Further Reading

- Precision torsion pendulum dynamics and optical readout methods (e.g., Cagnoli et al., Review of Scientific Instruments, 2000).  
- Numerical ODE solution methods in Python (`scipy.integrate.solve_ivp`).  
- Signal demodulation and coherent detection techniques in weak-signal analysis.
