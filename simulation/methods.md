***

# Methods for AIRM Sensitivity Simulations

This document defines the **numerical methodology** used in the AIRM (Anisotropic Inertial Response Model) torsion‑pendulum sensitivity simulations.[1]

It specifies the physical model, numerical integration scheme, noise assumptions, analysis pipeline, falsification tests, and decision criteria to enable **full reproducibility and independent audit**.[1]

***

## IMPORTANT SCIENTIFIC SCOPE STATEMENT

These simulations:

- **DO NOT** demonstrate new physics  
- **DO NOT** assert the existence of anisotropic inertia  
- **DO** test whether a predefined analysis pipeline can recover a *known, externally prescribed modulation* under controlled assumptions  

All signals are injected by construction.  
All conclusions are methodological.[1]

A numerical “GO” means:

> *If a signal of this form existed at this strength, the pipeline would recover it.*

Reality is decided by hardware, not simulations.[1]

***

## 1. Overview

The simulations evaluate the detectability of a small, time‑dependent modulation of the effective moment of inertia of a torsional oscillator.[1]

Two configurations are studied:

- **Baseline (null)**  
  $$\epsilon(t) = 0$$

- **Spinner‑enabled**  
  $$\epsilon(t) = \alpha \cos[2\pi (f_\text{spin} + f_\text{sid}) t + \phi]$$

where $$\alpha$$ is a dimensionless phenomenological coupling parameter.[1]

***

## 2. Physical Model

The torsion pendulum is modeled as a damped harmonic oscillator with a phenomenological, time‑dependent effective inertia.[1]

The **equation of motion implemented in the code** is:

$$
I_0 [1 + \epsilon(t)] \ddot{\theta}(t) + \gamma \dot{\theta}(t) + \kappa \theta(t) = \tau_\text{drive}(t)
$$

where:

- $$\theta(t)$$ — angular displacement (rad)  
- $$I_0$$ — nominal moment of inertia (kg·m²)  
- $$\gamma$$ — damping coefficient (N·m·s/rad)  
- $$\kappa$$ — torsion constant (N·m/rad)  
- $$\epsilon(t)$$ — externally prescribed fractional inertia modulation  
- $$\tau_\text{drive}(t)$$ — **numerical carrier‑maintenance torque**[1]

### Numerical Drive (Explicitly Non‑Physical)

A small sinusoidal drive torque is included:

$$
\tau_\text{drive}(t) = \tau_0 \sin(\omega_0 t)
$$

This drive exists **only** to prevent numerical ring‑down during long integrations and to maintain a stable carrier for phase demodulation.[1]

- It does **not** inject power at the target sideband  
- It does **not** affect detectability conclusions  
- It has no physical interpretation  

***

## 3. Numerical Integration

- Integrator: `scipy.integrate.solve_ivp`  
- Method: RK45  
- Relative tolerance: `rtol = 1e-10`  
- Absolute tolerance: `atol = 1e-13`[1]

### Time Sampling

- Sampling rate: `fs = 5 Hz`  
- Time step: `dt = 0.2 s`  
- Total duration: `48 hours`  

This duration is sufficient to resolve sidereal‑scale modulation frequencies.[1]

***

## 4. Noise Model

Measurement noise is modeled as **additive, white Gaussian noise** applied directly to the angular displacement.[1]

- RMS noise per sample: `1 × 10⁻⁸ rad`  
- Noise is uncorrelated between samples  
- No colored or environmental noise is included  

This represents an optimistic but realistic optical‑lever readout limit.[1]

***

## 5. Analysis Pipeline

The same pipeline is applied to both null and signal‑injected simulations.[1]

### Step‑by‑Step Procedure

1. Integrate the equation of motion  
2. Add measurement noise to $$\theta(t)$$  
3. Perform quadrature (IQ) demodulation at the natural frequency $$f_0$$  
4. Low‑pass filter the I/Q channels to isolate slow phase evolution  
5. Unwrap the phase and remove linear trends  
6. Convert phase slope to instantaneous frequency deviation:  
   $$
   \delta f(t) = \frac{1}{2\pi} \frac{d\phi}{dt}
   $$  
7. Estimate recovered signal amplitude using coherent projection (matched filtering) at the **target frequency**  
   $$
   f_\text{target} = f_\text{spin} + f_\text{sid}
   $$
[1]

***

## 6. Null and Falsification Tests

### 6.1 Baseline Null Test

- Set $$\alpha = 0$$  
- Run the full pipeline  
- Establish the numerical noise floor  
- Verify absence of coherent recovery at $$f_\text{target}$$[1]

### 6.2 Wrong‑Frequency Falsification

- Analyze recovered data at an intentionally incorrect frequency  
- Confirm recovered amplitude collapses to the null background  

A pipeline that recovers comparable amplitudes at correct and incorrect frequencies is considered invalid.[1]

***

## 7. Detection Metric & Decision Rule

Detection significance is quantified using a signal‑to‑noise ratio (SNR) relative to the null background.[1]

| Condition | Interpretation |
|----------|----------------|
| `SNR ≥ 10` | **GO** — pipeline is sensitive |
| `SNR < 10` | **NO‑GO** — sensitivity insufficient |

This threshold is **fixed a priori** and not tuned post hoc.[1]

***

## 8. Reproducibility

All simulations are reproducible using Python 3.x with:

- `numpy`  
- `scipy`  
- `matplotlib` (optional)[1]

Relevant scripts:

- `airm_full_analysis.py`  
- `baseline_no_spinner.py`  
- `falsification_test.py`  
- `README.md` (directory‑level context)[1]

Random number generation is explicitly seeded for reproducibility.[1]

***

## 9. Limitations

- The modulation $$\epsilon(t)$$ is purely phenomenological  
- Linear dynamics are assumed  
- Environmental and nonlinear effects are not modeled  
- Sensitivity depends on assumed noise level and quality factor[1]

Results represent **best‑case methodological sensitivity**, not guaranteed experimental performance.[1]

***

## Final Statement

These simulations exist to enforce **analysis discipline**.[1]

They ensure that:

- the pipeline behaves correctly,  
- falsification tests work, and  
- numerical artifacts are not mistaken for signals.[1]

A numerical **GO** is an invitation to build and validate hardware — **not a statement about nature.**[1]
