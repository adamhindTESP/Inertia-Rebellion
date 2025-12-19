# Inertia Rebellion Project Charter

**`/docs/CHARTER.md` — Governance and Scope Document**

---

## 1. Project Mission

**Inertia Rebellion** is an open-source, citizen-science initiative to design, build, and validate a low-cost torsion-balance experiment. The goal is to **test instrument sensitivity** to hypothetical macroscopic inertial anisotropy (e.g., effects sometimes discussed in Mach-inspired or anisotropic inertia models) at a target coupling level of:

\[
\alpha \sim 1 \times 10^{-10}
\]

This project emphasizes **instrumentation-first science**, using pre-registered protocols, open hardware and software, and community review.

No claim is made regarding the existence of new physics.

---

## 2. Theory Summary

The torsional system is modeled as a damped harmonic oscillator with a time-dependent effective inertia:

\[
I_0 \left[ 1 + \epsilon(t) \right] \ddot{\theta}(t)
\;+\;
\gamma \, \dot{\theta}(t)
\;+\;
\kappa \, \theta(t)
\;=\;
\tau_{\mathrm{ext}}(t)
\]

where the fractional inertia modulation is parameterized as:

\[
\epsilon(t) = \alpha \cos\!\left( 2\pi f_{\mathrm{target}} \, t \right)
\]

Here:

- \( I_0 \) is the nominal moment of inertia  
- \( \theta(t) \) is the angular displacement  
- \( \gamma \) is the damping coefficient  
- \( \kappa \) is the torsion constant  
- \( \tau_{\mathrm{ext}}(t) \) represents external torques  

To first order, this modulation produces a fractional shift in the resonant frequency:

\[
\frac{\Delta \omega_0^2}{\omega_0^2} \;\approx\; -\,\epsilon(t)
\]

This formulation is used **only** to define sensitivity requirements and analysis targets.

---

## 3. Scope and Objectives

### Project Phases

- **Phase 0 — Theory & Simulation (Complete)**  
  Development of the Anisotropic Inertial Response Model (AIRM), numerical sensitivity studies, and falsification checks.

- **Phase 1 — Hardware Fabrication & Bench Validation (Current)**  
  Construction and validation of the **AIRM Spinner** apparatus.  
  Publication of BOMs, wiring, firmware, and validation protocols.

- **Phase 2 — Experimental Operation**  
  Commissioning, null tests, and controlled modulation runs.

- **Phase 3 — Analysis & Iteration**  
  Analysis, interpretation (if warranted), and design refinement.

### Explicitly Out of Scope

- Claims of discovery  
- High-cost or institutional vacuum systems  
- Non-torsion-based experimental methods  

---

## 4. Key Assumptions and Risks

### Assumptions

- High-Q torsional behavior can be achieved at low cost  
- Optical lever sensitivity of order  
  \[
  10^{-8}\,\mathrm{rad}
  \]
  is feasible  
- Sidereal-frequency signals can be distinguished from systematics  

### Risks

- Environmental noise exceeding modeled levels  
- Fabrication tolerances limiting achievable quality factor  
- Null results reducing community engagement  

### Mitigations

- Pre-registered analysis protocols (e.g., OSF / Zenodo)  
- Modular, upgradeable hardware design  
- Explicit acceptance of null results as valid outcomes  

---

## 5. Governance and Contribution Model

- **Project Lead:** Adam Hind (`adamhindTESP`)
- **Decision Making:**  
  Open discussion via GitHub Issues and Discussions
- **Major Changes:**  
  Require review via pull request
- **Code of Conduct:**  
  Contributor Covenant (see `CODE_OF_CONDUCT.md`)

Contributions are welcome in hardware replication, firmware, simulation, theory refinement, and documentation.

---

## 6. Milestones and Timeline

- **Phase 0:** Theory & simulation — *Complete (Dec 2025)*  
- **Phase 1:** Hardware validation — *Jan–Feb 2026*  
- **Phase 2:** Data collection — *Mar–Apr 2026*  
- **Phase 3:** Analysis & publication — *May 2026+*

Dates are aspirational and may shift based on validation outcomes.

---

## 7. Resources

- **Estimated Budget:** ~$200 USD (Tier-1 build)
- **Collaboration Platform:** GitHub
- **Preprint Archive:** arXiv
- **Licensing:**  
  - Hardware: CERN Open Hardware Licence v2 – Permissive  
  - Software: MIT License  

---

## 8. Success Metrics

1. **Simulation GO/NO-GO**  
   Demonstrated numerical sensitivity of  
   \[
   \alpha_{\min} \le 1 \times 10^{-10}
   \]
   in a 48-hour simulated integration.

2. **Experimental Validation**  
   Measured noise floor at the target frequency consistent with simulation.

3. **Replication**  
   At least **5 independent replication or validation attempts**.

4. **Dissemination**  
   Open-access arXiv preprint or journal publication (results or nulls).

---

## Sign-off

**Signed:** Adam Hind  
**Role:** Project Lead  
**Date:** 2025-12-18 (v0.1 release)
