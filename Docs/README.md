# Inertia Rebellion — Documentation

Welcome to the **Inertia Rebellion** documentation site.

This repository hosts open experimental hardware, firmware, analysis methods, and replication protocols for investigating **inertial anisotropy and frame-dependent effects** using low-cost, reproducible torsion-balance–style apparatus.

All documentation is written to support:
- Independent replication
- Incremental improvement
- Transparent error analysis
- Publication-adjacent technical clarity

This is not a claim repository.  
This is a **measurement and methods repository**.

---

## Project Overview

The **Inertia Rebellion Project** explores whether small, orientation-dependent or time-dependent deviations in inertial response can be detected using Earth-based rotating torsion systems.

The core experimental platform is the **AIRM Spinner**:
- A slowly rotating torsion pendulum
- Optical lever readout
- Controlled magnetic calibration torque
- Continuous data logging for long-baseline analysis

The design emphasizes:
- Ultra-low rotation frequencies
- Known injected calibration signals
- Open, auditable electronics and firmware
- Cost accessibility (sub-$200 electronics target)

---

## What This Documentation Covers

This documentation site includes:

- **Hardware construction**
  - Electronics schematics
  - Wiring and pinouts
  - Optical lever alignment
  - Power and safety considerations

- **Firmware**
  - Stepper control
  - Calibration pulse generation
  - ADC data acquisition
  - Serial logging format

- **Calibration & Validation**
  - Magnetic torque injection
  - Optical sensitivity calibration
  - Noise baseline characterization
  - Sanity checks and failure modes

- **Data & Analysis**
  - Expected signal structure
  - Rotation and sidereal modulation concepts
  - Noise sources and systematic controls
  - Replication-first analysis philosophy

- **Replication Guidance**
  - Builder checklists
  - Common pitfalls
  - Parameter ranges that matter
  - What *does not* matter

---

## Documentation Structure

```text
docs/
├── README.md        ← This page (project overview)
├── hardware.md      ← Hardware build & schematics
├── firmware.md      ← Arduino / control firmware
├── calibration.md   ← Calibration & validation procedures
├── analysis.md      ← Data analysis & interpretation
├── simulation.md   ← Simulations & synthetic data
└── contribute.md   ← How to contribute or replicate
