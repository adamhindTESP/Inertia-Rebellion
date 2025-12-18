# Inertia Rebellion

**An Open-Source Initiative for Precision Inertial and Gravitational Instrumentation**

Repository: `Inertia-Rebellion`

## Licenses
- **Hardware:** CERN Open Hardware Licence v2 – Permissive  
- **Software:** MIT License  

---

## Overview

**Inertia Rebellion** is an open-source experimental physics initiative focused on the **design, simulation, construction, and validation of precision torsion-based instruments** for investigating subtle inertial, gravitational, and environmental effects.

Rather than representing a single experiment or claim, this repository serves as an **umbrella framework** for multiple independently testable research modules. Each module is developed using open-science principles and is released only after its assumptions, limitations, and validation requirements are explicitly documented.

The project emphasizes:

- Instrumentation before interpretation  
- Explicit assumptions and non-goals  
- Reproducibility and falsifiability  
- Conservative, gated experimental workflows  
- Accessibility to independent builders and reviewers  

No scientific claims are made by default. All interpretation is conditional on successful validation.

---

## Repository Structure and Philosophy

This repository is organized around **modules**, each representing a self-contained experimental platform or investigation. Modules may differ in motivation, hardware, and analysis methods, but all follow the same core philosophy:

> **We build instruments first, validate them rigorously, and only then ask physics questions.**

Modules are expected to progress through clearly defined phases:

1. Theoretical motivation and modeling  
2. Numerical sensitivity and falsification studies  
3. Hardware design and bench validation  
4. Data collection and analysis  
5. Interpretation and publication (if warranted)  

At any given time, different modules may be at different phases.

---

## Active Module: AIRM

### Anisotropic Inertial Response Model

The currently active module in this repository is **AIRM**, which explores whether a torsional oscillator could exhibit a **time-dependent modulation of effective inertia** correlated with controlled laboratory rotation and Earth’s sidereal motion.

This module is framed explicitly as a **search and constraint experiment**, not an assertion of new physics.

---

### Phenomenological Model

The hypothesized effect is parameterized as a modulation of the effective moment of inertia:

\[
I_{\mathrm{eff}}(t) = I_0 \left[ 1 + \alpha \cos\!\left( 2\pi (f_{\mathrm{spin}} + f_{\mathrm{sid}})\, t \right) \right]
\]

where:

- \( I_0 \) is the nominal moment of inertia  
- \( \alpha \) is a dimensionless coupling parameter  
- \( f_{\mathrm{spin}} \) is the controlled rotation frequency of the apparatus  
- \( f_{\mathrm{sid}} \) is the sidereal frequency  

A hypothetical signal would appear at sideband frequencies:

\[
f_{\mathrm{spin}} \pm f_{\mathrm{sid}}
\]

This formulation is used solely to define **instrument sensitivity requirements and analysis targets**.

---

## Numerical Sensitivity Studies (AIRM)

A complete numerical simulation of the torsion pendulum dynamics and analysis pipeline has been performed for the AIRM module. These studies include:

- High-Q torsional oscillator dynamics  
- Realistic readout noise models  
- Phase- and quadrature-based demodulation  
- Explicit null and falsification tests  

### Representative Simulation Parameters

- Natural oscillation period: **19.86 s**  
- Quality factor: **Q ≈ 100,000**  
- Integration time: **48 hours**

### Simulation Outcome

- Background frequency noise (null):

\[
(4.32 \pm 1.15) \times 10^{-8}\ \mathrm{Hz}
\]

- Numerical sensitivity to coupling parameter:

\[
\alpha_{\min} \lesssim 1 \times 10^{-10}
\]

These results establish **theoretical sensitivity only**.  
No physical data have been collected.

The numerical results motivate construction of validation hardware but do **not** constitute experimental constraints.

The full analysis code is available in:
