# arXiv Pre-Submission Summary  
**Inertia Rebellion — AIRM Module (v1.0.0 Methods Release)**

## Overview

This repository documents **Inertia Rebellion**, an open-source, instrumentation-first experimental physics initiative.  
The currently active module, **AIRM (Anisotropic Inertial Response Model)**, develops and validates a **low-cost torsion-balance apparatus** and analysis pipeline designed to test sensitivity to hypothetical inertial anisotropy under controlled rotation.

This is a **methods-only release**.  
No experimental data exist.  
No physical claims are made.

---

## Purpose of arXiv Submission

The intended arXiv submission serves to:

- Publicly document the **experimental design, assumptions, and limitations**
- Pre-register the **analysis pipeline, null tests, and falsification logic**
- Establish an **archival reference** for the instrumentation framework
- Enable independent review prior to any data collection

The submission is explicitly **not** a claim of detection or discovery.

---

## Scientific Context (High Level)

The experiment is motivated by phenomenological models sometimes discussed in the context of Mach-inspired or anisotropic inertia frameworks. These models motivate searching for **very small, time-dependent modulations** of the effective inertia of a torsional oscillator.

The project does **not** advocate a specific theory.  
The model is used only to define **instrument sensitivity targets** and **analysis frequencies**.

---

## Experimental Platform

**AIRM Spinner (Tier-1)**

- Fiber-suspended torsion pendulum
- Optical lever angular readout
- Ultra-slow controlled rotation (f_spin ≈ 0.001 Hz)
- Magnetic calibration torque injection
- Arduino-based deterministic firmware
- Continuous raw CSV data logging
- Offline analysis only (no onboard signal processing)

Estimated Tier-1 cost: ~200 USD.

The apparatus is intentionally simple, open, and replication-friendly.

---

## Analysis & Validation Strategy

The repository includes:

- Numerical simulations of torsion-pendulum dynamics
- Realistic readout noise models
- Phase- and quadrature-based demodulation
- Fixed-frequency analysis only (no scanning)
- Mandatory null and falsification tests:
  - no-spinner baseline
  - wrong-frequency projections
  - phase scrambling
  - calibration-window exclusion

A conservative **SNR > 10** decision threshold is fixed *a priori*.

All analysis steps are documented and reproducible.

---

## Current Status

- Theory & simulation: **Complete**
- Hardware design & documentation: **Complete**
- Firmware & logging: **Complete**
- Validation protocol: **Defined**
- Experimental data: **None collected**

This release represents a **frozen Tier-1 methods and instrumentation baseline**.

---

## What the Submission Does *Not* Claim

- No detection of inertial anisotropy
- No constraints on physical models
- No experimental anomalies
- No interpretation beyond instrumentation readiness

Any future claims would require:
- successful hardware validation
- null tests on real data
- independent replication

---

## Why arXiv Is Appropriate

The submission contributes:

- An openly documented precision-measurement platform
- A reproducible analysis pipeline with explicit falsification logic
- A low-cost experimental design suitable for replication and education
- A clear separation between methods and interpretation

The work is aligned with arXiv categories such as:
- experimental physics instrumentation
- precision measurement
- methods and validation studies
- physics.ins-det (Instrumentation and Detectors)

---

## Contact

**Author:** Adam Hind  
**Affiliation:** Independent Researcher  
**Repository:** https://github.com/adamhindTESP/Inertia-Rebellion  
**Release:** v1.0.0 (Tier-1 Methods & Instrumentation)

---

**Summary Statement**

> This submission documents *how* a careful torsion-balance experiment can be built, validated, and falsified — not *what it will find*.
