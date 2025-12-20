# Hardware — AIRM Spinner Apparatus (Tier-1)

This document describes the **Tier-1 hardware design** of the AIRM Spinner torsion-balance apparatus used in the *Inertia Rebellion* project.

The hardware is designed to be:

- Low cost  
- Fully open  
- Replication-friendly  
- Explicit about limitations and systematics  

This is **not precision metrology hardware**.  
It is a **controlled testbed** for detecting *and falsifying* small inertial modulations under slow, deliberate rotation.

---

## 1. System Overview

The AIRM Spinner consists of a **slowly rotating torsion pendulum** instrumented with:

- A stepper-driven rotation stage  
- An optical-lever angular readout  
- A magnetic calibration torque actuator  
- Continuous digital data logging  

The entire system is controlled by a single microcontroller and is intended to operate continuously for **hours to days**.

### High-Level Architecture

Arduino MCU
├── Stepper motor driver → Rotation stage
├── Optical lever ADC   → θ(t) readout
├── MOSFET coil driver  → Calibration torque
└── USB serial          → Data logging

---

## 2. Design Philosophy

Key design choices:

- **Very low rotation frequency**
  - Tier-1 target: f_spin ≈ 0.001 Hz
  - Minimizes mechanical disturbance and vibration coupling

- **Injected calibration torque**
  - Ensures response to known forces
  - Prevents misidentification of noise as signal

- **Optical lever readout**
  - High sensitivity
  - Simple, inexpensive, and well-understood

- **Open electronics**
  - No proprietary sensors
  - No black-box signal conditioning

All subsystems are intentionally simple so that **failure modes remain visible**, not hidden.

---

## 3. Major Subsystems

### 3.1 Rotation System

- **Motor:** NEMA-17 stepper motor  
- **Driver:** A4988 or DRV8825  
- **Coupling:** Direct or 1:1 mechanical coupling  
- **Control:** Open-loop, constant step rate  

#### Tier-1 Configuration (Frozen)

- Full-step mode  
- **0.2 steps per second**  
- 200 steps per revolution  
- **1000 seconds per revolution**  
- Effective modulation frequency:  
  **f_spin ≈ 0.001 Hz**

The rotation system is **not an encoder** and does not provide absolute angular position.

Its purpose is to impose a **configured, repeatable modulation timescale** (set by firmware), not to measure angle.

---

### 3.2 Torsion Pendulum

- **Suspension:** Thin torsion fiber (material user-selectable)  
- **Test mass:** Symmetric mass distribution  
- **Mirror:** Small front-surface mirror for optical lever  

Desired properties:

- Low torsional stiffness  
- Long decay time (high Q preferred)  
- Minimal magnetic and thermal asymmetry  

The mechanical design is intentionally flexible to allow replication using locally available materials.

---

### 3.3 Optical Lever Readout

Angular displacement θ(t) is measured using a **laser + photodiode optical lever**.

**Components:**
- 650 nm, 5 mW laser diode  
- Front-surface mirror on pendulum  
- BPW34 (or equivalent) photodiode  
- Passive resistor + RC filter into Arduino ADC  

**Principle:**
- Angular deflection → beam displacement  
- Photodiode voltage varies approximately linearly with θ  
- ADC digitizes at 1 Hz (Tier-1 default)

This readout is:
- Sensitive  
- Drift-prone by design (so drift is observable)  
- Calibrated using injected torque

---

### 3.4 Magnetic Calibration Coil

A magnetic calibration coil provides **explicit, repeatable torque injections**.

**Components:**
- Solenoidal coil (~500 turns, 28 AWG)  
- Logic-level N-channel MOSFET  
- Flyback protection diode  
- 12 V external supply  

**Operation:**
- Short current pulse (~100 ms typical)  
- Produces magnetic field coupling to pendulum-mounted magnet  

**Purpose:**
- Verify torsional response  
- Measure system gain  
- Distinguish mechanical dynamics from readout artifacts  

If a signal cannot be reproduced using injected torque, it is **not trusted**.

---

### 3.5 Control Electronics

- **Microcontroller:** Arduino Uno or Nano (ATmega328P)  
- **Interfaces:**
  - Digital outputs → stepper control  
  - PWM output → calibration coil  
  - Analog input → optical lever  
- **Logging:** USB serial, CSV format  

The Arduino platform is used for:
- Transparency  
- Simplicity  
- Replication ease  

No timing-critical DSP or signal processing is performed onboard.

---

## 4. Power Architecture

Two power domains are used:

| Subsystem | Voltage | Source |
|---------|--------|--------|
| MCU + optics | 5 V | USB or regulated supply |
| Stepper + coil | 12 V | External wall adapter |

All grounds are tied at a single reference point.

Care is taken to:
- Avoid ground loops  
- Prevent motor noise from contaminating ADC readings  

---

## 5. Schematics & Wiring

Complete schematics are provided in the hardware directory:

- `hardware/spinner_schematics.html` — interactive / printable  
- `hardware/spinner_schematics.pdf` — publication-ready  
- `hardware/BOM.md` — component list and costs  

Schematics include:
- Full pin mappings  
- Safety notes (laser, MOSFETs)  
- Validation checklist  
- Estimated cost breakdown  

Builders are strongly encouraged to review schematics before assembly.

---

## 6. Bill of Materials (Summary)

Electronics cost target (excluding mechanics):

- **Total:** ~USD $75  
- **MCU + motor + driver:** ~USD $45  
- **Optics + calibration electronics:** ~USD $30  

Mechanical components (frame, fiber, enclosure) are intentionally not standardized.

---

## 7. Known Limitations

This hardware does **not** provide:

- Absolute angle measurement  
- Temperature stabilization  
- Vibration isolation  
- Magnetic shielding beyond basic precautions  

These limitations are intentional so that:
- Noise sources remain visible  
- Over-interpretation is avoided  
- Replication does not require specialized facilities  

---

## 8. Safety Notes

- **Laser:** Class 3R (5 mW). Avoid eye exposure.  
- **Stepper driver:** Set current limit before connecting motor.  
- **MOSFET:** Must be logic-level (Rds(on) specified at 4.5–5 V).  
- **Power:** Always share common ground between supplies.  

Failure to follow these guidelines may damage hardware or invalidate data.

---

## 9. Relation to Other Documentation

- Firmware → `docs/firmware.md`  
- Calibration → `docs/calibration.md`  
- Analysis → `docs/analysis.md`  
- Simulations → `simulation/`  

---

## Status

- Hardware: **Replication-ready**  
- Schematics: **Complete**  
- BOM: **Complete**  
- Mechanical variants: **Open**  

The goal is not perfection.  
The goal is **testability**.
