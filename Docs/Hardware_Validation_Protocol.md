# Hardware Validation Protocol v1.0 — Inertia Rebellion Apparatus (AIRM)

This document defines the mandatory hardware validation gates for the Inertia Rebellion torsion-balance experiment.

Validation is required to:

- Establish calibration constants  
- Exclude common false positives  
- Prevent premature interpretation  
- Ensure reproducibility and auditability  

No sidereal searches, no detection claims, and no Tier‑2 spinner interpretation are permitted until all applicable validation gates are passed.

---

## Validation Philosophy

AIRM follows a gated experimental protocol consistent with best practices in precision measurement.

Principles:

- Every hardware change introduces new couplings  
- Couplings must be bounded before interpretation  
- Validation precedes analysis (never the reverse)  
- A failed gate is a NO‑GO, not an anomaly  

Passing validation establishes instrument credibility, not physical conclusions.

---

## Tier‑1 Validation — Static Pendulum (Required)

Tier‑1 establishes baseline torsion‑pendulum behavior without spinner‑enabled searches.

---

### Gate 1 — Free Oscillation Characterization

**Objective**  
Verify that the pendulum behaves as a linear harmonic oscillator within its working range.

**Procedure**

1. Displace pendulum by a small angle (recommended: ≤ 5 mrad peak).  
2. Release without external forcing.  
3. Record angular readout for ≥ 10 oscillation periods.  
4. Estimate the fundamental frequency using a consistent method  
   (e.g., sinusoidal fit, zero‑crossings, or Hilbert phase).

**Pass criteria**

- ≥ 10 visible oscillation cycles with SNR > 10.  
- Single dominant spectral peak at the fundamental.  
- Harmonic distortion bounded:  
  - second harmonic amplitude < 1% of the fundamental.  
- No measurable amplitude‑dependent frequency shift:  
  - Δf / f₀ < 0.1% when comparing ≥ 50% change in initial amplitude.

**Outputs**

- Natural period T₀.  
- Resonant frequency f₀.  
- Method used to estimate f₀.

---

### Gate 2 — Damping and Stability

**Objective**  
Measure damping and confirm stability across repeated runs.

**Procedure**

1. Fit an exponential decay envelope to the free‑oscillation ringdown.  
2. Repeat measurements across multiple runs and, if possible, different times of day.

**Pass criteria**

- Quality factor Q stable within ±10% across runs.  
- No unexplained long‑term drift in equilibrium angle.

**Outputs**

- Q (or equivalent damping parameter).  
- Baseline drift rate estimate (if any).

---

### Gate 3 — Optical Readout Noise Floor

**Objective**  
Establish the angular readout noise floor and identify dominant noise sources.

**Procedure**

1. Record ≥ 2 hours of data with the pendulum at rest.  
2. Compute the PSD using the same method intended for later analysis.  
3. Repeat overnight when feasible (recommended).

**Pass criteria**

- No ADC clipping or rail saturation.  
- Noise level consistent with expected optical/electronic limits (order‑of‑magnitude).  
- No unexplained narrowband lines  
  - near the mechanical resonance (around f₀), or  
  - at known environmental frequencies (mains, mechanical vibrations).  
- Integrated RMS in the analysis band is stable across repeated runs.

**Outputs**

- Angular noise density estimate or PSD plot.  
- Usable bandwidth estimate.

---

### Gate 4 — Torque Calibration Response

**Objective**  
Validate applied calibration torque → angular response mapping.

**Procedure**

1. Apply calibration torque pulses at fixed settings.  
2. Measure peak deflection and relaxation response.  
3. Repeat across multiple pulse amplitudes and polarities (if supported).

**Pass criteria**

- Pulse‑to‑pulse repeatability.  
- Linear scaling across the tested range:  
  - deviations ≤ 5% or linear fit R² ≥ 0.98.  
- No hysteresis or polarity‑dependent behavior beyond noise.

**Outputs**

- Effective torque‑to‑angle calibration constant.  
- Verified linear‑regime bounds.

---

### Gate 5 — Calibration Pulse & DAQ Integrity

**Objective**  
Ensure calibration pulses are visible, non‑destructive, and do not corrupt data logging.

**Procedure**

