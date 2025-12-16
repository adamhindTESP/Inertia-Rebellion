# Hardware Validation Protocol — Inertia Rebellion Apparatus

This document defines the **mandatory hardware validation gates** for the Inertia Rebellion torsion-balance experiment.

Validation is required to:
- Establish calibration constants
- Exclude common false positives
- Prevent premature interpretation of data
- Ensure reproducibility and auditability

**No experimental claims, sidereal searches, or spinner upgrades are permitted until all applicable validation gates are passed.**

---

## Validation Philosophy

The Inertia Rebellion apparatus follows a **gated experimental protocol** inspired by best practices in precision measurement and gravitational physics.

Key principles:

- Every hardware upgrade introduces new couplings
- All couplings must be characterized before interpretation
- Validation precedes analysis, not the reverse
- Failure to validate is treated as a **NO-GO**, not an anomaly

---

## Tier 1 Validation — Static Pendulum (Required)

Tier 1 establishes the baseline physical behavior of the torsion pendulum.

### Gate 1 — Free Oscillation Characterization

**Objective:**  
Verify that the torsion pendulum behaves as a linear harmonic oscillator.

**Procedure:**
1. Displace pendulum by a small angle (< 5 mrad)
2. Release without external forcing
3. Record angular displacement over ≥ 10 oscillation periods

**Pass Criteria:**
- ≥ 10 oscillation cycles visible with **signal-to-noise ratio > 10**
- Single dominant frequency with **second harmonic < 1% of fundamental**
- No measurable amplitude-dependent frequency shift:
  - \( \Delta f / f_0 < 0.1\% \) over a ≥ 50% amplitude range

**Outputs:**
- Natural period \( T_0 \)
- Resonant frequency \( f_0 \)

---

### Gate 2 — Damping and Stability

**Objective:**  
Measure damping and confirm long-term stability.

**Procedure:**
1. Fit exponential decay envelope to oscillation amplitude
2. Repeat measurement over multiple runs and times of day

**Pass Criteria:**
- Consistent decay constant across runs
- Quality factor \( Q \) stable within ±10%
- No unexplained drift in equilibrium angle

**Outputs:**
- Damping coefficient \( \gamma \)
- Quality factor \( Q \)

---

### Gate 3 — Optical Readout Noise Floor

**Objective:**  
Establish the angular noise floor of the readout system.

**Procedure:**
1. Record ≥ 2 hours of data with pendulum at rest
2. Compute power spectral density (PSD)

**Pass Criteria:**
- Noise consistent with expected optical + electronic limits
- No persistent narrowband lines near the sidereal frequency
- No unexplained low-frequency excess

**Outputs:**
- Angular noise density
- Verified usable bandwidth

---

### Gate 4 — Torque Calibration Response

**Objective:**  
Validate applied torque → angular response mapping.

**Procedure:**
1. Apply known calibration torque pulses
2. Measure angular deflection and relaxation
3. Repeat for multiple amplitudes

**Pass Criteria:**
- Linear response within expected range
- Repeatable calibration constant
- No hysteresis or sign-dependent response

**Outputs:**
- Torque-to-angle calibration constant
- Verification of linear regime

---

### Tier 1 GO / NO-GO Decision

**GO if and only if:**
- All four Tier 1 gates pass
- No unexplained spectral features remain
- Calibration constants are internally consistent

Failure at any gate requires investigation and repeat testing.

---

## Tier 2 Validation — Spinner Upgrade (Conditional)

Tier 2 validation applies **only after Tier 1 is fully certified**.

### Gate 5 — Rotation Stability

**Objective:**  
Verify stable and phase-controllable rotation.

**Procedure:**
1. Run rotation stage continuously for ≥ 24 hours
2. Record step count or encoder data

**Pass Criteria:**
- Rotation frequency stable within **±0.1% over 24 hours**
- Step or encoder jitter < **1 part in 10⁴**
- Cumulative phase error < **10° after 24 hours**

---

### Gate 6 — Mechanical Decoupling

**Objective:**  
Ensure rotation does not mechanically drive the pendulum.

**Procedure:**
1. Rotate with pendulum mechanically isolated
2. Compare PSD with and without rotation enabled

**Pass Criteria:**
- No new spectral lines near \( f_0 \)
- No broadband noise increase
- No correlation between motor steps and angular motion

---

### Gate 7 — Electromagnetic and Thermal Coupling

**Objective:**  
Exclude non-gravitational coupling mechanisms.

**Procedure:**
- Vary motor current
- Disable rotation while electronics remain powered
- Monitor temperature near pendulum

**Pass Criteria:**
- No angular response correlated with current draw
- No temperature-correlated drift
- No electronic cross-talk signatures

---

## Validation Versioning

Each completed validation run receives:

- **Run ID:** `YYYYMMDD-TIER-GATE-VERSION`  
  - Example: `20251216-T1-G1-v2`
- **SHA256 hash** of all raw data files
- **Firmware git commit hash**
- **Analysis code git commit hash**

This ensures exact reproducibility and traceability.

---

## Documentation Requirements

For each validation gate, the following must be archived:

- Raw data files
- Timestamped configuration notes
- Firmware version identifier
- Environmental conditions (approximate)

Validation results must be recorded before proceeding.

---

## Failure Handling

If a validation gate fails:

- Stop progression immediately
- Identify coupling or instability source
- Modify hardware or configuration
- Re-run full affected gate sequence

A failed gate is **not** evidence of new physics.

---

## Relationship to Analysis

Validation certifies that:
- Hardware behavior is understood
- Noise sources are bounded
- Analysis assumptions are justified

All signal extraction and null tests are performed **after** validation
and are defined in `/docs/analysis.md`.

---

## Summary

This validation protocol exists to protect the integrity of the experiment.

**Passing validation does not imply detection.**  
It only establishes that the apparatus is behaving as expected.

Only after validation may higher-level searches be conducted.

Proceed slowly.  
Validate everything.  
Trust nothing without a gate.
