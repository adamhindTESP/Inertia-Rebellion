# Inertia Rebellion — Documentation Index

This directory contains the **authoritative documentation** for the
Inertia Rebellion project.

These documents define the **Tier-1 frozen experiment**:  
hardware, firmware behavior, calibration logic, analysis rules, and
replication boundaries.

This directory does **not** contain code or simulations.  
It defines **how those components must behave and be interpreted**.

---

## Documentation Scope

The documents in this folder are normative.  
They specify:

- What the experiment *is*
- What the experiment *is not*
- What assumptions are allowed
- What invalidates a dataset
- What must be reported for replication

Any change to Tier-1 behavior requires updating these documents
and incrementing the experiment version.

---

## Documentation Structure

Docs/
├── README.md        ← This index
├── hardware.md      ← Hardware design & limitations
├── firmware.md      ← Firmware guarantees & I/O behavior
├── calibration.md   ← Calibration & validation logic
├── analysis.md      ← Signal extraction & null tests
├── simulation.md   ← Simulation assumptions & scope
├── contribute.md   ← How to replicate or contribute
└── FUTURE_WORK.md  ← Speculative, non-frozen extensions

---

## Relation to Code & Data

The documentation here **governs** the following top-level directories:

- `firmware/`  
  → Implementation of the documented firmware behavior

- `hardware/`  
  → Schematics and build materials consistent with `hardware.md`

- `simulation/`  
  → Numerical simulations constrained by `simulation.md`

- `theory/`  
  → Phenomenological framework referenced by analysis

Documentation is always treated as **upstream** of code and data.

---

## Freeze Policy

Tier-1 documentation is **frozen by version**.

A change to any of the following requires a documented version increment:

- Firmware output format
- Calibration method
- Analysis pipeline
- Hardware coupling assumptions

Speculative ideas are isolated in `FUTURE_WORK.md`
and do **not** affect Tier-1 validity.

---

## Guiding Principle

> *If it is not documented here, it is not part of Tier-1.*

This separation ensures:
- Reproducibility
- Auditability
- Clear scientific boundaries
