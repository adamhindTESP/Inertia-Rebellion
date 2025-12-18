# Inertia Rebellion

**An Open-Source Initiative for Precision Inertial and Gravitational Instrumentation**

Repository: `Inertia-Rebellion`

**Licenses**
- **Hardware:** CERN Open Hardware Licence v2 – Permissive  
- **Software:** MIT License

---

## Overview

**Inertia Rebellion** is an open-source experimental physics initiative focused on the
design, simulation, construction, and validation of **precision torsion-based instruments**
for investigating subtle inertial, gravitational, and environmental effects.

This repository does **not** represent a single experiment or scientific claim.
Instead, it serves as an **umbrella framework** for multiple independently testable
research modules developed using open-science principles.

Each module is released only after its assumptions, limitations, and validation
requirements are explicitly documented.

The project emphasizes:

- Instrumentation before interpretation  
- Explicit assumptions and non-goals  
- Reproducibility and falsifiability  
- Conservative, gated experimental workflows  
- Accessibility to independent builders and reviewers  

No scientific claims are made by default.  
All interpretation is conditional on successful validation.

---

## Repository Philosophy

This repository is organized around **modules**, each representing a self-contained
experimental platform or investigation.

All modules follow the same core principle:

> **Build instruments first.  
> Validate them rigorously.  
> Only then ask physics questions.**

Modules are expected to progress through clearly defined phases:

1. Theoretical motivation and modeling  
2. Numerical sensitivity and falsification studies  
3. Hardware design and bench validation  
4. Data collection and analysis  
5. Interpretation and publication (if warranted)

Different modules may be at different phases at any given time.

---

## Active Module: AIRM  
**Anisotropic Inertial Response Model**

The currently active module in this repository is **AIRM**, which explores whether a
torsional oscillator could exhibit a time-dependent modulation of effective inertia
correlated with controlled laboratory rotation and Earth’s sidereal motion.

This module is framed explicitly as a **search and constraint experiment**,  
**not** an assertion of new physics.

---

## Phenomenological Model (AIRM)

The hypothesized effect is parameterized as a modulation of the effective moment of inertia:

I_eff(t) = I_0 [ 1 + α cos( 2π (f_spin + f_sid) t ) ]

where:

- `I_0` is the nominal moment of inertia  
- `α` is a dimensionless coupling parameter  
- `f_spin` is the controlled rotation frequency of the apparatus  
- `f_sid` is the sidereal frequency  

A hypothetical signal would appear at sideband frequencies:

f_spin ± f_sid

This formulation is used **only** to define instrument sensitivity requirements and
analysis targets.

---

## Numerical Sensitivity Studies (AIRM)

A complete numerical simulation of the torsion pendulum dynamics and analysis pipeline
has been performed for the AIRM module. These studies include:

- High-Q torsional oscillator dynamics  
- Realistic readout noise models  
- Phase- and quadrature-based demodulation  
- Explicit null and falsification tests  

**Representative simulation parameters:**

- Natural oscillation period: **19.86 s**  
- Quality factor: **Q ≈ 100,000**  
- Integration time: **48 hours**

**Simulation outcome (theoretical only):**

- Background frequency noise (null) -

(4.32 ± 1.15) × 10⁻⁸ Hz

- Numerical sensitivity to coupling parameter: -

α_min ≲ 1 × 10⁻¹⁰

These results establish **theoretical sensitivity only**.  
**No physical data have been collected.**

The numerical results motivate construction of validation hardware but do **not**
constitute experimental constraints.

Full analysis code is available in:

/simulation/

---

## Hardware Platform: AIRM Spinner

The AIRM module uses a low-cost, vacuum-compatible torsion-balance platform referred to
throughout the repository as the **AIRM Spinner**.

**Key subsystems:**

- **Torsion Pendulum Core**  
  Fiber-suspended asymmetric test mass  

- **Angular Metrology**  
  Optical lever (laser + photodiode)  

- **Actuation and Calibration**  
  Magnetic torque coil and controlled rotation stage  

- **Isolation**  
  Compact vacuum enclosure and passive vibration control  

**Estimated total system cost:** ~**$200 USD**

Complete build documentation, BOMs, firmware, and validation gates are provided in:

/hardware/

---

## Project Status

The current maturity and scope of the project are summarized in:

➡️ **STATUS.md**

In brief:

- Phase 1 — Hardware fabrication & bench validation  
- No experimental data exist yet  
- No physical claims are made  

---

## Roadmap

### AIRM Module

1. **Phase 0 — Complete**  
   Theory and numerical sensitivity studies  

2. **Phase 1 — Current**  
   Hardware construction and Tier-1 validation  

3. **Phase 2**  
   Integration, commissioning, and controlled data runs  

4. **Phase 3**  
   Analysis, interpretation, and publication (if warranted)

### Inertia Rebellion (Long-Term)

- Additional torsion-based sensing modules  
- Environmental and systematic coupling studies  
- Calibration-focused open instruments  
- Educational and citizen-science replications  

---

## Contributing

Contributions from scientists, engineers, makers, and students are welcome.

Areas of contribution include:

- **Hardware:** Replication, mechanical design, component testing  
- **Software:** Simulation, analysis, firmware development  
- **Theory:** Model refinement and falsification strategies  
- **Documentation:** Tutorials, build notes, replication reports  

Please review `/docs/` and open an Issue or Discussion to get started.

---

## Licensing and Citation

All hardware designs and documentation are released under the  
**CERN Open Hardware Licence v2 – Permissive**.

All software is released under the **MIT License**.

### Citation (AIRM Module)

If you reference the AIRM Spinner instrumentation or analysis framework, please cite:

Adam Hind  
*AIRM Spinner: An open-source torsion-balance platform for inertial anisotropy validation*  
Inertia Rebellion Project (2025)  
arXiv: *to be assigned*

---

## Final Note

**Inertia Rebellion is an instrumentation-first project.**

A numerical “GO” indicates that an instrument is worth building and validating —
**not** that new physics has been observed or is expected.

Interpretation follows validation.  
Validation follows construction.  
Construction follows careful modeling.

That ordering is intentional.
