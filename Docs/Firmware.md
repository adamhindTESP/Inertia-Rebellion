# Firmware — AIRM Spinner Control & Data Logging (Tier-1)

This document describes the **authoritative Tier-1 firmware behavior**
used to operate the AIRM Spinner torsion-balance apparatus.

The firmware is intentionally minimal.
Its role is **deterministic I/O control and transparent data logging**, not signal interpretation.

All physics analysis is performed offline.

---

## 1. Firmware Role in the Experiment

The firmware performs four essential tasks:

1. Impose controlled rotation at a fixed modulation frequency (`f_spin`)
2. Read angular displacement from the optical lever
3. Inject calibration torques on command
4. Log raw data continuously for offline analysis

The firmware explicitly does **not**:

- Filter data
- Demodulate signals
- Estimate frequencies
- Apply calibration scaling
- Perform statistical tests
- Make GO / NO-GO decisions

This strict separation ensures:
- Full auditability
- Reversible data processing
- No hidden signal conditioning
- Independent reanalysis by third parties

---

## 2. Hardware Assumptions (Tier-1)

The firmware assumes the following hardware:

- MCU: Arduino Uno or Nano (ATmega328P)
- Logic level: 5 V
- ADC resolution: 10-bit
- External 12 V supply for stepper motor and calibration coil

Any change to MCU, voltage rails, or timing source **requires a new firmware version**.

---

## 3. Rotation Control

### 3.1 Strategy

Rotation is implemented using:

- Open-loop stepper motor control
- Fixed step rate
- No encoder or feedback

The goal is **slow, repeatable modulation**, not angular precision.

---

### 3.2 Fixed Tier-1 Parameters

- Motor: 200 steps per revolution
- Microstepping: Full step
- Step rate: **0.2 steps/s**
- Rotation period: 1000 s per revolution
- Effective modulation frequency:

f_spin = 0.001 Hz

These parameters are **hard-coded** in Tier-1 firmware.

---

### 3.3 Timing Model

Stepper timing is driven by:

- `millis()`-based scheduling
- Deterministic loop execution

The firmware does **not** attempt:
- Clock discipline
- ppm-level stability
- Absolute time synchronization

This is sufficient for sideband detection in offline analysis.

---

## 4. Optical Lever Readout

### 4.1 ADC Sampling

- Signal source: Photodiode voltage divider
- ADC reference: Arduino 5 V rail
- ADC resolution: 10-bit (0–1023)
- Sampling rate: **1 Hz**

Each sample is tagged with a millisecond timestamp (`millis()`).

No filtering, offset correction, or gain normalization is performed.

---

### 4.2 Signal Characteristics

Typical behavior after alignment:

- Resting midpoint: ~512 ADC counts
- Dynamic range: ±100 counts (geometry-dependent)

Calibration and scaling are handled offline.

---

## 5. Magnetic Calibration Control

### 5.1 Purpose

The magnetic coil provides:

- Known, repeatable torque impulses
- Mechanical response validation
- A falsification control channel

Calibration exists to validate the instrument — not to tune it.

---

### 5.2 Control Method

- Output: PWM-capable digital pin
- Driver: Logic-level MOSFET
- Pulse duration: ~100 ms (fixed)
- Duty cycle: Fixed in firmware

Calibration pulses are issued manually via serial command (`C`).

---

### 5.3 Data Alignment

Calibration pulses are **not explicitly flagged** in the data stream.

Injection timing is inferred during analysis using:
- Known command timing
- Characteristic angular response

This design preserves raw-data primacy and simplicity.

---

## 6. Serial Data Logging

### 6.1 Output Format (Authoritative)

The firmware outputs **one CSV line per sample**:

Time_ms,Theta_ADC,Status

**Field definitions:**

- `Time_ms` — milliseconds since MCU reset
- `Theta_ADC` — raw ADC value (0–1023)
- `Status` — always `"OK"` (reserved for future diagnostics)

No step count, calibration flag, or derived quantity is logged.

---

### 6.2 Sampling Philosophy

A 1 Hz logging rate was chosen to:

- Match simulation assumptions
- Minimize serial overhead
- Avoid implicit filtering

---

## 7. Command Interface

The Tier-1 firmware supports:

| Command | Action |
|-------|-------|
| `C` | Inject calibration torque pulse |

Commands are non-blocking and do not alter:
- Rotation frequency
- ADC scaling
- Logging format

---

## 8. Known Limitations

The firmware:

- Does not detect missed steps
- Does not measure coil current
- Does not provide absolute time sync

These limitations are intentional and visible in the data.

---

## 9. Alignment with Other Components

- Hardware → `hardware/`
- Calibration → `Docs/calibration.md`
- Analysis → `Docs/analysis.md`
- Simulation → `simulation/`

All parameters (sampling rate, modulation frequency) are consistent across components.

---

## 10. Design Guarantees

- Firmware does not generate or enhance physics signals
- All transformations are reversible
- Any behavioral change increments the firmware version and must be recorded

---

## Status

- Firmware: **Frozen (Tier-1)**
- Rotation control: **Validated**
- Data logging: **Validated**
- Calibration interface: **Validated**

---

> **Design principle:**  
> *If the firmware looks boring, it is working correctly.*
