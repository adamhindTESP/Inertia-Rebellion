# Hardware Validation Protocol — Inertia Rebellion Apparatus (AIRM)

This document defines the **mandatory hardware validation gates** for the Inertia Rebellion torsion-balance experiment.

Validation is required to:
- Establish calibration constants
- Exclude common false positives
- Prevent premature interpretation of data
- Ensure reproducibility and auditability

**No sidereal searches, no “detection” claims, and no Tier-2 spinner upgrades are permitted until all applicable validation gates are passed.**

---

## Validation Philosophy

AIRM follows a **gated experimental protocol** inspired by best practices in precision measurement.

Principles:
- Every hardware change introduces new couplings
- Couplings must be bounded before interpretation
- Validation precedes analysis (never the reverse)
- A failed gate is a **NO-GO**, not an anomaly

---

## Tier 1 Validation — Static Pendulum (Required)

Tier 1 establishes baseline torsion-pendulum behavior without any spinner-enabled searches.

### Gate 1 — Free Oscillation Characterization

**Objective:** Verify the pendulum behaves as a linear harmonic oscillator in its working range.

**Procedure:**
1. Displace pendulum by a small angle (recommended: < 5 mrad)
2. Release without external forcing
3. Record angular readout over ≥ 10 oscillation periods
4. Compute the spectrum (or fit a sinusoid + residual)

**Pass Criteria:**
- ≥ 10 cycles visible with **SNR > 10**
- Single dominant peak at the fundamental
- Harmonic distortion bounded:
  - second harmonic amplitude < 1% of the fundamental (measured from PSD or fit residual)
- No measurable amplitude-dependent frequency shift:
  - Δf / f0 < 0.1% across a ≥ 50% amplitude range

**Outputs:**
- Natural period T0
- Resonant frequency f0

---

### Gate 2 — Damping and Stability

**Objective:** Measure damping and confirm stability across repeated runs.

**Procedure:**
1. Fit an exponential decay envelope to ringdown amplitude
2. Repeat across multiple runs and (if possible) different times of day

**Pass Criteria:**
- Quality factor Q stable within ±10% across runs
- No unexplained long-term drift in equilibrium angle (baseline)

**Outputs:**
- Q (and/or equivalent damping parameterization)
- Stability notes (baseline drift rate, if any)

---

### Gate 3 — Optical Readout Noise Floor

**Objective:** Establish the angular readout noise floor and identify dominant noise sources.

**Procedure:**
1. Record ≥ 2 hours with the pendulum at rest (minimum)
2. Compute PSD (same method you will use later in analysis)
3. Repeat overnight when feasible (recommended)

**Pass Criteria:**
- No ADC clipping or rail saturation
- Noise level consistent with expected optical/electronic limits (order-of-magnitude)
- No unexplained narrowband lines near:
  - the mechanical resonance region (around f0), or
  - known environmental lines (mains, mechanical vibrations)

**Outputs:**
- Angular noise density estimate (and/or PSD plot)
- Usable bandwidth estimate

---

### Gate 4 — Torque Calibration Response

**Objective:** Validate applied calibration torque → angular response mapping.

**Procedure:**
1. Apply calibration torque pulses (via coil) at fixed settings
2. Measure peak deflection and relaxation response
3. Repeat for multiple pulse amplitudes and both polarities if supported

**Pass Criteria:**
- Response is repeatable (pulse-to-pulse consistency)
- Linear scaling across the tested range (within expected tolerance)
- No hysteresis or sign-dependent behavior beyond noise

**Outputs:**
- Torque-to-angle calibration constant (effective)
- Verified “linear regime” bounds

---

### Gate 4A — Calibration Pulse Integrity (Firmware/DAQ sanity)

**Objective:** Ensure calibration pulses are visible, non-destructive, and do not corrupt logging.

**Procedure:**
1. Trigger calibration pulses during a short logging run
2. Confirm the readout shows a transient response
3. Confirm no clipping, timestamp jumps, or serial dropouts during the pulse window

**Pass Criteria:**
- Calibration transient is visible above noise
- No ADC clipping during pulses
- CSV stream remains well-formed (no missing fields, no stalls)

**Outputs:**
- Example raw CSV segment showing pulse response
- Notes on pulse settings used

---

### Tier 1 GO / NO-GO Decision

**GO if and only if:**
- Gates 1–4 (and 4A) pass
- Calibration is repeatable and internally consistent
- No unexplained dominant spectral features remain

Failure at any gate requires investigation and repeat testing.

---

## Tier 2 Validation — Spinner Upgrade (Conditional)

Tier 2 applies **only after Tier 1 is certified**.

> Note: The Tier-1 firmware output is `Time_ms,Theta_ADC,Status` and does not include encoder/step logging.  
> Tier-2 rotation validation therefore focuses on **stability, coupling suppression, and correlation tests**.  
> If encoder-grade phase tracking is required, it must be added as an explicit Tier-2 hardware upgrade.

### Gate 5 — Rotation Stability (Open-loop)

**Objective:** Verify rotation is stable enough to define a modulation timescale and does not drift catastrophically.

**Procedure:**
1. Run the rotation stage continuously for ≥ 24 hours
2. Log any stalls, missed steps (audible/visual markers), and temperature
3. If available, use an external timing reference (phone video + marker, optical interrupter, or encoder)

**Pass Criteria:**
- No stalls or thermal shutdown over 24 hours
- Rotation rate remains stable within ±0.1% over 24 hours **or** bounded by an external measurement method
- No significant change in mechanical noise floor while rotating

**Outputs:**
- Rotation settings (f_spin target)
- Stability evidence (external measurement or documented checks)

---

### Gate 6 — Mechanical Decoupling

**Objective:** Ensure rotation does not mechanically drive the pendulum.

**Procedure:**
1. Compare PSD with rotation OFF vs ON (same measurement duration)
2. Check for correlations between motor operation and angular motion

**Pass Criteria:**
- No new lines near f0
- No significant broadband noise increase when rotation is enabled
- No clear correlation between motor activity and readout

---

### Gate 7 — Electromagnetic and Thermal Coupling

**Objective:** Exclude non-inertial couplings (EM/thermal) as a source of coherent signatures.

**Procedure:**
- Vary motor current / driver settings
- Run electronics powered with rotation disabled
- Monitor temperature near pendulum and electronics
- Repeat PSD comparison across conditions

**Pass Criteria:**
- No angular response correlated with motor current draw
- No temperature-correlated drift that mimics target-band structure
- No electronic cross-talk signatures

---

## Validation Versioning and Traceability

Each validation run must record:
- **Run ID:** `YYYYMMDD-TIER-GATE-VERSION` (example: `20251218-T1-G3-v1`)
- SHA256 hash of raw data files
- Firmware git commit hash (or release tag if frozen)
- Analysis code git commit hash (or release tag if frozen)
- Configuration notes (hardware, settings, environment)

This ensures exact reproducibility.

---

## Failure Handling

If a validation gate fails:
- Stop progression immediately
- Identify likely coupling or instability source
- Modify hardware/configuration as needed
- Re-run all affected gates

A failed gate is **not** evidence of new physics.

---

## Relationship to Analysis

Validation certifies that:
- Hardware behavior is understood
- Noise sources are bounded
- Analysis assumptions are justified

Signal extraction and null tests occur only **after validation** and are defined in `/docs/analysis.md`.

---

## Summary

This protocol exists to protect the integrity of the experiment.

**Passing validation does not imply detection.**  
It only establishes that the apparatus behaves as expected.

Proceed slowly. Validate everything. Trust nothing without a gate.
