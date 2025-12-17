# Simulation — AIRM Sensitivity & Falsification

This directory contains **numerical simulations** used to validate the analysis pipeline and quantify the **detectability** of small, externally prescribed modulations in the effective inertia of a torsional oscillator.

⚠️ **Important scientific scope statement**

These simulations:
- **Do NOT claim new physics**
- **Do NOT assert the existence of anisotropic inertia**
- **DO** test whether a proposed signal-processing pipeline can recover a *known injected signal* under controlled assumptions
- **DO** implement falsification and null tests

All assumptions are explicit. All code is provided for independent review, reproduction, and criticism.

---

## Purpose of This Directory

The simulations serve four tightly defined roles:

1. **Sensitivity estimation**  
   Determine what modulation amplitudes `α` would be detectable *if* they existed.

2. **Pipeline validation**  
   Verify that the demodulation + extraction chain behaves correctly.

3. **Null testing**  
   Establish the numerical noise floor with no injected signal.

4. **Falsification**  
   Demonstrate that recovered signals collapse when tested at the wrong frequency.

This directory is the **numerical analog of Tier 1 hardware validation**.

---

## Core Physical Model (As Implemented)

The torsion pendulum is modeled with a *phenomenological* time-dependent effective inertia:

\[
I_{\mathrm{eff}}(t) = I_0 \,[1 + \epsilon(t)]
\]

where the modulation is externally prescribed as:

\[
\epsilon(t) = \alpha \cos\!\left(2\pi f_{\mathrm{target}} t + \phi\right),
\quad
f_{\mathrm{target}} = f_{\mathrm{spin}} + f_{\mathrm{sid}}.
\]

The equation of motion integrated by the code is:

\[
I_0[1+\epsilon(t)]\,\ddot{\theta}(t)
+ \gamma\,\dot{\theta}(t)
+ \kappa\,\theta(t) = 0.
\]

This form is used **only** to test detectability and analysis robustness.

---

## Noise Model (Explicit and Auditable)

The simulations assume Gaussian measurement noise specified as a **one-sided amplitude spectral density**:

- Units: rad / √Hz

Discrete per-sample RMS noise is computed as:

\[
\sigma_{\mathrm{sample}} = \mathrm{ASD}\,\sqrt{\frac{f_s}{2}}.
\]

This convention matches standard signal-processing practice and is enforced consistently throughout the code.

---

## Analysis Pipeline (Exactly What the Code Does)

For each realization:

1. Integrate the equation of motion using `solve_ivp`
2. Add measurement noise
3. Perform **IQ demodulation at the natural frequency** \(f_0\)
4. Low-pass filter to isolate baseband phase evolution
5. Unwrap phase and remove linear trend
6. Convert phase slope to instantaneous frequency deviation:
   \[
   \delta f(t) = \frac{1}{2\pi}\frac{d\phi}{dt}
   \]
7. Estimate recovered signal amplitude using **coherent projection**
   (matched filtering) at:
   - the injected target frequency
   - a nearby “wrong” frequency (falsification test)

---

## Files

| File | Role |
|-----|-----|
| `sensitivity_analysis.py` | Main script: sensitivity sweep, null distribution, falsification |
| `baseline_no_spinner.py` | Control simulation with `α = 0` only |
| `falsification_test.py` | Focused wrong-frequency collapse test |
| `methods.md` | Mathematical derivations and signal-processing rationale |
| `README.md` | This document |

---

## GO / NO-GO Logic

The sensitivity script performs:

- **Null runs** (`α = 0`) → establishes numerical noise distribution
- **Sweep over α** → measures recovered amplitude vs null
- **SNR vs null**:
  \[
  \mathrm{SNR} = \frac{\langle A_{\mathrm{true}}\rangle - \mu_{\mathrm{null}}}{\sigma_{\mathrm{null}}}
  \]

### Decision rule (as coded)

- **GO** if best recovered SNR ≥ 10  
- **NO-GO** otherwise

A falsification ratio is also reported:

\[
\text{false/true} =
\frac{A(f_{\mathrm{false}})}{A(f_{\mathrm{target}})}.
\]

Values ≪ 1 indicate a well-behaved pipeline.

---

## Outputs

Each run automatically creates:

simulation/runs/<RUN_ID>/
├── run_meta.json          # full config + derived parameters
├── alpha_sweep.csv        # numerical results
├── snr_sweep.png          # (optional) SNR vs alpha
└── falsification_ratio.png# (optional) wrong-frequency test

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
- `numpy`
- `scipy`
- `matplotlib` (optional, for plots)

```bash
pip install numpy scipy matplotlib

Final Note

A numerical GO here only means:

“If a signal of this form existed at this strength, our pipeline would detect it.”

Reality is decided by Tier 1 hardware validation, not simulations.

This directory exists to make sure you are not fooling yourself before touching data.
