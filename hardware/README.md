# AIRM Spinner — Tier-1 Validation Build

## Hardware Readiness Scope

This hardware documentation defines a **buildable torsion-balance apparatus**
intended for calibration, noise characterization, and validation of the
analysis pipeline.

A numerical or analysis **“GO”** indicates that this apparatus is worth
constructing for controlled measurement and validation.

It does **not** imply that any physical anomaly is expected, predicted,
or claimed. All physical interpretation is deferred until experimental
data successfully passes calibration, null, and falsification tests.

---

## 🔧 Accessibility & Builder Support (Tier-1)

This section exists to help non-expert builders successfully assemble and
validate the Tier-1 apparatus without compromising experimental rigor.

These additions are optional but strongly recommended for
citizen-science replication.

---

## Bill of Materials (BOM)

### A. Control & Computation

| Item | Specification | Qty | Example Source (Non-binding) |
|------|---------------|-----|-----------------------------|
| Arduino Uno R3 | ATmega328P, USB | 1 | Arduino / Amazon |
| USB Cable | USB-A to USB-B | 1 | Generic |

---

### B. Motion / Spin System

| Item | Specification | Qty | Example Source |
|------|---------------|-----|----------------|
| Stepper Motor | NEMA 17, 200 steps/rev | 1 | Pololu / Amazon |
| Stepper Driver | A4988 or DRV8825 (with heatsink) | 1 | Pololu |
| External PSU | 12 V, ≥2 A | 1 | Generic |
| Heatsink | For driver | 1 | Included or add-on |

---

### C. Optical Lever Readout

| Item | Specification | Qty | Example Source |
|------|---------------|-----|----------------|
| Laser Diode Module | 650 nm, 5 mW, 5 V (Class 3R) | 1 | Amazon |
| Photodiode | BPW34 | 1 | Mouser / Digi-Key |
| Resistor | 330 Ω, ¼ W | 1 | Generic |
| Resistor | 10 kΩ, ¼ W | 1 | Generic |
| Capacitor | 10 nF ceramic | 1 | Generic |
| Mirror | Small, front-surface | 1 | Optical supplier |

---

### D. Calibration / Actuation

| Item | Specification | Qty | Notes |
|------|---------------|-----|-------|
| MOSFET | IRLZ44N (logic-level) | 1 | **Must be logic-level** |
| Flyback Diode | 1N4007 | 1 | Coil protection |
| Magnet Wire | 28 AWG | ~10 m | Calibration coil |
| NdFeB Magnet | ~1 g | 1 | Mounted to pendulum |

---

### E. Mechanical (Reference Components)

| Item | Specification | Qty | Notes |
|------|---------------|-----|-------|
| **Torsion Fiber (Starter)** | 0.1 mm polymer fishing line | 1 | Amazon / sporting goods (~$5) |
| **Torsion Fiber (Precision)** | 25–50 µm tungsten wire | 1 | Goodfellow / McMaster |
| **Torsion Fiber (Alt.)** | Quartz fiber | 1 | Commercial or pulled |
| Rotation Stage | Manual or motor-coupled | 1 | 1:1 coupling |
| Frame | Rigid, non-magnetic | 1 | Aluminum / composite |
| Breadboard / Perfboard | — | 1 | Electronics |
| Jumper Wires | Male-male | ~20 | |

**Torsion Fiber Notes**
- Fishing line yields lower Q (∼10³) but is fully sufficient for electronics
  validation, optical lever calibration, and pipeline testing.
- Precision fibers should only be used after the apparatus is mechanically
  stable and repeatable.

**TIER-1 TOTAL: ~$85** (electronics + starter fiber)  
Precision fiber upgrade: +$30–50.

---

## Tools Required

- Soldering iron and solder  
- Digital multimeter  
- Small screwdrivers / hex keys  
- Wire cutters / strippers  
- Computer with USB port  

---

## Mechanical Coupling — Conceptual Sketch

Stepper Motor Shaft
│
▼
┌─────────┐
│ Coupler │  (rigid or flexible)
└────┬────┘
│
▼
Rotation Stage
│
▼
Torsion Fiber
│
▼
Pendulum + Mirror

**Key requirement:**  
Rotation must be **slow, smooth, and repeatable** — not high torque.

---

## Recommended Build Order (Tier-1)

### Phase 0 — Bench Bring-Up (No Mechanics)