1. Trigger calibration pulses during a short logging run.  
2. Confirm visible transient response in angular readout.  
3. Inspect raw data stream for integrity.

**Pass criteria**

- Calibration transient visible above noise.  
- No ADC clipping during pulses.  
- Data stream remains well‑formed:  
  - no missing samples,  
  - no timestamp discontinuities,  
  - no serial dropouts.

**Outputs**

- Example raw CSV segment showing pulse response.  
- Pulse parameters used.

---

## Tier‑1 GO / NO‑GO Decision

**GO** if and only if:

- Gates 1–5 pass.  
- Calibration is repeatable and internally consistent.  
- No unexplained dominant spectral features remain.

Failure at any gate requires investigation and repeat testing.

---

## Tier‑2 Validation — Spinner Upgrade (Conditional)

Tier‑2 applies only after Tier‑1 certification.

Note: Tier‑1 firmware outputs `Time_ms,Theta_ADC,Status` only. Encoder‑grade phase tracking is not assumed. Any encoder upgrade constitutes a separate Tier‑2 hardware change that must be re‑validated through the relevant gates.

---

### Gate 6 — Rotation Stability (Open‑Loop)

**Objective**  
Verify rotation is stable enough to define a modulation timescale and does not introduce gross instability.

**Procedure**

1. Run rotation continuously for ≥ 24 hours.  
2. Log stalls, missed steps, temperature, and audible/visual anomalies.  
3. If available, bound rotation rate using an external reference  
   (phone video, optical marker, interrupter, or encoder).

**Pass criteria**

- No stalls or thermal shutdowns over 24 hours.  
- Rotation rate bounded by an external method and documented.  
- Mechanical noise floor does not increase catastrophically during rotation.

**Outputs**

- Target f_spin and driver settings.  
- Evidence or documentation of rate stability.

---

### Gate 7 — Mechanical Decoupling

**Objective**  
Ensure rotation does not mechanically drive the pendulum.

**Procedure**

1. Compare PSD with rotation OFF vs ON.  
2. Look for correlations between motor activity and angular motion.

**Pass criteria**

- No new spectral lines near f₀.  
- No significant broadband noise increase when rotation is enabled.  
- No time‑correlated signatures with motor operation.

**Outputs**

- PSD comparison plots (OFF vs ON).  
- Notes on any observed couplings.

---

### Gate 8 — Electromagnetic & Thermal Coupling

**Objective**  
Exclude non‑inertial couplings as a source of coherent signatures.

**Procedure**

- Vary motor current and driver settings.  
- Power electronics with rotation disabled.  
- Monitor temperatures near pendulum and electronics.  
- Repeat PSD comparisons across conditions.

**Pass criteria**

- No angular response correlated with motor current.  
- No temperature‑correlated drift mimicking target‑band structure.  
- No electronic cross‑talk signatures.

**Outputs**

- PSD and trend plots across conditions.  
- Summary of EM/thermal coupling limits.

---

## Validation Versioning & Traceability

Each validation run must record:

- Run ID: `YYYYMMDD-TIER-GATE-VERSION`.  
- SHA‑256 hash of raw data files.  
- Firmware git commit or release tag.  
- Analysis code git commit or release tag.  
- Configuration notes (hardware, environment, settings).

Raw data and derived outputs should be stored together for auditability.

---

## Failure Handling

If a validation gate fails:

1. Stop progression immediately.  
2. Identify likely coupling or instability.  
3. Modify hardware or configuration.  
4. Re‑run all affected gates.

A failed gate is not evidence of new physics.

---

## Relationship to Analysis

Validation certifies that:

- Hardware behavior is understood.  
- Noise sources are bounded.  
- Analysis assumptions are justified.

Signal extraction, null tests, and falsification occur only after validation and are defined in `/simulation/`.

---

## Tier Summary

| Tier | Gates | Required for            |
|------|-------|-------------------------|
| 1    | 1–5   | Baseline pendulum use  |
| 2    | 6–8   | Spinner modulation use |

---

## Summary

This protocol exists to protect experimental integrity.

Passing validation does not imply detection.  
It only establishes that the apparatus behaves as expected.

Proceed slowly. Validate everything. Trust nothing without a gate.
