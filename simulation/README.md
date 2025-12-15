# AIRM Sensitivity Simulations

This directory contains numerical simulations used to evaluate the detectability of small, time-dependent modulations in the effective inertia of a torsional oscillator.

These simulations are sensitivity and validation studies only. They do not assert the existence of new physics, nor do they claim a specific physical origin for any modulation term.

All assumptions are explicit and the code is provided for independent review and falsification.

---

## Overview

The simulations model a torsion pendulum with a phenomenological fractional modulation of the effective moment of inertia,

I(t) = I₀ [1 + ε(t)]

where ε(t) is a small, externally prescribed function used solely to test analysis sensitivity.

Two configurations are provided:

1. A baseline control simulation with no modulation
2. A spinner-enabled configuration with a known, time-dependent modulation frequency

---

## Files

### baseline_no_spinner.py

Control simulation with no imposed modulation.

Purpose:
- Establish the numerical noise floor
- Verify the analysis does not produce false positives
- Provide a null reference for comparison

Expected result:
- No statistically significant signal at the target frequencies

---

### spinner_sensitivity.py

Sensitivity study with a prescribed modulation at known frequencies (f_spin ± f_sid).

Purpose:
- Test recoverability of weak injected modulation
- Quantify signal-to-noise ratio versus coupling strength α
- Define conservative GO / NO-GO thresholds for hardware development

Expected result:
- Linear scaling of recovered signal with α
- Clear separation from null background above threshold

---

## Important Notes

- The modulation term ε(t) is phenomenological and does not assume a physical mechanism.
- A GO result indicates detectability under stated assumptions only.
- No claim is made regarding modification of inertia or coupling to fundamental fields.
- Results are conditional on the model and noise assumptions.

---

## Intended Use

These simulations are intended to:
- Validate analysis methods
- Guide experimental sensitivity requirements
- Enable independent replication and review

They are not evidence for new physical effects.

---

## Next Steps

1. Independent code review
2. Cross-validation with alternative noise and damping models
3. Tier-1 hardware null testing prior to exploratory measurements
