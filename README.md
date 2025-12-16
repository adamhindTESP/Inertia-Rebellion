# Inertia Rebellion

**An Open-Source Initiative for Precision Inertial and Gravitational Experiments**

Repository: `Inertia-Rebellion`  
Licenses:

- **Hardware:** CERN Open Hardware Licence v2 – Permissive
- **Software:** MIT License

-----

## Project Overview

**Inertia Rebellion** is an open-source experimental physics initiative dedicated to the design, simulation, and construction of **high-sensitivity torsion-based instruments** for probing subtle inertial, gravitational, and environmental effects.

Rather than a single experiment, Inertia Rebellion serves as an **umbrella framework** under which multiple independently testable research modules are developed, documented, and released using open-science principles. Each module is designed to be:

- Physically well-posed
- Explicit in assumptions
- Reproducible and falsifiable
- Accessible to independent builders and reviewers

The initiative emphasizes transparency, pre-registered analysis pipelines, and conservative interpretation of results.

-----

## Active Research Module: AIRM

### Anisotropic Inertial Response Model

### Scientific Motivation

The AIRM module investigates whether a torsional oscillator exhibits a **time-dependent modulation of effective inertia** correlated with laboratory rotation and Earth’s sidereal motion. Such a modulation would be consistent with certain Mach-inspired or anisotropic inertia hypotheses.

This is a **search and constraint experiment**, not an assertion of new physics.

### Phenomenological Model

The hypothesized effect is modeled as a modulation of the effective moment of inertia:

$$I_{\text{eff}}(t) = I_0 \left[ 1 + \alpha \cos\left( 2\pi (f_{\text{spin}} + f_{\text{sid}}) t \right) \right]$$

Where:

- $I_0$ — nominal moment of inertia
- $\alpha$ — dimensionless anisotropy coupling parameter
- $f_{\text{spin}}$ — controlled apparatus rotation frequency
- $f_{\text{sid}}$ — sidereal frequency

A detectable signal appears at the sideband frequencies:

$$f_{\text{spin}} \pm f_{\text{sid}}$$

-----

## AIRM Sensitivity Analysis and GO Decision

A comprehensive numerical simulation of the torsion pendulum dynamics and analysis pipeline has been completed. The simulation includes:

- High-Q oscillator dynamics
- Realistic readout noise
- Quadrature demodulation and phase-based frequency extraction
- Explicit falsification tests at offset frequencies

### Key Simulation Parameters

- Natural oscillation period: **19.86 s**
- Quality factor: **Q ≈ 100,000**
- Integration time: **48 hours**

### Result Summary

- Null background frequency noise:

$$(4.32 \pm 1.15) \times 10^{-8} \text{ Hz}$$

- Minimum detectable coupling:

$$\alpha_{\text{min}} \lesssim 1 \times 10^{-10}$$

**Decision:** ✅ **GO**  
The AIRM Spinner apparatus is theoretically capable of probing anisotropic inertia down to the $10^{-10}$ level under stated assumptions.

The full sensitivity analysis is implemented in:

**/simulation/airm_full_analysis.py**

-----

## AIRM Hardware Platform: The “Spinner” Apparatus

The AIRM module uses a **vacuum-compatible torsion balance**, optimized for low cost and high sensitivity.

### Major Subsystems

- **Torsion Pendulum Core**  
  Quartz fiber suspension with asymmetric dumbbell test mass
- **Metrology**  
  Laser-based optical lever for nanoradian-scale angular readout
- **Actuation & Control**  
  Magnetic torque coil (calibration) and stepper-driven rotation stage (spin modulation)
- **Vacuum & Isolation**  
  Compact vacuum chamber with passive vibration isolation

**Estimated total cost:** approximately **$200 USD**

Complete BOMs, CAD files, and build instructions are located in:

/hardware/

Future Inertia Rebellion modules may reuse, modify, or replace this platform depending on experimental goals.

-----

## Roadmap

### AIRM Module Roadmap

1. **Phase 0 (Complete)**  
   Theoretical framework and sensitivity simulation
1. **Phase 1 (Current)**  
   Hardware fabrication and subsystem validation
1. **Phase 2**  
   Integration, commissioning, and data runs
1. **Phase 3**  
   Data analysis, publication, and design iteration

### Inertia Rebellion Initiative (High-Level)

- Development of additional torsion-based sensing modules
- Transient gravitational and inertial sensing experiments
- Environmental coupling and systematic characterization
- Educational and calibration-focused open instruments

-----

## How to Contribute

Collaboration from scientists, engineers, makers, and students is welcome.

Ways to contribute include:

- **Hardware:** Replication, CAD improvements, component characterization
- **Software:** Simulation extensions, data analysis, firmware
- **Theory:** Model refinement, systematic error analysis, falsification proposals
- **Outreach:** Documentation, tutorials, replication reports

Start by reviewing the documentation in `/docs/`, then open an Issue or Discussion.

-----

## License and Citation

All hardware design files and documentation are released under the  
**CERN Open Hardware Licence v2 – Permissive**.

All software and simulation code are released under the **MIT License**.

### Citation (AIRM Module)

If you use or reference the **AIRM Spinner module**, please cite:

Adam Hind,  
*A low-cost, open-source torsion balance for high-sensitivity searches for macroscopic inertial anisotropy.*  
The Inertia Rebellion Project (2025).  
arXiv: to be assigned

-----

## Repository Structure

```
inertia-rebellion/  
├── README.md            # This file (umbrella overview)  
├── LICENSE.md           # Licensing information  
├── theory/              # Theoretical foundations (AIRM)  
├── simulation/          # Sensitivity and falsification studies  
├── hardware/            # BOMs, CAD, build instructions  
├── firmware/            # Microcontroller code  
├── analysis/            # Data analysis tools and templates  
└── docs/                # Project charter, references, design notes  
```

This repository currently hosts the **AIRM Spinner module**.  
Additional modules may be added here or released as standalone repositories as the initiative expands.

-----

## Acknowledgments

This project protocol was developed through an iterative, open design process and benefits from the broader torsion-balance and precision-measurement research community.
