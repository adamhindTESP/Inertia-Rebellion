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

### Result Summary (Simulation Only)

- Null background frequency noise:

$$
(4.32 \pm 1.15) \times 10^{-8}\ \text{Hz}
$$

- Minimum detectable coupling (numerical sensitivity):

$$
\alpha_{\text{min}} \lesssim 1 \times 10^{-10}
$$

**Theoretical Sensitivity:** ✅ **$10^{-10}$ achievable** (simulation)  
**Hardware Status:** Phase 1 validation required before physics constraints are possible.

No physical data have yet been collected; all results presented here are derived exclusively from numerical sensitivity studies.

The full sensitivity analysis is implemented in:

**`/simulation/airm_full_analysis.py`**

**See [STATUS.md](STATUS.md) for current project maturity and explicit non-goals.**
