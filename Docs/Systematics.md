# Systematics — Known Couplings, Exclusions, and False-Positive Controls

This document identifies **known systematic couplings**, outlines **explicit exclusions**, and explains why false positives are unlikely in the AIRM Spinner experiment.

The purpose of this document is not to argue for the existence of anisotropic inertia, but to demonstrate that any recovered signal must survive a well-defined set of physical, instrumental, and analytical challenges.

---

## 1. Philosophy of Systematics Control

The experiment is designed under the following principles:

- No signal is trusted unless it can be falsified
- All plausible couplings are assumed guilty until excluded
- Systematics are addressed structurally, not statistically
- Absence of evidence must be demonstrable, not assumed

Systematics are handled through **design separation**, **frequency discrimination**, **phase coherence requirements**, and **null tests**.

---

## 2. Mechanical Systematics

### 2.1 Seismic and Vibrational Coupling

**Source:**
- Building vibration
- Foot traffic
- HVAC systems
- Ground motion

**Mitigation:**
- High-Q torsion pendulum acts as a mechanical low-pass filter
- Target signal lies well below dominant seismic frequencies
- No mechanical drive at sidereal frequency
- Baseline (no-spinner) runs establish vibrational noise floor

**Exclusion Logic:**
- Vibrational noise produces broadband or stochastic motion
- Cannot generate narrowband, phase-coherent sidebands
- Signal must disappear when rotation is disabled

---

### 2.2 Fiber Nonlinearity and Creep

**Source:**
- Torsion fiber aging
- Stress relaxation
- Temperature-dependent stiffness

**Mitigation:**
- Small-angle operation (linear regime)
- Long integration times average out slow drifts
- Calibration pulses verify linear response

**Exclusion Logic:**
- Fiber creep produces monotonic or very low-frequency drift
- Cannot lock phase to f_spin ± f_sid
- Appears identically in baseline and spinner-disabled runs

---

## 3. Magnetic Systematics

### 3.1 Ambient Magnetic Fields

**Source:**
- Earth’s magnetic field
- Nearby electronics
- Power-line harmonics

**Mitigation:**
- Minimal ferromagnetic material in pendulum
- Fixed laboratory orientation
- Static background fields produce static torques only

**Exclusion Logic:**
- Static fields do not produce time-varying sidebands
- Environmental magnetic noise is incoherent with f_spin
- Signal phase must track apparatus rotation, not lab frame

---

### 3.2 Calibration Coil Leakage

**Source:**
- Residual current leakage
- Ground loops
- PWM harmonics

**Mitigation:**
- Calibration coil normally inactive
- Calibration pulses explicitly logged
- Logic-level MOSFET ensures clean switching

**Exclusion Logic:**
- Signals must vanish when calibration disabled
- Timing of calibration pulses is known and removable
- Any persistent signal after removal invalidates the dataset

---

## 4. Thermal Systematics

### 4.1 Temperature Drift

**Source:**
- Room temperature variation
- Electronics self-heating

**Mitigation:**
- Low power dissipation
- Slow thermal time constants
- Long integration windows

**Exclusion Logic:**
- Thermal drift is slow and broadband
- Cannot phase-lock to sidereal frequency
- Appears in baseline runs

---

### 4.2 Radiative Heating from Laser

**Source:**
- Optical lever laser

**Mitigation:**
- Low-power (5 mW) laser
- Constant illumination
- No modulation at target frequencies

**Exclusion Logic:**
- Constant heating produces static offset
- No mechanism for frequency sidebands
- Verified by laser-on / laser-off tests

---

## 5. Electrical and Readout Systematics

### 5.1 ADC Noise and Quantization

**Source:**
- ADC quantization (10-bit)
- Reference voltage noise

**Mitigation:**
- Oversampling through long integration
- Noise floor characterized in baseline runs

**Exclusion Logic:**
- ADC noise is white or broadband
- Cannot produce narrowband coherent signals
- Independent of rotation state

---

### 5.2 Clock and Timing Drift

**Source:**
- Microcontroller clock instability

**Mitigation:**
- Timestamped data logging
- Long averaging times
- Frequency-domain analysis tolerant to small drift

**Exclusion Logic:**
- Clock drift shifts frequency, not phase coherence
- Falsification via incorrect demodulation frequency
- Signal collapses when reference frequency offset

---

## 6. Rotation-Induced Artifacts

### 6.1 Mechanical Imbalance

**Source:**
- Imperfect mass symmetry
- Bearing friction

**Mitigation:**
- Very slow rotation (millihertz scale)
- Mechanical decoupling of rotation stage from pendulum

**Exclusion Logic:**
- Imbalance produces signal at f_spin
- AIRM signature appears at f_spin ± f_sid
- Sideband separation is key discriminator

---

### 6.2 Control Electronics Crosstalk

**Source:**
- Stepper motor EMI
- Power supply coupling

**Mitigation:**
- Stepper operates at extremely low step rate
- No high-frequency switching near resonance
- Separate supply rails where practical

**Exclusion Logic:**
- EMI correlates with step timing
- Does not track sidereal phase
- Identified by step-correlated artifacts

---

## 7. Analysis-Induced False Positives

### 7.1 Overfitting and Look-Elsewhere Effects

**Mitigation:**
- Predefined target frequencies
- No post-hoc frequency scanning
- Fixed analysis pipeline

**Exclusion Logic:**
- Signals must appear at predicted frequencies only
- Off-frequency projections must return null
- Null tests explicitly included

---

### 7.2 Demodulation Bias

**Mitigation:**
- Quadrature demodulation
- Phase-agnostic amplitude recovery
- Independent sine and cosine projections

**Exclusion Logic:**
- Incorrect demodulation frequency destroys coherence
- Phase scrambling removes signal
- Demonstrated via falsification tests

---

## 8. Baseline and Null Experiments

The following runs are mandatory:

- No-spinner (static orientation)
- Calibration-disabled
- Wrong-frequency demodulation
- Phase-scrambled analysis

A signal present in any null configuration is rejected.

---

## 9. Why False Positives Are Unlikely

A false positive would require a disturbance that:

- Is mechanically transmitted
- Is magnetically invisible
- Is thermally silent
- Is electrically coherent
- Locks phase to sidereal time
- Produces symmetric sidebands
- Disappears under null tests
- Reappears only under correct configuration

No known environmental or instrumental process satisfies all of these simultaneously.

---

## 10. Scope and Limitations

This document does not claim:

- Elimination of all conceivable systematics
- Detection of new physics
- Immunity to unknown couplings

It does demonstrate that **any surviving signal is highly constrained** and must be taken seriously as an experimental observation.

---

## Status

- Systematics identified: Yes
- Mitigations implemented: Yes
- Null tests defined: Yes
- Falsification logic explicit: Yes

---

> **Principle:**  
> *Extraordinary claims are not avoided by boldness, but by eliminating ordinary explanations one by one.*
