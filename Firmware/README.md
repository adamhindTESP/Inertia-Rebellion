# AIRM Spinner — Tier-1 Validation Hardware

This directory defines a **buildable torsion-balance apparatus** for the Inertia Rebellion project.  
The Tier-1 build is explicitly intended for **calibration, noise characterization, and validation of the full analysis pipeline**.

A numerical or simulation **“GO”** means this hardware is worth constructing for controlled measurement.

It does **not** imply:
- the existence of an anomaly
- an expectation of new physics
- a claim of anisotropic inertia

All physical interpretation is deferred until real data passes calibration, null, and falsification tests.

---

## Scope of This Build (Tier-1)

The Tier-1 apparatus is designed to answer one question only:

> **“Are we measuring what we think we are measuring?”**

Specifically, Tier-1 enables:

- Verification of angular readout sensitivity
- Measurement of torsion constant \( \kappa \) and damping \( Q \)
- Injection and recovery of known calibration torques
- Long-duration null data collection
- End-to-end testing of the analysis pipeline on real hardware

---

## Directory Contents

hardware/
├── README.md                ← this file (build + integration guide)
├── Validation.md            ← validation gates and criteria
├── spinner_schematics.html  ← full wiring & circuit schematics (printable)

---

## Hardware Architecture (Summary)

- **Control & Logging**: Arduino Uno / Nano
- **Rotation**: NEMA-17 stepper via A4988 / DRV8825
- **Angular Readout**: Optical lever (laser + photodiode)
- **Calibration**: Magnetic torque coil (MOSFET-driven)
- **Data Output**: 1 Hz CSV over USB serial

Full wiring diagrams and pinouts are provided in  
➡️ **`spinner_schematics.html`**

---

## Bill of Materials (Tier-1)

### A. Control & Computation

| Item | Specification | Qty |
|-----|---------------|-----|
| Arduino Uno R3 | ATmega328P, USB | 1 |
| USB Cable | USB-A ↔ USB-B | 1 |

### B. Motion / Spin System

| Item | Specification | Qty |
|-----|---------------|-----|
| Stepper Motor | NEMA-17, 200 steps/rev | 1 |
| Stepper Driver | A4988 or DRV8825 (with heatsink) | 1 |
| External PSU | 12 V, ≥ 2 A | 1 |

### C. Optical Lever Readout

| Item | Specification | Qty |
|-----|---------------|-----|
| Laser Diode Module | 650 nm, 5 mW, 5 V (Class 3R) | 1 |
| Photodiode | BPW34 | 1 |
| Resistor | 330 Ω, ¼ W | 1 |
| Resistor | 10 kΩ, ¼ W | 1 |
| Capacitor | 10 nF ceramic | 1 |
| Mirror | Small, front-surface | 1 |

### D. Calibration / Actuation

| Item | Specification | Qty |
|-----|---------------|-----|
| MOSFET | IRLZ44N (logic-level) | 1 |
| Flyback Diode | 1N4007 | 1 |
| Magnet Wire | 28 AWG (~10 m) | 1 |
| NdFeB Magnet | ~1 g | 1 |

### E. Mechanical (Reference Components)

| Item | Specification | Notes |
|-----|---------------|------|
| **Torsion Fiber (Starter)** | 0.1 mm polymer fishing line | Low-Q, beginner friendly |
| **Torsion Fiber (Precision)** | 25–50 µm tungsten | High-Q upgrade |
| Rotation Stage | Manual or motor-coupled | 1:1 coupling |
| Frame | Rigid, non-magnetic | Aluminum / composite |
| Breadboard / Perfboard | — | Prototyping |
| Jumper Wires | Male–male | ~20 |

**Cost (Tier-1):**  
- Electronics + starter fiber: **~$85 USD**  
- Precision fiber upgrade: **+ $30–50**

---

## Tools Required

- Soldering iron and solder  
- Digital multimeter (DMM)  
- Wire cutters / strippers  
- Small screwdrivers / hex keys  
- Computer with USB port  

