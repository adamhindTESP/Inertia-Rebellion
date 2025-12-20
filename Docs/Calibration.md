# Calibration — Torque Injection & Validation Logic

This document defines the **calibration philosophy, torque model, and validation logic** for the AIRM Spinner torsion-balance experiment.

Calibration is treated as a **controlled, injected disturbance** used to:
- Validate mechanical response
- Verify readout sensitivity
- Establish absolute and relative scale
- Guard against false positives

Calibration does **not** assume or imply the presence of anisotropic inertia or any new physics.

---

## 1. Purpose of Calibration

The calibration system exists to answer three questions unambiguously:

1. Does the torsion pendulum respond as expected to a known applied torque?
2. Is the optical lever readout linear and stable over the operating range?
3. Can injected signals be distinguished from background noise using the same analysis pipeline?

A signal that cannot be reproduced, scaled, or falsified using calibration injections is **not considered credible**.

---

## 2. Calibration Philosophy

The calibration approach is deliberately conservative:

- Calibration torques are **externally applied**
- Injection times are **explicitly logged**
- No calibration correction is applied in firmware
- All calibration analysis is performed offline

This ensures:
- Full transparency
- Reproducibility
- Independent reanalysis by third parties

Calibration does not “tune” the experiment; it **tests it**.

---

## 3. Magnetic Torque Injection System

### 3.1 Physical Implementation

Calibration torque is generated using:

- A fixed solenoidal magnetic coil
- A small permanent magnet attached to the torsion pendulum
- A logic-level MOSFET driven by the microcontroller

When energized, the coil produces a magnetic field that exerts a torque on the pendulum-mounted magnet.

---

### 3.2 Coil Geometry (Typical)

- Coil type: Solenoid
- Length: ~3 cm
- Diameter: ~2 cm
- Turns: ~500
- Wire: 28 AWG magnet wire
- Resistance: ~5 Ω
- Inductance: ~10 mH

These values are **order-of-magnitude**, not precision parameters.

Exact torque calibration is performed empirically.

---

## 4. Torque Model (Order-of-Magnitude)

The applied magnetic torque is modeled as:

τ(t) ≈ m × B(t)

Where:

- τ(t) is the applied torque
- m is the magnetic dipole moment of the pendulum-mounted magnet
- B(t) is the magnetic field produced by the calibration coil

For a solenoid, the on-axis field is approximately:

B ≈ μ₀ · N · I / L

Where:

- μ₀ is the permeability of free space
- N is the number of turns
- I is the coil current
- L is the coil length

Using typical values:

- I ≈ 1 A
- N ≈ 500
- L ≈ 0.03 m

Gives:

B ≈ 10–30 mT (order of magnitude)

With a small NdFeB magnet (m ≈ 0.01–0.1 A·m²), the resulting torque is:

τ ≈ 10⁻⁷ to 10⁻⁶ N·m

This estimate is used **only** to size the system and ensure measurable deflection.

Absolute torque calibration is derived from the pendulum response, not from this model.

---

## 5. Calibration Pulse Definition

### 5.1 Pulse Shape

A calibration injection consists of:

- A square current pulse
- Fixed duration (typically ~100 ms)
- Fixed duty cycle (typically 50%)

The exact waveform is not critical, provided it is:
- Repeatable
- Logged
- Clearly separable from background motion

---

### 5.2 Logging Requirements

Calibration pulses are **not explicitly flagged** in the firmware data stream.

Instead, calibration timing is inferred during analysis using:
- Known serial command timestamps
- The characteristic transient angular response of the pendulum

This design choice ensures:
- Minimal firmware complexity
- Raw-data primacy
- Independent verification by third parties

Calibration windows may be excluded or analyzed explicitly during offline processing.

---

## 6. Mechanical Response Validation

### 6.1 Expected Response

A valid calibration injection produces:

- A transient angular deflection θ(t)
- Followed by free oscillation at the natural torsional frequency
- With decay governed by the quality factor Q

Key observables:

- Peak deflection amplitude
- Ringdown frequency
- Ringdown decay time

These must be consistent across repeated injections.

---

### 6.2 Linearity Check

Calibration pulses of different amplitudes should satisfy:

- θ_max ∝ τ (within linear regime)
- No hysteresis or memory effects
- No dependence on sign of applied torque (except phase)

Departure from linearity indicates:
- Mechanical nonlinearity
- Magnetic coupling issues
- Readout saturation

---

## 7. Optical Lever Calibration

Calibration injections are used to convert ADC units into angular displacement.

Procedure:

1. Apply known calibration pulse
2. Measure peak ADC response ΔADC
3. Infer angular displacement using torsion dynamics
4. Compute scale factor:

Angular sensitivity ≈ ΔADC / Δθ

This factor is geometry-dependent and must be measured, not assumed.

No scaling is applied in firmware.

---

## 8. Validation Logic & Falsification

### 8.1 Validation Criteria

A calibration system is considered valid if:

- Injected pulses are always detectable above noise
- Response timing matches injection timing
- Amplitude scaling is stable over time
- Removing calibration pulses removes the signal

---

### 8.2 Falsification Tests

Calibration enables direct falsification:

- Disable coil → signal must disappear
- Shift analysis window → coherence must collapse
- Reverse pulse polarity → phase must invert
- Change pulse timing → response must follow

Any signal that survives these tests is suspect.

---

## 9. Relationship to Anisotropy Search

Calibration torques differ fundamentally from the AIRM signal:

- Calibration is impulsive and broadband
- AIRM modulation is continuous and narrowband
- Calibration is injected intentionally
- AIRM signal must be recovered blindly

The same analysis pipeline is applied to both.

Calibration establishes **what the instrument can see**, not **what it should see**.

---

## 10. Design Guarantees

- Calibration torques are external and explicit
- All injections are logged
- No hidden corrections exist
- All calibration effects are reversible in software
- Any change to calibration parameters requires version update

---

## Status

- Calibration hardware: Implemented
- Firmware control: Implemented
- Logging: Implemented
- Analysis: Offline, reproducible

Calibration is **not optional**.

If a signal cannot be calibrated, it cannot be trusted.

---

> **Principle:**  
> *Calibration does not prove new physics — it proves your instrument deserves to look.*
