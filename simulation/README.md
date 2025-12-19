# Simulation — AIRM Sensitivity & Falsification

This directory contains numerical simulations used to validate the analysis
pipeline and quantify the detectability of small, externally prescribed
modulations in the effective inertia of a torsional oscillator.

---

## ⚠️ Important Scientific Scope Statement

These simulations:

- **Do NOT** claim new physics  
- **Do NOT** assert the existence of anisotropic inertia  
- **DO** test whether a proposed signal-processing pipeline can recover a
  known injected signal under controlled assumptions  
- **DO** implement explicit null and falsification tests  

All assumptions are explicit.  
All code is provided for independent review, reproduction, and criticism.

---

## Purpose of This Directory

The simulations serve four tightly defined roles:

1. **Sensitivity estimation**  
   Determine what modulation amplitudes α would be detectable *if they existed*.

2. **Pipeline validation**  
   Verify that the demodulation and extraction chain behaves correctly.

3. **Null testing**  
   Establish the numerical noise floor with no injected signal.

4. **Falsification**  
   Demonstrate that recovered signals collapse when tested at the wrong frequency.

This directory is the numerical analog of **Tier-1 hardware validation**.

---

## Core Physical Model (As Implemented)

The torsion pendulum is modeled with a phenomenological, time-dependent
effective inertia:

I_eff(t) = I₀ [1 + ε(t)]

where the externally prescribed modulation is:

ε(t) = α cos(2π f_target t + φ),
f_target = f_spin + f_sid

The equation of motion integrated by the code is:

I₀ [1 + ε(t)] θ̈(t) + γ θ̇(t) + κ θ(t) = 0

This formulation is used **only** to test detectability and analysis robustness.

---

## Noise Model (Explicit and Auditable)

The simulations assume Gaussian measurement noise.

Noise is injected either as:

- a **per-sample RMS angular noise** (rad), or  
- equivalently via a **one-sided ASD** converted to discrete samples using -

σ_sample = ASD · √(f_s / 2)

The chosen convention is explicitly documented in each script and enforced
consistently within that script.

---

## Analysis Pipeline (Exactly What the Code Does)

For each realization:

1. Integrate the equation of motion using `solve_ivp`
2. Add measurement noise
3. Perform IQ demodulation at the natural frequency `f₀`
4. Low-pass filter to isolate baseband phase evolution
5. Unwrap phase and remove linear trend
6. Convert phase slope to instantaneous frequency deviation:

δf(t) = (1 / 2π) dφ/dt

7. Estimate recovered signal amplitude using coherent projection
   (matched filtering) at:
   - the injected target frequency
   - a nearby incorrect frequency (falsification test)

---

## Files

| File | Role |
|-----|-----|
| `airm_full_analysis.py` | Full discovery-channel simulation (spin + sidereal), null tests, sensitivity sweep |
| `sensitivity_analysis.py` | Core sensitivity and GO/NO-GO logic |
| `baseline_no_spinner.py` | Control simulation with α = 0 (no spinner / no sidereal channel) |
| `falsification_test.py` | Focused wrong-frequency collapse test |
| `methods.md` | Mathematical derivations and signal-processing rationale |
| `README.md` | This document |

---

## GO / NO-GO Logic

The sensitivity scripts perform:

- **Null runs** (α = 0) → establish numerical noise distribution  
- **Sweep over α** → measure recovered amplitude vs null  
- **SNR relative to null**:

SNR = (⟨A_true⟩ − μ_null) / σ_null

### Decision rule (as coded)

- **GO** if best recovered SNR ≥ 10  
- **NO-GO** otherwise  

A falsification ratio is also reported:

false / true = A(f_false) / A(f_target)

Values ≪ 1 indicate a well-behaved pipeline.

---

## Outputs

Each run automatically creates:

simulation/runs/<RUN_ID>/
├── run_meta.json            # full configuration + derived parameters
├── alpha_sweep.csv          # numerical results
├── snr_sweep.png            # (optional) SNR vs α
└── falsification_ratio.png  # (optional) wrong-frequency test

All results are timestamped and reproducible.

---

## Intended Use

These simulations are intended to:

- Validate analysis methodology  
- Guide experimental sensitivity requirements  
- Provide transparent falsification evidence  
- Enable independent replication and critique  

They are **not** intended to demonstrate or argue for new physics.

---

## Requirements

- Python 3.x  
- numpy  
- scipy  
- matplotlib (optional, for plots)

pip install numpy scipy matplotlib

---

## Final Note

A numerical **GO** here only means:

> *“If a signal of this form existed at this strength, our pipeline would detect it.”*

Reality is decided by **Tier-1 hardware validation**, not simulations.

This directory exists to ensure you are **not fooling yourself before touching data**.
