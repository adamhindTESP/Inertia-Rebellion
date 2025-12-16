# Hardware — Inertia Rebellion Apparatus

This directory defines the **physical hardware, sourcing, and validation framework**
for the Inertia Rebellion torsion-balance experiment.

The hardware program is deliberately **incremental, gated, and conservative**.
Construction proceeds in tiers, and **no higher tier may be installed until the
previous tier has passed validation**.

This structure is essential to prevent false positives and to ensure that any
future sidereal or spinner-related signals are interpreted correctly.

---

## Hardware Philosophy

The apparatus is designed to be:

- Low-cost and accessible
- Modular and auditable
- Conservative in assumptions
- Explicitly falsifiable
- Suitable for independent replication

All measurements are grounded in **classical torsion-balance physics**.
No new physical effects are assumed in the hardware design.

---

## Build Tiers Overview

The build is divided into **two sequential tiers**:

- **Tier 1:** Static Pendulum (Required Baseline)
- **Tier 2:** Spinner Upgrade (Sidereal Search)

Tier 2 components **must not** be installed until Tier 1 has passed all validation
gates.

---

## Tier 1 — Static Pendulum (Required Baseline)

Tier 1 establishes the experimental foundation.

Its purpose is to:

- Measure the torsion constant κ
- Establish the angular noise floor
- Validate optical readout sensitivity
- Characterize damping and long-term stability
- Calibrate applied torque response

**No sidereal or spinner-related claims are possible in Tier 1.**

Tier 1 is mandatory for all builds.

**Estimated electronics + materials cost:** ~**$250 USD**

---

### Tier 1 Key Subsystems

- Torsion fiber and test mass
- Optical lever readout (laser + photodiode)
- Mechanical support and isolation
- Calibration torque actuator
- Data logging electronics

Tier 1 data defines all calibration constants required for later analysis.

---

## Tier 2 — Spinner Upgrade (Sidereal Search)

Tier 2 introduces controlled rotation of the apparatus to shift any hypothetical
signal away from Earth’s sidereal frequency and into the sidebands:

f_spin ± f_sid

This tier **does not change** the underlying torsion pendulum.
It only adds controlled modulation.

**Estimated incremental cost:** ~**$150 USD**

---

### Tier 2 Adds

- Slow, continuous rotation stage
- Motor and driver hardware
- Encoder or step-count tracking
- Mechanical decoupling elements
- Firmware-controlled spin frequency

Tier 2 must **not** be installed until Tier 1 validation is complete.

---

## Directory Contents

hardware/
- README.md — This file
- BOM_Tier1_Static_Pendulum.csv — Ordering list for Tier 1
- BOM_Tier2_Spinner_Upgrade.csv — Ordering list for Tier 2
- assembly_guide.md — Step-by-step build instructions
- validation.md — Hardware validation gates and criteria
- mechanical.md — Mechanical layout and alignment notes
- REVISION.md — Hardware revision history

---

## Validation Gates

Hardware validation is mandatory before advancing tiers.

Minimum Tier 1 validation includes:

1. Stable optical lever readout
2. Clearly resolved free torsional oscillations
3. Repeatable torque calibration response
4. No unexplained spectral lines near sidereal frequencies
5. Long-term stability over multi-hour runs

Validation criteria are defined in detail in:

hardware/validation.md

Tier 2 validation adds:

- Verified rotation frequency stability
- No mechanical coupling between motor and pendulum
- No spurious modulation introduced by rotation hardware

---

## Relationship to Other Directories

- **simulation/**  
  Defines sensitivity targets and hardware requirements

- **firmware/**  
  Deterministic control and raw data logging only

- **analysis/**  
  Offline signal extraction, null tests, and falsification

- **docs/**  
  Calibration models, systematics, and methodology

Hardware implements requirements defined elsewhere — it does not interpret data.

---

## Safety Notes

- Laser diodes must be operated within rated limits
- Magnetic calibration coils must include flyback protection
- Motors and drivers must be current-limited
- All grounds must be commoned to prevent measurement artifacts

Builders are responsible for safe laboratory practices.

---

## License

All hardware design files and documentation are released under the:

**CERN Open Hardware Licence Version 2 – Permissive (CERN-OHL-P v2)**

---

Proceed deliberately.  
Validate everything.  
Upgrade nothing prematurely.
