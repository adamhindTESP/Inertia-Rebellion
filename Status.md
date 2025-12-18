# Project Status

**Project:** Inertia Rebellion  
**Active Module:** AIRM (Anisotropic Inertial Response Model)  
**Current Phase:** Phase 1 — Hardware Fabrication & Bench Validation  
**Latest Stable Release:** v0.1  
**Experimental Data:** None collected

---

## What Exists

The following components are complete and publicly available:

- Theoretical motivation and phenomenological modeling (AIRM)
- Numerical sensitivity and falsification simulations
- End-to-end analysis pipeline (simulation-based)
- Tier-1 hardware design, BOMs, and build documentation
- Formal hardware validation protocol and gating criteria
- Firmware for rotation control, calibration, and angular readout
- Open-source repository structure with versioned release (v0.1)

All designs, documentation, and software are released as open hardware / open source
under CERN OHL-P v2 and MIT-compatible licenses.

---

## What Does NOT Yet Exist

The following do **not** exist at this time:

- Physical hardware builds
- Calibration data
- Null datasets or sidereal data
- Any experimental measurements or constraints
- Any physical interpretation or claims

No real-world data have been collected for the AIRM module.

---

## Interpretation Policy

No physical interpretation, anomaly discussion, or parameter constraints are permitted
until **all Tier-1 validation gates** are passed on real hardware.

Numerical “GO” decisions in this repository indicate that:
- the analysis pipeline is well-behaved, and
- the instrument design is *worth constructing and validating*.

They do **not** imply:
- detection of an effect,
- expectation of new physics, or
- experimental constraints on physical models.

This repository currently represents a **methods and instrumentation release only**.

---

## Intended Use at This Stage

At its current maturity, this repository is intended for:

- Independent review of modeling and assumptions
- Replication of the Tier-1 hardware platform
- Bench validation and noise characterization
- Educational and citizen-science instrumentation work
- Preparation for future experimental campaigns

Any progression beyond Phase 1 requires successful completion of
the documented validation protocol.

---

## Change Control

Significant changes to scope, interpretation policy, or experimental status
will be reflected by:
- a new tagged release, and
- an update to this file.

---

**Last updated:** v0.1 release  
**Status:** Instrumentation development in progress
