# Firmware — AIRM Spinner Control & Data Logging

This document describes the **firmware architecture, scope, and guarantees** used to operate the AIRM Spinner torsion-balance apparatus.

The firmware is intentionally minimal.  
Its role is **deterministic I/O control and transparent data logging**, not signal interpretation.

All physics analysis is performed offline.

---

## 1. Firmware Role in the Experiment

The firmware performs four essential tasks:

1. **Impose controlled rotation** at a known modulation frequency (f_spin)
2. **Read angular displacement** from the optical lever
3. **Inject calibration torques** on command
4. **Log raw data** continuously for offline analysis

The firmware explicitly does **not**:

- Filter data
- Demodulate signals
- Estimate frequencies
- Perform statistical tests
- Make GO / NO-GO decisions

The firmware may perform **minimal sanity checks only**, such as:
- ADC range clamping
- Counter overflow handling
- Basic fault flags

It never transforms or enhances the physics signal beyond **digitization, timestamping, and framing**.

This separation ensures:
- Full auditability
- Reversible data processing
- No hidden signal conditioning
- Independent reanalysis by third parties

---

## 2. Hardware Assumptions & Versioning

The firmware assumes the following hardware, which is part of the **experimental definition**:

- MCU: Arduino Uno or Nano (ATmega328P)
- Logic level: 5 V
- ADC resolution: 10-bit
- External 12 V supply for motor and calibration coil

Any port to a different MCU, voltage rail, or timing source **must be treated as a new firmware version** and documented alongside the data.

---

## 3. Rotation Control

### 3.1 Rotation Strategy

Rotation is implemented using:

- Open-loop stepper control
- Fixed step interval scheduling
- No encoder or closed-loop feedback

The goal is not precise angular positioning, but **stable, slow, repeatable modulation**.

---

### 3.2 Typical Configuration (Parameterizable)

Typical default configuration (set via firmware constants):

- Motor: 200 steps per revolution
- Microstepping: Full-step (configurable)
- Step interval: 1 step per second (configurable)
- Effective rotation frequency:  
  f_spin ≈ 0.001 Hz (default)

Only the **parameters** are adjustable; the **conceptual approach** (slow, open-loop modulation) is fixed.

---

### 3.3 Timing Model

Stepper timing is driven by:

- `millis()`-based scheduling
- Deterministic main loop execution

This timing model is sufficient to:
- Establish a known modulation timescale
- Enable offline phase tracking

It is **not** intended to provide ppm-level frequency stability or clock discipline.

---

## 4. Optical Lever Readout

### 4.1 ADC Sampling

- Signal source: Photodiode voltage divider
- ADC reference: Arduino 5 V rail
- ADC resolution: 10-bit (0–1023)
- Sampling rate: 1 Hz (default)

Each sample is tagged with a **millisecond-resolution timestamp** using `millis()`.

No attempt is made to:
- Discipline the clock
- Correct drift
- Apply filtering or gain correction

---

### 4.2 Signal Characteristics

Typical operating behavior after alignment:

- Resting midpoint: ~512 ADC counts
- Dynamic range: ±100 counts (geometry-dependent)

The firmware does not:
- Zero the signal
- Track baseline drift
- Normalize or scale readings

Calibration is performed via injected torque and handled offline.

---

## 5. Magnetic Calibration Control

### 5.1 Purpose

The magnetic calibration coil provides:

- Known, repeatable torque impulses
- Validation of mechanical response
- A safeguard against false positives

Every credible signal must be interpretable relative to injected calibration behavior.

---

### 5.2 Control Method

- Output: PWM-capable digital pin
- Driver: Logic-level MOSFET
- Pulse duration: ~100 ms (typical)
- Duty cycle: Configurable

Calibration pulses may be issued manually via serial command.

---

### 5.3 Data Alignment

Each calibration pulse is logged with:

- A timestamp
- A calibration flag in the data stream

This allows injected torques to be aligned precisely with the optical-lever response during offline analysis.

---

## 6. Serial Data Logging

### 6.1 Output Format

The firmware outputs **one CSV line per sample** over USB serial.

Default field order:

timestamp_ms, adc_raw, step_count, cal_flag

Field definitions:

- `timestamp_ms`  
  Unsigned 32-bit integer, milliseconds since MCU reset

- `adc_raw`  
  Raw ADC count (0–1023)

- `step_count`  
  Cumulative motor step index (wraparound permitted)

- `cal_flag`  
  0 = normal sample  
  1 = within calibration pulse window

By default:
- No header row is emitted
- Output is ASCII CSV
- One line corresponds to one sample

This format is human-readable, script-friendly, and robust against dropped lines.

---

### 6.2 Sampling Philosophy

A 1 Hz logging rate was chosen to:

- Match simulation assumptions
- Minimize serial bottlenecks
- Avoid implicit filtering

Higher sampling rates are possible but not required for the current analysis pipeline.

---

## 7. Command Interface

The firmware supports a minimal serial command set:

| Command | Action |
|-------|--------|
| `C` | Inject calibration torque pulse |
| `S` | Report system status |

Commands are optional, non-blocking, and logged.

No command modifies:
- Rotation frequency
- ADC scaling
- Logging format

This preserves experiment repeatability.

---

## 8. Error Handling & Known Limitations

The firmware:

- Does not detect missed motor steps
- Does not measure coil current
- Does not provide absolute time synchronization

These limitations are intentional and documented.

Failures are designed to be **visible in the data**, not silently corrected.

---

## 9. Relation to Other Project Components

- Hardware design → `docs/hardware.md`
- Calibration logic → `docs/calibration.md`
- Simulation assumptions → `simulation/`
- Data analysis → `analysis/`

Firmware behavior is explicitly aligned with simulation parameters (sampling rate, modulation timescale).

---

## 10. Design Guarantees

- Firmware does not generate or enhance physics signals
- All transformations are reversible from the serial data log
- Any change to timing, motor control, or ADC behavior increments the firmware version and must be recorded with the data

---

## Status

- Firmware: **Operational**
- Rotation control: **Validated**
- Data logging: **Validated**
- Calibration interface: **Validated**

No “smart” features are planned.

---

> **Design principle:**  
> *If the firmware looks boring, it is working correctly.*