---

## Recommended Build Order

### Phase 0 — Electronics Bring-Up (No Mechanics)

**Goal:** Verify firmware and electronics in isolation.

1. Flash Arduino with spinner firmware
2. Verify USB serial output
3. Wire stepper driver + motor
4. Set driver current limit (see below)
5. Verify smooth rotation at target speed
6. Confirm common ground between 5 V and 12 V rails

**STOP** if vibration, missed steps, or overheating occur.

---

### Phase 1 — Optical Readout Validation

**Goal:** Verify angular sensing without interpretation.

1. Rigidly mount laser and photodiode
2. Align beam to photodiode center
3. Record ADC value at rest (~512 typical)
4. Manually deflect mirror → verify linear response
5. Record short runs to estimate noise floor

---

### Phase 2 — Calibration Coil Verification

**Goal:** Verify known-torque injection.

1. Wind calibration coil (~500 turns)
2. Wire coil, MOSFET, and flyback diode
3. Trigger PWM pulse (`C` command)
4. Observe transient in optical signal
5. Confirm repeatability

---

### Phase 3 — Mechanical Integration

**Goal:** Integrate torsion system conservatively.

1. Suspend torsion fiber
2. Mount mirror and test magnet
3. Attach rotation stage (1:1 coupling)
4. Verify free oscillation
5. Measure natural frequency \( f_0 \) and \( Q \)
6. Compare measured values to simulation inputs

---

### Phase 4 — Long-Duration Validation Runs

**Goal:** Produce data suitable for pipeline testing.

1. Run spinner at configured \( f_{\mathrm{spin}} \)
2. Collect ≥ 24–48 hours of continuous data
3. Inject calibration pulses periodically
4. Run full analysis pipeline on real data

---

## Stepper Driver Current Limit (Critical)

**Most common failure mode.**

**Procedure (A4988 / DRV8825):**

1. Disconnect stepper motor
2. Power driver with 12 V
3. Set DMM to DC volts
4. Black probe → GND
5. Red probe → Vref potentiometer
6. Adjust until **Vref ≈ 0.4 V**
7. Power off, reconnect motor

- Too high → vibration, heat  
- Too low → missed steps  

---

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|------|-------------|----|
| Stepper vibrates | Current limit wrong | Reset Vref |
| No rotation | ENABLE pin floating | Tie ENABLE → GND |
| Jerky motion | Speed too high | Reduce steps/s |
| ADC stuck at 0 or 1023 | Photodiode reversed | Swap polarity |
| No coil response | Wrong MOSFET | Use IRLZ-series |

If multiple issues appear, revert to **Phase 0**.

---

## Tier-1 Validation Criteria

- Optical noise floor ≲ \(10^{-8}\,\mathrm{rad}/\sqrt{\mathrm{Hz}}\) (order-of-magnitude)
- Null runs show no coherent peak at \( f_{\mathrm{target}} \)
- Calibration injections recovered with correct phase and scaling
- Wrong-frequency analysis yields false/true < 0.1

See **`Validation.md`** for formal gate definitions.

---

## Explicit Non-Goals

This build does **not** aim to:

- demonstrate anisotropic inertia
- detect new physics
- produce publishable anomalies

It exists solely to validate the **instrument + analysis chain**.

---

## Gate to Next Tier

Progress beyond Tier-1 requires:

- stable noise characterization
- reproducible calibration response
- agreement between measurement and simulation
- successful falsification tests on real data

Only after these conditions are met should physical interpretation be attempted.

---

## Builder Skill Expectations

| Skill Level | Outcome |
|-----------|--------|
| Expert maker | Smooth build |
| Arduino hobbyist | Successful with this guide |
| Beginner citizen scientist | Successful with patience |
| Complete novice | Not recommended (yet) |

---

## Final Note

> **Accessibility improves replicability, not claims.**

A successful Tier-1 build means:

> *“We are measuring what we think we are measuring.”*

Nothing more — and nothing less.

**Tier-1 hardware is ready for distributed replication.**
