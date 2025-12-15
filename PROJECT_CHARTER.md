# Inertia Rebellion Project Charter

## 1. Project Mission

The Inertia Rebellion is an open-source, citizen-science initiative to design, build, and operate a low-cost torsion balance experiment. The goal is to probe for hypothetical macroscopic inertial anisotropy (e.g., related to tensor-to-scalar matter coupling)—a potential laboratory signature of Mach's principle—at a target sensitivity of $\alpha \approx 1 \times 10^{-10}$. This project promotes scientific rigor through pre-registered protocols, open hardware/software, and community collaboration, without asserting the existence of new physics.

## 2. Theory Summary

The system is governed by:

$$I_0 [1 + \epsilon(t)] \ddot{\theta}(t) + \gamma \dot{\theta}(t) + \kappa \theta(t) = \tau_{\text{ext}}(t)$$

where $\epsilon(t) = \alpha \cos(2\pi f_{\text{target}} t)$ encodes possible anisotropic inertia.

The discovery parameter is $\alpha$, which modulates the resonant frequency:

$$\frac{\Delta \omega_0^2}{\omega_0^2} \approx -\epsilon(t)$$

## 3. Scope and Objectives

- **Theoretical Phase (Complete)**: Develop the Anisotropic Inertial Response Model (AIRM), perform sensitivity simulations, and establish feasibility.
- **Hardware Phase (Current)**: Fabricate subsystems, validate components, and assemble the "Spinner" apparatus. Publish Fritzing/CAD files and Bill of Materials (BOM).
- **Experimental Phase**: Commission the setup, conduct null and modulated data runs, analyze results.
- **Iteration Phase**: Publish findings, refine designs based on community input.

**Out of scope**: Claims of discovery; high-cost vacuum systems; non-torsion methods.

## 4. Key Assumptions and Risks

- **Assumptions**: High-Q vacuum operation achievable at low cost; optical lever sensitivity $\sim 10^{-8}$ rad; sidereal modulation distinguishable from systematics.
- **Risks**: Environmental noise (seismic, thermal) exceeding models; fabrication tolerances limiting Q; null results discouraging iteration.
- **Mitigation**: Pre-registered analysis protocols (e.g., on OSF or Zenodo) to avoid bias; modular design for upgrades; community review.

## 5. Governance and Contribution Guidelines

- **Lead**: Adam Hind (adamhindTESP)
- **Decision Making**: Consensus via GitHub Issues/Discussions; major changes require pull requests.
- **Code of Conduct**: Follow Contributor Covenant (add CODE_OF_CONDUCT.md if needed).
- **Contributions**: Welcome in hardware builds, code enhancements, theory refinements, outreach. Start by reviewing this charter and `/theory/`, then post in Discussions.

## 6. Milestones and Timeline

- **Phase 0**: Theoretical design (Dec 2025 – Complete)
- **Phase 1**: Hardware build/validation (Jan-Feb 2026)
- **Phase 2**: Data collection (Mar-Apr 2026)
- **Phase 3**: Analysis/publication (May 2026+)

## 7. Resources

- **Budget**: ~$200 for prototype
- **Tools**: GitHub for collaboration; arXiv for preprints
- **Licenses**: CERN OHL v2 (hardware), MIT (software)

## 8. Success Metrics

1. **Simulation GO/NO-GO**: Achieve $\alpha_{\text{min}} \le 10^{-10}$ in 48-hour sensitivity sweep
2. **Experimental Validation**: Measured noise floor at target frequency $\le \alpha_{\text{min, sim}}$
3. **Community Engagement**: $\ge 5$ independent replications or validation attempts
4. **Publication**: Results published in open-access journal or arXiv preprint

---

**Signed**: Adam Hind  
**Date**: December 15, 2025
