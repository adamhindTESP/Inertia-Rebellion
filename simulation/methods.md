# Methods for AIRM Sensitivity Simulations

This document describes the methodology used in the AIRM torsion-pendulum sensitivity simulations. It defines the physical model, numerical methods, noise assumptions, analysis pipeline, and decision criteria to enable full reproducibility and independent review.

---

## 1. Overview

The simulations evaluate the detectability of small, externally prescribed, time-dependent modulations in the effective inertia of a torsional oscillator.

IMPORTANT SCOPE STATEMENT  
These simulations do NOT demonstrate new physics.  
Their sole purpose is to establish the sensitivity limits of the measurement and analysis pipeline under controlled assumptions.

Two configurations are simulated:

- Baseline (no spinner):  
  epsilon(t) = 0

- Spinner-enabled:  
  epsilon(t) = alpha * cos(2π * (f_spin + f_sid) * t + phi)

---

## 2. Model Equations

The torsion pendulum is modeled as a damped harmonic oscillator with a small, phenomenological modulation of its effective inertia.

The equation of motion integrated by the simulations is:

theta_ddot(t)
+ (gamma / I0) * theta_dot(t)
+ [kappa / (I0 * (1 + epsilon(t)))] * theta(t)
= 0

Where:

- theta(t) is the angular displacement [rad]  
- I0 is the nominal moment of inertia [kg·m²]  
- kappa is the torsion constant [N·m / rad]  
- gamma is the damping coefficient [N·m·s / rad]  
- epsilon(t) is an externally prescribed fractional inertia modulation  

NOTE  
The modulation epsilon(t) is purely phenomenological and does not assume any physical interaction or mechanism.

---

## 3. Numerical Methods

- The equations of motion are solved using:
  - scipy.integrate.solve_ivp
  - RK45 integrator
- Solver tolerances:
  - rtol = 1e-9
  - atol = 1e-12
- Time sampling:
  - Uniform step: dt = 1 second
  - Total duration: 48 hours

The integration duration is sufficient to resolve sidereal-scale modulation frequencies.

---

## 4. Noise Model

Readout noise is modeled as additive Gaussian noise applied directly to the angular displacement.

- RMS noise per sample:
  - 1e-8 rad
- Noise is uncorrelated between samples
- This approximates realistic optical-lever sensitivity in torsion-pendulum experiments

No colored noise or frequency-dependent shaping is applied.

---

## 5. Analysis Procedure

### 5.1 Baseline Simulation (NO-GO Reference)

- Integrate the equation of motion with epsilon(t) = 0
- Compute the power spectral density (PSD) using Welch’s method
- Inspect the spectrum at target frequencies
- Establish the numerical noise floor
- Verify the absence of coherent false positives

This configuration defines the null background.

---

### 5.2 Spinner-Enabled Sensitivity Analysis

For simulations with nonzero modulation:

1. Integrate the equation of motion
2. Add measurement noise
3. Perform quadrature (IQ) demodulation at the natural frequency f0
4. Apply low-pass filtering to isolate slow phase evolution
5. Unwrap the phase and remove linear trends
6. Convert phase slope to instantaneous frequency deviation:

   delta_f(t) = (1 / (2π)) * d(phi)/dt

7. Project delta_f(t) onto reference sinusoids at:
   - f_spin + f_sid
   - f_spin − f_sid
8. Sweep the coupling strength alpha to determine the minimum detectable signal

---

### 5.3 Falsification / Null Test

A falsification test is performed by deliberately analyzing the recovered signal at an incorrect reference frequency.

- When the demodulation frequency does not match the injected modulation, the recovered signal collapses to the null background
- This confirms the pipeline does not generate spurious coherent signals
- Signal recovery requires correct phase coherence

---

## 6. Decision Criteria

Detection significance is quantified using a signal-to-noise ratio (SNR) relative to the null distribution.

| Metric | Threshold | Interpretation |
|------|----------|----------------|
| SNR > 10 | GO | Signal considered detectable |
| SNR ≤ 10 | NO-GO | Configuration is null-limited |

The null distribution is obtained from simulations with alpha = 0.

---

## 7. Reproducibility

All parameters, assumptions, and analysis steps are implemented in:

- baseline_no_spinner.py
- sensitivity_analysis_full.py
- falsification_test.py
- simulation/README.md

Simulations can be reproduced using Python 3.x with:

- numpy
- scipy
- matplotlib (optional, for plots)

---

## 8. Limitations

- epsilon(t) is phenomenological and does not represent a known interaction
- Simulations assume linear dynamics
- Real hardware may exhibit nonlinearities and environmental couplings
- Results depend on assumed noise level, damping, and quality factor

---

## 9. References / Further Reading

Torsion Pendulum Methods
- Adelberger et al., Annual Review of Nuclear and Particle Science (2003)
- Li et al., Sensors (2024)
- Chen et al., Sensors (2023)

Numerical Methods
- SciPy documentation for solve_ivp

Weak-Signal Detection
- Saulson, Physical Review D (1990)
- Cagnoli et al., Review of Scientific Instruments (2000)

---

Usage note:  
For directory-level context and file descriptions, see simulation/README.md.
