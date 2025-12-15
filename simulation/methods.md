## Methods for AIRM Sensitivity Simulations

This document describes the methodology used in the torsion-pendulum sensitivity simulations. It clarifies assumptions, analysis steps, and observables to enable reproducibility and independent review.

---

## 1. Overview

The simulations evaluate the detectability of small, time-dependent modulations in the effective inertia of a torsional oscillator. This work supports ground testing of ultra-precise inertial sensors relevant to space-based gravitational wave detection and precision geodesy.

**Important:** These simulations are not intended to demonstrate new physics. Their sole purpose is to establish the sensitivity limits of the measurement and analysis pipeline.

Two configurations are simulated:

- **Baseline (No Spinner):** Static orientation with no applied modulation  
- **Spinner-Enabled:** Controlled, time-dependent modulation at known frequencies  
  (f_spin ± f_sid)

---

## 2. Model Equations

The torsion pendulum is modeled as a damped harmonic oscillator with a small,
externally prescribed fractional modulation of the moment of inertia.

Equation of motion:

theta_ddot(t)
+ (gamma / I0) * theta_dot(t)
+ [kappa / (I0 * (1 + epsilon(t)))] * theta(t)
= 0

---

### Variables and Parameters

- **theta(t)** — angular displacement [rad]  
- **I0** — nominal moment of inertia [kg·m²]  
- **kappa** — torsion constant [N·m / rad]  
- **gamma** — damping coefficient [N·m·s / rad]  
- **epsilon(t)** — small, prescribed fractional modulation  

**Important:**  
The modulation term epsilon(t) is phenomenological and does not assume any physical
mechanism. In the spinner-enabled configuration it is sinusoidal at the combined
spin and sidereal frequencies.

---

## 3. Numerical Methods

- The system of ordinary differential equations is solved using  
  `scipy.integrate.solve_ivp` with the RK45 solver.
- Solver tolerances:
  - Relative tolerance: rtol = 1e-9
  - Absolute tolerance: atol = 1e-12
- Time sampling:
  - Uniform time step: dt = 1 s
  - Total duration: 48 hours (sufficient to resolve sidereal timescales)

### Noise Model

- Readout noise is modeled as additive Gaussian noise
- RMS amplitude: 1e-8 rad per sample
- This approximates realistic optical-lever sensitivity in a torsion pendulum apparatus

---

## 4. Analysis Procedure

### 4.1 Baseline Simulation (NO-GO)

- Compute the power spectral density (PSD) using Welch’s method
- Inspect the spectrum at target frequencies
- Establish the numerical noise floor and verify absence of false positives

### 4.2 Spinner-Enabled Sensitivity Analysis

- Demodulate angular displacement at the nominal resonance frequency f0
  using quadrature (lock-in style) detection
- Apply low-pass filtering to isolate slow modulation  
  (cutoff = 0.01 Hz)
- Extract phase and compute instantaneous frequency deviation delta_f(t)
- Project delta_f(t) onto reference sinusoids at  
  f_spin ± f_sid to recover modulation amplitude
- Sweep coupling strength alpha to determine minimum detectable signal

### 4.3 Falsification / Null Test

A falsification test is performed by deliberately demodulating the recovered
frequency deviation at a slightly incorrect reference frequency.

- When the demodulation frequency is offset from the true injected modulation,
  the recovered signal collapses to the null background
- This confirms that the analysis pipeline does not generate spurious coherent
  signals and requires correct phase coherence for signal recovery

---

## 5. Decision Criteria

| Metric | Threshold | Interpretation |
|------|----------|---------------|
| SNR | > 10 | Signal considered detectable (GO) |
| SNR | ≤ 10 | Configuration considered null-limited (NO-GO) |

---

## 6. Reproducibility

All parameters, initial conditions, and noise assumptions are explicitly defined
in the simulation scripts:

- `baseline_no_spinner.py`
- `sensitivity_analysis.py`
- `falsification_test.py`

Independent users can reproduce the simulations using Python 3.x with standard
scientific libraries (numpy, scipy, matplotlib).

---

## 7. Limitations

- epsilon(t) is purely phenomenological and does not represent any known interaction
- Simulations assume linear dynamics; real hardware may exhibit additional
  nonlinearities and environmental couplings
- Results are conditional on the assumed noise level, damping, and quality factor

---

## 8. References / Further Reading

**Torsion Pendulum Methods**
- Adelberger et al., Annual Review of Nuclear and Particle Science (2003)
- Li et al., Sensors (2024)
- Chen et al., Sensors (2023)

**Numerical Methods**
- SciPy documentation for `solve_ivp`

**Weak-Signal Detection**
- Saulson, Physical Review D (1990)
- Cagnoli et al., Review of Scientific Instruments (2000)

---

**Usage Note:**  
For simulation context and file-level descriptions, see `README.md` in this directory.
