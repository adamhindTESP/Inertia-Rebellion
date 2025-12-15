# Spinner-Enabled Sensitivity Analysis

This simulation models the **spinner-enabled torsion pendulum** for the Inertia Rebellion Apparatus (AIRM). It is designed to evaluate the system’s sensitivity to tiny anisotropic inertia modulations (α) and verify the feasibility of detecting a sidereal signal via quadrature demodulation.

---

## Overview

The simulation implements:

- Time-dependent fractional inertia modulation:  
  `ε(t) = α * cos(2π (f_spin + f_sid) t + φ)`
- Equation of motion for a high-Q torsion pendulum:  
