# AIRM Sensitivity Simulations

This directory contains numerical simulations used to evaluate the detectability of small, time-dependent modulations in the effective inertia of a torsional oscillator.

**Important:** These simulations are sensitivity and validation studies only. They do **not** assert the existence of new physics and make no claims about fundamental mechanisms. All assumptions are explicit, and the code is provided for independent review and falsification.

---

## Overview

The simulations model a torsion pendulum with a phenomenological fractional modulation of the effective moment of inertia:

$$
I(t) = I_0 \,[1 + \epsilon(t)]
$$

where `ε(t)` is a small, externally prescribed function used solely to test analysis sensitivity.

Two configurations are provided:  

1. **Baseline Control:** no modulation  
2. **Spinner-Enabled Simulation:** prescribed modulation at known frequencies \(f_\text{spin} \pm f_\text{sid}\)

---

## Files

| File | Purpose | Expected Result |
|------|--------|----------------|
| [`baseline_no_spinner.py`](baseline_no_spinner.py) | Control simulation with no imposed modulation | No statistically significant signal at target frequencies; establishes numerical noise floor |
| [`sensitivity_analysis.py`](sensitivity_analysis.py) | Spinner-enabled sensitivity study with sweep over modulation amplitude `α` | Linear scaling of recovered signal with `α`; clear separation from null background; GO/NO-GO thresholds established |
| [`falsification_test.py`](falsification_test.py) | Validates analysis by testing a nearby “wrong” frequency | Signal collapses when demodulated at offset frequency (confirms pipeline correctness) |
| [`methods.md`](methods.md) | Detailed derivations of EOM, demodulation, and noise modeling | Reference for contributors to understand math and implementation |
| [`README_spinner.md`](README_spinner.md) | Companion README for spinner simulation | Optional, keeps main README concise |

---

## Simulation Description

**Pendulum Parameters**

- \( \omega_0 = \sqrt{\kappa / I_0} \approx 0.316\ \text{rad/s} \)  
- \( f_0 = \omega_0 / 2\pi \approx 0.0503\ \text{Hz} \)  
- \( \gamma = \kappa / 10^5 \approx 10^{-9}\ \text{N·m·s/rad} \) (Q = 100,000)  
- Initial deflection: \( \theta_0 = 10^{-6}\ \text{rad} \)

**Modulation**

$$
\epsilon(t) = \alpha \cos\big[ 2 \pi (f_\text{spin} + f_\text{sid}) t + \phi \big]
$$

- \( f_\text{spin} = 0.001\ \text{Hz} \)  
- \( f_\text{sid} \approx 1.1606 \times 10^{-5}\ \text{Hz} \)

**Noise**

- Gaussian, RMS ≈ \( 1 \times 10^{-8}\ \text{rad/sample} \), simulating optical lever readout

**Analysis Pipeline**

- Quadrature demodulation with low-pass filtering isolates frequency modulation  
- Instantaneous frequency extracted via phase derivative (Hilbert transform)  
- Signal amplitude computed by projection onto cos/sin reference at target frequency  

**Sweep & Decision**

- Vary `α` (logspace) → compute SNR against null runs → define conservative GO / NO-GO thresholds

---

## Important Notes

- `ε(t)` is phenomenological; no physical origin is assumed  
- A GO result indicates detectability under stated assumptions only  
- Null simulations establish the noise floor; spinner simulations test recoverability  
- Falsification tests ensure your pipeline does not detect signals at incorrect frequencies

---

## Intended Use

These simulations are intended to:  

- Validate analysis methods  
- Guide experimental sensitivity requirements  
- Enable independent replication and review  

**Not intended to provide evidence for new physics.**

---

## Requirements

- Python 3.x  
- `numpy`  
- `scipy`  
- `matplotlib` (optional, for plotting)

```bash
pip install numpy scipy matplotlib
