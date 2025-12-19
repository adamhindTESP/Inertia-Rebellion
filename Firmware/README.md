# Firmware — AIRM Spinner Control & Data Logging

This document describes the firmware architecture, scope, and guarantees
used to operate the AIRM Spinner torsion-balance apparatus.

The firmware is intentionally minimal.
Its role is **deterministic I/O control and transparent data logging** —
not signal interpretation.

All physics analysis is performed offline.

---

## 1. Firmware Scope and Guarantees

The firmware is designed to:

- Control slow, deterministic rotation of the apparatus
- Read angular displacement from the optical lever
- Inject calibration torques on command
- Log raw, time-stamped data for offline analysis

The firmware explicitly does **not**:

- Filter data
- Demodulate signals
- Estimate frequencies
- Perform statistical analysis
- Make GO / NO-GO decisions

This separation guarantees auditability and reversibility.

---

## 2. Hardware Assumptions

The firmware assumes the following hardware configuration:

- MCU: Arduino Uno / Nano (ATmega328P)
- Logic level: 5 V
- ADC resolution: 10-bit (0–1023)
- External supply for motor and calibration coil

Any change to MCU, clock source, or voltage rail constitutes a **new firmware version**
and must be recorded alongside experimental data.

---

## 3. Timing Model

- All timing is derived from `millis()`
- No external clock discipline is used
- Long-term drift is accepted and handled offline

The firmware provides **deterministic timestamps**, not absolute time.

---

## 4. Rotation Control (Summary)

- Open-loop stepper motor control
- Fixed step scheduling
- No encoder or closed-loop feedback

The goal is **stable, slow modulation**, not precise angular positioning.

---

## 5. Calibration Interface (Summary)

- Magnetic calibration torque applied via PWM-driven coil
- Triggered manually over serial
- Used to validate mechanical response and pipeline integrity

---

## 6. Serial Data Logging

The firmware outputs raw, time-stamped measurements over USB serial
for offline analysis.

No filtering, demodulation, or signal conditioning is performed onboard.

---

### 6.1 Output Format

The firmware emits **one CSV line per sample** at a fixed rate.

**CSV header (emitted once at startup):**

Time_ms,Theta_ADC,Status

**Field definitions:**

- `Time_ms`  
  Milliseconds since MCU reset, obtained from `millis()`.

- `Theta_ADC`  
  Raw ADC reading from the optical-lever photodiode  
  (integer range: 0–1023).

- `Status`  
  ASCII status field. Currently always `"OK"` during normal operation.  
  Reserved for future fault or diagnostic flags.

**Example output:**

Time_ms,Theta_ADC,Status
12345,512,OK
13345,510,OK

The header is not required for parsing, but is emitted for human readability.

---

### 6.2 Sampling Rate

- Default logging rate: **1 Hz**
- Controlled via `log_interval = 1000 ms`

This rate is chosen to:

- Match numerical simulation assumptions
- Minimize serial bandwidth usage
- Avoid implicit filtering

Higher sampling rates are not required for Tier-1 validation.

---

### 6.3 Calibration Pulse Behavior

When the serial command:

C

is received:

- A brief magnetic calibration pulse is applied
- Pulse duration: ~100 ms
- Coil power: fixed PWM value

**Important:**  
Calibration pulses are **not explicitly flagged** in the CSV output.

Their presence must be inferred during analysis using:

- Known command timing
- Observed angular response

This behavior is intentional and documented.

---

## Design Principle

> *If the firmware looks boring, it is working correctly.*
