# Anisotropic Inertial Response Model (AIRM)

**Framework for Torsion-Balance Tests**

## 1. Introduction & Motivation

This document defines the Anisotropic Inertial Response Model (AIRM), a phenomenological framework for testing weak, direction-dependent variations in inertia using a laboratory torsion-balance apparatus.

The motivation is inspired by Mach's principle, which suggests that inertial properties may arise from interactions with the global mass-energy distribution of the universe. If such an interaction exists, a conceivable experimental signature would be a minuscule anisotropy: a dependence of an object's inertial response on its orientation relative to a cosmological preferred frame.

The AIRM does **not** assume such an effect exists. Instead, it introduces a dimensionless coupling parameter $\alpha$, which is to be experimentally constrained or bounded. The purpose of this framework is to define a falsifiable signal model and a corresponding detection strategy compatible with precision torsion-balance experiments.

## 2. Core Model: Time-Dependent Inertia Modulation

AIRM models a possible anisotropy as a time-varying modulation of the effective moment of inertia of the torsion pendulum:

$$I_\mathrm{eff}(t) = I_0\,[1 + \epsilon(t)],$$

where $I_0$ is the nominal moment of inertia and $\epsilon(t) \ll 1$ is a fractional modulation.

Two independent modulations combine in the laboratory frame:

- **Sidereal modulation** ($f_\mathrm{sid}$):  
  Earth's rotation modulates the orientation of the apparatus relative to any fixed cosmic anisotropy at the sidereal frequency,  
  $$f_\mathrm{sid} \approx 1.16 \times 10^{-5}\,\mathrm{Hz}.$$

- **Experimental ("spinner") modulation** ($f_\mathrm{spin}$):  
  Actively rotating the test mass at a controlled frequency,  
  $$f_\mathrm{spin} \sim 10^{-3}\,\mathrm{Hz},$$  
  shifts any anisotropic response away from low-frequency noise.

The combined fractional inertia modulation appears at a well-defined sideband frequency and is modeled as:

$$\epsilon(t) = \alpha \cos\!\left[2\pi (f_\mathrm{spin} + f_\mathrm{sid})\,t + \phi \right],$$

where:
- $\alpha \ll 1$ is the dimensionless anisotropy coupling constant
- $\phi$ is an unknown phase

The equation of motion for the torsion pendulum angle $\theta(t)$ is:

$$I_0[1 + \epsilon(t)]\,\ddot{\theta}(t) + \gamma \dot{\theta}(t) + \kappa \theta(t) = \tau_\mathrm{ext}(t),$$

where $\gamma$ is the damping coefficient, $\kappa$ is the torsion constant, and $\tau_\mathrm{ext}$ represents externally applied calibration torques.

## 3. Signal and Detection Strategy

For $\alpha \ll 1$, the inertia modulation produces a parametric frequency modulation of the pendulum's natural angular frequency

$$\omega_0 = \sqrt{\kappa / I_0}.$$

To leading order, the instantaneous frequency shift is:

$$\delta \omega(t) \approx -\frac{\omega_0}{2}\,\epsilon(t).$$

The corresponding frequency deviation in hertz is:

$$\delta f(t) = \frac{\delta \omega(t)}{2\pi}.$$

### Detection Pipeline
1. Measure the angular trajectory $\theta(t)$ using an optical lever readout.
2. Demodulate the signal at the carrier frequency $\omega_0$ using quadrature (phase-sensitive) techniques to extract the slow frequency deviation $\delta f(t)$.
3. Project $\delta f(t)$ onto a sinusoidal template at the known target frequency  
   $$f_\mathrm{target} = f_\mathrm{spin} + f_\mathrm{sid}$$  
   using matched filtering.

The recovered frequency-deviation amplitude is:

$$A_\mathrm{meas} \approx \frac{f_0 \alpha}{2},$$

where $f_0 = \omega_0 / (2\pi)$.

This linear relationship forms the basis for estimating or constraining $\alpha$.

## 4. Predicted Sensitivity

The fundamental sensitivity limit is set by the angular readout noise and the integration time.

For an optical lever with noise density $\sim 10^{-8}\,\mathrm{rad}/\sqrt{\mathrm{Hz}}$, and a torsion pendulum with:
- $f_0 \approx 0.05\,\mathrm{Hz}$
- quality factor $Q > 10^5$

numerical simulations show that a 48-hour integration can achieve sensitivity to:

$$\alpha_\mathrm{min} \lesssim 1 \times 10^{-10} \quad (\text{for SNR} > 10).$$

This threshold defines the experimental feasibility ("GO") criterion for the apparatus.

**Passing this sensitivity benchmark does not imply detection.** All physical interpretation requires successful completion of hardware validation gates, null tests, and falsification checks.

## 5. Systematic Effects & Model Scope

### Potential Confounding Effects
- Thermal drifts and gradients
- Magnetic coupling to the test mass
- Seismic and tilt noise
- Gravitational gradients
- Electronic cross-talk and timing artifacts

### Mitigation Strategy
- Shifting the signal to the sidereal sideband suppresses most laboratory-fixed systematics
- Continuous calibration torque injections verify linearity and phase fidelity
- Explicit falsification tests at nearby frequencies reject spurious coherence
- Validation gates ensure hardware behavior is understood prior to interpretation

**A failed validation or null test is treated as a NO-GO, not as evidence for new physics.**

## 6. Model Extensions (Non-Binding)

The AIRM framework can be extended in future work to include:
- Quadrupolar or higher-order sidereal harmonics
- Coupling to test-mass spin or chiral geometry
- Full tensor formulations within the Standard-Model Extension (SME)

These extensions are out of scope for the present Tier-1 experiment.

## 7. References
- Mach, E. (1883). *The Science of Mechanics*.
- Sciama, D. W. (1953). On the origin of inertia. *Monthly Notices of the Royal Astronomical Society*.
- Saulson, P. R. (1990). Thermal noise in mechanical experiments. *Physical Review D*.
- Heckel, B. R., et al. (2008). Preferred-frame tests with polarized electrons. *Physical Review D*.
- Adelberger, E. G., et al. (2009). Tests of fundamental physics with torsion balances. *Annual Review of Nuclear and Particle Science*.

---

## Final Statement

This document defines a **testable, falsifiable, and conservative** phenomenological framework.

**Passing sensitivity benchmarks validates the instrument and analysis pipeline** — not the existence of anisotropic inertia.

**Physical conclusions are drawn only from validated experimental data.**

---

**Status: FREEZE-READY**  
**Tier-1 Complete: v0.1-theory**