**Goal:** Verify electronics and firmware independently.

1. Flash Arduino with serial + logging firmware
2. Verify USB communication (Blink test)
3. Wire A4988 + stepper motor
4. **Set current limit** (see procedure below)
5. Verify smooth rotation at commanded rate
6. Verify common ground between 5 V and 12 V rails

**STOP if vibration, missed steps, or overheating occur.**

---

### Phase 1 — Optical Readout Validation

**Goal:** Verify angular sensing without interpretation.

1. Mount laser and photodiode rigidly
2. Align beam to photodiode center
3. Record ADC at rest (expect ~512)
4. Manually deflect mirror → confirm linear response
5. Record short data runs → estimate noise floor

---

### Phase 2 — Calibration Coil Verification

**Goal:** Verify known-torque injection.

1. Wind calibration coil (~500 turns)
2. Wire coil, MOSFET, and flyback diode
3. Trigger PWM pulse from Arduino
4. Observe transient in optical signal
5. Confirm repeatability of injected response

---

### Phase 3 — Mechanical Integration

**Goal:** Integrate components conservatively.

1. Suspend torsion fiber
2. Mount mirror and test magnet
3. Attach rotation stage (1:1 coupling)
4. Verify free oscillation
5. Measure natural frequency \( f_0 \) and quality factor Q empirically
6. Use measured values for all subsequent analysis

---

### Phase 4 — Long-Duration Validation Runs

**Goal:** Produce data suitable for pipeline testing.

1. Run spin at configured \( f_{\mathrm{spin}} \)
2. Collect ≥ 24–48 h of continuous data
3. Inject calibration pulses periodically
4. Run full analysis pipeline on real data

---

## Stepper Driver Current Limit — Beginner Procedure

**Incorrect current limit is the most common build failure.**

**Required Tool:** Digital multimeter (DMM)

**Procedure (A4988 / DRV8825):**
1. Disconnect stepper motor
2. Power driver with 12 V supply
3. Set multimeter to DC volts
4. Place black probe on GND
5. Place red probe on Vref potentiometer
6. Adjust until **Vref ≈ 0.4 V**
7. Power off, reconnect motor, power on

**Rule of thumb**
- Too high → vibration, heat
- Too low → missed steps, stalling

---

## Common Failure Modes & Fixes

| Symptom | Likely Cause | Fix |
|--------|--------------|-----|
| Stepper vibrates | Current limit wrong | Re-set Vref to 0.4 V |
| No rotation | ENABLE pin floating | Tie ENABLE → GND |
| Jerky motion | Speed too high | Reduce to 0.5 steps/s |
| ADC stuck at 0 or 1023 | Photodiode reversed | Swap diode polarity |
| Laser signal noisy | Ambient light | Add shield / reduce gain |
| No coil response | Wrong MOSFET | Use IRLZ44N (not IRF520) |

**If multiple issues appear, stop and revert to Phase 0.**

---

## Tier-1 Validation Criteria

- Optical readout noise floor consistent with ≤ 10⁻⁸ rad/√Hz (order-of-magnitude)
- Null runs show no coherent peak at \( f_{\mathrm{target}} \)
- Calibration injections recovered with correct phase and amplitude scaling
- Wrong-frequency analysis yields false/true < 0.1

---

## Explicit Non-Goals

This build does **not** aim to:

- demonstrate anisotropic inertia
- detect new physics
- produce publishable anomalies

It exists to determine whether the **instrument + analysis chain**
behaves as required.

---

## Gate to Next Tier

Progress beyond Tier-1 requires:

- stable noise characterization
- reproducible calibration response
- agreement between measured and simulated behavior
- successful falsification tests on real data

Only after these conditions are met should physical interpretation
be considered.

---

## Builder Skill Expectations

| Skill Level | Expected Outcome |
|------------|------------------|
| Expert maker | Smooth build |
| Arduino hobbyist | Successful with this guide |
| Beginner citizen scientist | Successful with patience |
| Complete novice | Not recommended (yet) |

*A kit or video guide may be added in a future release.*

---

## Final Note

**Accessibility improves replicability, not claims.**

A successful Tier-1 build means:

> *“We are measuring what we think we are measuring.”*

Nothing more — and nothing less.

**TIER-1 TOTAL COST: ~$85** — ready for distributed replication.
