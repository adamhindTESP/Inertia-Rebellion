# Hardware — AIRM Spinner Apparatus

This document describes the **hardware design** of the AIRM Spinner torsion-balance apparatus used in the Inertia Rebellion project.

The hardware is designed to be:
- Low cost
- Fully open
- Replication-friendly
- Explicit about limitations and systematics

This is **not precision metrology hardware**.  
It is a **testbed for detecting and falsifying small inertial modulations** under controlled rotation.

---

## 1. System Overview

The AIRM Spinner consists of a **slowly rotating torsion pendulum** instrumented with:

- A stepper-driven rotation stage
- An optical lever angular readout
- A magnetic calibration torque actuator
- Continuous digital data logging

The entire system is controlled by a single microcontroller and is intended to operate for **hours to days** without intervention.

High-level architecture:

Arduino MCU
├── Stepper motor driver → Rotation stage
├── Optical lever ADC   → θ(t) readout
├── MOSFET coil driver  → Calibration torque
└── USB serial          → Data logging

---

## 2. Design Philosophy

Key design choices:

- **Very low rotation frequency**
  - Typical f_spin ≈ 0.001 Hz
  - Minimizes mechanical disturbances

- **Injected calibration torque**
  - Ensures system responds to known forces
  - Prevents mistaking noise for signal

- **Optical lever readout**
  - High sensitivity
  - Simple, inexpensive, and well-understood

- **Open electronics**
  - No proprietary sensors
  - No black-box components

Every subsystem is deliberately simple so that **failure modes are visible**, not hidden.

---

## 3. Major Subsystems

### 3.1 Rotation System

- **Motor:** NEMA 17 stepper motor
- **Driver:** A4988 or DRV8825
- **Coupling:** Direct or 1:1 mechanical coupling
- **Control:** Open-loop, constant step rate

Typical configuration:
- Full-step mode
- ~1 step per second
- Resulting in ~0.001 Hz rotation

The rotation system is not intended to provide precise angular encoding.  
Its purpose is to impose a **known, stable modulation timescale**.

---

### 3.2 Torsion Pendulum

- **Suspension:** Thin torsion fiber (material user-selectable)
- **Test mass:** Symmetric mass distribution
- **Mirror:** Small front-surface mirror for optical lever

Key properties:
- Low torsional stiffness
- Long decay time (high Q preferred)
- Minimal magnetic and thermal asymmetries

The exact mechanical design is intentionally flexible to allow replication with locally available materials.

---

### 3.3 Optical Lever Readout

The angular displacement θ(t) is measured using a **laser + photodiode optical lever**.

Components:
- 650 nm, 5 mW laser diode
- Front-surface mirror on pendulum
- BPW34 (or equivalent) photodiode
- Resistor + RC filter into Arduino ADC

Principle:
- Angular deflection causes beam displacement
- Photodiode voltage varies approximately linearly with θ
- ADC digitizes signal at 1 Hz (typical)

This readout is:
- Sensitive
- Drift-prone (by design, so drift is observable)
- Calibrated via injected torque

---

### 3.4 Magnetic Calibration Coil

A magnetic calibration coil provides **known, repeatable torque impulses**.

Components:
- Solenoidal coil (~500 turns, 28 AWG)
- Logic-level N-channel MOSFET
- Flyback protection diode
- 12 V external supply

Operation:
- Short PWM pulse (e.g. 100 ms)
- Produces known magnetic field
- Couples to small magnet on test mass

Purpose:
- Verify torsion response
- Measure system gain
- Distinguish real dynamics from readout artifacts

If a signal cannot be reproduced with injected torque, it is not trusted.

---

### 3.5 Control Electronics

- **Microcontroller:** Arduino Uno or Nano (ATmega328P)
- **Interfaces:**
  - Digital outputs: stepper control
  - PWM output: coil driver
  - Analog input: optical lever
- **Logging:** USB serial, CSV format

The Arduino was chosen for:
- Simplicity
- Transparency
- Ease of replication

No timing-critical DSP is performed on-board.

---

## 4. Power Architecture

Two power domains are used:

| Subsystem | Voltage | Source |
|---------|--------|--------|
| MCU + optics | 5 V | USB or regulated supply |
| Stepper + coil | 12 V | External wall adapter |

All grounds are tied together at a single reference point.

Care is taken to:
- Avoid ground loops
- Prevent motor noise from contaminating ADC readings

---

## 5. Schematics & Wiring

Complete schematics are provided in the hardware directory:

- `hardware/spinner_schematics.html` — interactive, printable
- `hardware/spinner_schematics.pdf` — publication-ready PDF
- `hardware/BOM.md` — component list and costs

The schematics include:
- Full pin mappings
- Safety notes (laser, MOSFETs)
- Validation checklist
- Estimated cost breakdown

Builders are strongly encouraged to review the PDF before assembly.

---

## 6. Bill of Materials (Summary)

Electronics cost target (excluding mechanics):

- **Total:** ~USD $75
- **Microcontroller + motor + driver:** ~USD $45
- **Optics + coil electronics:** ~USD $30

Mechanical components (frame, fiber, enclosure) are intentionally not standardized.

---

## 7. Known Limitations

This hardware **does not** provide:

- Absolute angle measurement
- Temperature stabilization
- Vibration isolation
- Magnetic shielding beyond basic precautions

These limitations are intentional and documented so that:
- Noise sources remain visible
- Overinterpretation is avoided
- Replication does not require specialized facilities

---

## 8. Safety Notes

- **Laser:** Class 3R (5 mW). Avoid eye exposure.
- **Stepper driver:** Set current limit before connecting motor.
- **MOSFET:** Must be logic-level (Rds(on) specified at 4.5–5 V).
- **Power:** Always share common ground between supplies.

Failure to follow these guidelines can damage components or invalidate data.

---

## 9. Relation to Other Docs

- Firmware implementation → `docs/firmware.md`
- Calibration procedures → `docs/calibration.md`
- Data interpretation → `docs/analysis.md`
- Simulations → `docs/simulation.md`

---

## Status

- Hardware: **Replication-ready**
- Schematics: **Complete**
- BOM: **Complete**
- Mechanical variants: **Open**

This hardware will evolve as replications surface new constraints or improvements.

The goal is not perfection —  
the goal is **testability**.
