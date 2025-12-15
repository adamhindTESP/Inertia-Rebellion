# The Inertia Rebellion Project: An Open-Source Search for Anisotropic Inertia

**Repository:** `inertia-rebellion`  
**License:** CERN Open Hardware Licence Version 2 - Permissive (Hardware), MIT (Software)

---

## Project Overview

The **Inertia Rebellion Project** is an open-hardware, open-science initiative to design, build, and operate a high-sensitivity torsion balance. The mission is to perform a laboratory-scale test for **macroscopic inertial anisotropy** — a possible signature of Mach's principle — at a sensitivity target of **α ~ 1×10⁻¹⁰**.

This repository contains the complete theoretical framework, sensitivity analysis, hardware design, and build protocol for the **"Spinner" apparatus**, a vacuum-compatible torsion pendulum with a rotating asymmetric test mass.

---

## Core Scientific Framework: The Anisotropic Inertial Response Model (AIRM)

The experiment aims to detect or constrain a hypothetical anisotropy in inertia by modeling it as a time-dependent modulation of the torsion pendulum’s effective moment of inertia:

I_eff(t) = I0 [ 1 + α cos( 2π (f_spin + f_sid) t ) ]

Where:
- **α** — Dimensionless anisotropy coupling constant  
- **fₛₚᵢₙ** — Controlled rotation frequency of the apparatus  
- **fₛᵢd** — Sidereal frequency  

This modulation produces a detectable signal at the sideband frequencies **fₛₚᵢₙ ± fₛᵢd**.

---

## Key Result: Theoretical Feasibility and GO Decision

A comprehensive numerical simulation of the system dynamics and signal detection chain has been performed. Using target hardware parameters and quadrature demodulation analysis, the simulation determines the minimum detectable anisotropy (**α_min**).

**Simulation Output Summary:**

```
Natural oscillation period, T0: 19.86 s
Approximate quality factor, Q: 100,000
Null background noise level: (4.32 ± 1.15) × 10⁻¹⁰ Hz
DECISION: GO — α_min ≤ 1 × 10⁻¹⁰
```

**Conclusion:**  
The proposed *Spinner* apparatus is theoretically capable of probing α down to the 10⁻¹⁰ level within a 48-hour integration. This warrants proceeding to the hardware construction phase.

The full sensitivity analysis is implemented in: /simulation/sensitivity_analysis.py

---

## Hardware Design: The "Spinner" Apparatus

A vacuum-capable torsion pendulum optimized for low-cost, high-precision construction. Major subsystems include:

- **Torsion Pendulum Core:** Quartz fiber suspension with asymmetric dumbbell test mass  
- **Metrology:** Laser-based optical lever for nanoradian angular measurement  
- **Actuation & Control:** Magnetic torque coil for calibration and a stepper-driven rotation stage for fₛₚᵢₙ modulation  
- **Vacuum & Isolation:** Simple chamber with vibration isolation platform  

A complete Bill of Materials (BOM) and build guide are in the `/hardware/` directory.  
**Estimated total cost: ~$200 USD**

---

## Roadmap and Contribution

This project follows a gated, pre-registered experimental protocol for scientific rigor. Development proceeds in four phases:

1. **Phase 0 (Complete):** Theoretical design and sensitivity simulation  
2. **Phase 1 (Current):** Hardware fabrication and subsystem validation  
3. **Phase 2:** Integration, commissioning, and data runs  
4. **Phase 3:** Data analysis, publication, and design iteration  

### How to Contribute

Collaboration from scientists, engineers, makers, and students is welcome.  
Possible contributions include:

- **Hardware:** Replicating the build, improving CAD designs, or characterizing components  
- **Software:** Enhancing data analysis, simulation tools, or microcontroller firmware  
- **Theory:** Refining the AIRM, analyzing systematic errors, or proposing testable extensions  
- **Outreach:** Documenting builds, translating materials, or leading community discussions  

Start by reviewing the **Project Charter** and **Theory documentation**, then introduce yourself and your interests in the **Discussions** or **Issues** tab.

---

## License and Citation

All hardware design files and documentation are released under the **CERN Open Hardware Licence Version 2 - Permissive**.  
Software and simulation code are released under the **MIT License**.

If this work informs your research or design, please cite:

> Adam Hind, *A low-cost, open-source torsion balance for high-sensitivity searches for macroscopic inertial anisotropy.* The Inertia Rebellion Project (2025). [arXiv ID to be assigned upon submission]

---

## Acknowledgments

This project protocol was developed through an iterative, collaborative design process.

---

## Repository Structure

```
inertia-rebellion/
├── README.md                       # This file
├── LICENSE.md                      # Licensing information
├── theory/                         # Theoretical foundations (AIRM)
├── simulation/                     # Feasibility and sensitivity analysis
├── hardware/                       # BOM, CAD, build instructions
├── firmware/                       # Microcontroller code for data acquisition & control
├── analysis/                       # Data analysis scripts and templates
└── docs/                           # Project charter, references, and other documents
```
```
