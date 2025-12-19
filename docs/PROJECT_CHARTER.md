**`/docs/CHARTER.md` — Inertia Rebellion Project Charter**

---

# Inertia Rebellion — Project Charter

## 1. Mission

**Inertia Rebellion** is an open-source, citizen-science initiative focused on the
**design, construction, and validation of low-cost torsion-balance instrumentation**
for precision inertial and gravitational experiments.

The project’s primary goal is to develop and validate experimental platforms
capable of **testing sensitivity** to hypothetical macroscopic inertial anisotropy
at the level of a dimensionless coupling parameter
\( \alpha \sim 10^{-10} \), as motivated by Mach-inspired and related
phenomenological models.

This project is **instrumentation-first**:

- No physical effects are assumed to exist  
- No discovery claims are made by default  
- All interpretation is conditional on successful validation  

Scientific rigor is promoted through pre-registered analysis protocols,
open hardware and software, and transparent community collaboration.

---

## 2. Phenomenological Modeling Context

To define instrument requirements and analysis targets, the system is modeled
using a **phenomenological torsional oscillator framework**.

The angular dynamics are written as:

\[
I_0 \left[ 1 + \epsilon(t) \right] \ddot{\theta}(t)
+ \gamma \dot{\theta}(t)
+ \kappa \theta(t)
= \tau_{\mathrm{ext}}(t)
\]

where the hypothetical modulation is parameterized as:

\[
\epsilon(t) = \alpha \cos\!\left( 2\pi f_{\mathrm{target}} t \right)
\]

Equivalently, this can be expressed as an effective moment of inertia:

\[
I_{\mathrm{eff}}(t) = I_0 \left[ 1 + \alpha \cos\!\left( 2\pi f_{\mathrm{target}} t \right) \right]
\]

In this phenomenological model, the coupling parameter \( \alpha \) produces a
fractional modulation of the resonant frequency:

\[
\frac{\Delta \omega_0^2}{\omega_0^2} \approx -\epsilon(t)
\]

These expressions are used **solely** to:

- Establish instrument sensitivity requirements  
- Define null and falsification tests  
- Guide numerical simulations  

They do **not** constitute an assumed physical theory.

---

## 3. Scope and Objectives

### In Scope

- **Phase 0 — Complete**  
  Phenomenological modeling, numerical sensitivity studies, falsification analysis

- **Phase 1 — Current**  
  Hardware fabrication, subsystem testing, and Tier-1 validation of the
  *AIRM Spinner* apparatus, including publication of BOMs, CAD files,
  firmware, and validation gates

- **Phase 2 — Future**  
  Commissioning, controlled data runs, and systematic characterization

- **Phase 3 — Conditional**  
  Analysis, documentation, and dissemination of results  
  (including null results, if applicable)

### Explicitly Out of Scope

- Claims of discovery or new physics  
- High-cost or proprietary vacuum systems  
- Non-torsional experimental approaches  
- Interpretation prior to successful validation  

---

## 4. Assumptions, Risks, and Mitigation

### Key Assumptions

- High-Q torsional operation is achievable using low-cost components  
- Optical lever angular sensitivity of order  
  \( 10^{-8}\,\mathrm{rad} \) is practical  
- Sidereal-frequency sidebands can be distinguished from dominant systematics  

### Principal Risks

- Environmental noise exceeding modeled levels  
- Fabrication tolerances limiting achievable quality factor  
- Systematic couplings mimicking target modulation frequencies  

### Mitigation Strategies

- Pre-registered analysis and falsification protocols  
- Explicit null tests and off-target frequency checks  
- Modular hardware design to support iteration  
- Open community review and replication  

---

## 5. Governance and Contributions

- **Project Lead:** Adam Hind (`adamhindTESP`)
- **Decision Process:**  
  Open discussion via GitHub Issues and Discussions  
  Major changes require pull requests and review

- **Code of Conduct:**  
  Governed by `CODE_OF_CONDUCT.md`

- **Contributions Welcome In:**  
  - Hardware replication and testing  
  - Simulation and analysis tools  
  - Theory refinement and falsification proposals  
  - Documentation and educational material  

Contributors are encouraged to review this charter and the `/docs/` directory
before participating.

---

## 6. Milestones (Indicative)

- **Phase 0:** Modeling and numerical sensitivity analysis — *complete*  
- **Phase 1:** Hardware fabrication and bench validation — *in progress*  
- **Phase 2:** Commissioning and controlled measurements — *future*  
- **Phase 3:** Analysis and dissemination — *conditional*  

Timelines are intentionally flexible and depend on validation outcomes.

---

## 7. Resources and Infrastructure

- **Target Budget:** ~\$200 USD for Tier-1 apparatus  
- **Collaboration Platform:** GitHub  
- **Preprint Platform:** arXiv  
- **Licensing:**  
  - Hardware: CERN Open Hardware Licence v2 – Permissive  
  - Software: MIT License  

---

## 8. Success Criteria

Success is defined by **methodological clarity and reproducibility**, not by
positive results.

Key indicators include:

1. **Simulation Validation**  
   Demonstrated numerical sensitivity to  
   \( \alpha \lesssim 10^{-10} \)

2. **Experimental Validation**  
   Measured noise floors consistent with modeled limits

3. **Reproducibility**  
   Independent replication or validation attempts by external builders

4. **Dissemination**  
   Public release of methods, results (including nulls), and lessons learned

---

**Signed:** Adam Hind  
**Role:** Project Lead  
**Date:** 2025-12-18 (v0.1 release)
