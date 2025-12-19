# Spinner-Enabled Sensitivity Analysis

This simulation models the **spinner-enabled torsion pendulum**
used in the Inertia Rebellion Apparatus (AIRM).

It exists to answer a single question:

> *Does controlled rotation move a hypothetical inertial-anisotropy signal
> into a clean, searchable frequency channel without enhancing or fabricating it?*

---

## Why a Spinner Is Used

In the absence of rotation, any hypothetical inertial anisotropy would appear
as a slow or static modulation that is difficult to distinguish from drift,
thermal effects, or long-timescale systematics.

Introducing **controlled rotation** does **not** increase signal strength.
Instead, it **translates a hypothetical sidereal modulation into a narrow,
well-defined sideband** in frequency space.

This enables:
- Lock-in style detection
- Explicit falsification at nearby frequencies
- Separation from low-frequency noise

The spinner is therefore a **signal-labeling mechanism**, not a signal source.

---

## What Changes Compared to the Non-Spinning Case

Relative to the baseline (non-spinning) simulation:

- The target signal appears at  
  `f_target = f_spin + f_sid`
- The analysis searches for a **narrow sideband**, not broadband power
- Phase coherence becomes a primary discriminant
- Wrong-frequency collapse becomes a falsification test

No additional physics assumptions are introduced.

---

## What This Simulation Implements

The spinner-enabled model includes:

- A prescribed fractional inertia modulation:

ε(t) = α cos(2π (f_spin + f_sid) t + φ)

- A high-Q torsion pendulum equation of motion:

I₀ [1 + ε(t)] θ̈ + γ θ̇ + κ θ = 0

- Quadrature demodulation at the natural frequency
- Coherent detection at the spin–sidereal sideband
- Explicit null and wrong-frequency tests

---

## What This Simulation Does NOT Do

This simulation:

- Does **not** claim anisotropic inertia exists
- Does **not** model microscopic mechanisms
- Does **not** add signal power via rotation
- Does **not** compensate for experimental systematics
- Does **not** replace hardware validation

Rotation is treated strictly as a **known, externally imposed modulation**.

---

## Relation to Hardware

The spinner-enabled simulation defines:

- Required spin stability (timescale, not precision)
- Acceptable jitter and drift
- Minimum integration time for detectability
- Analysis expectations before hardware is built

A numerical “GO” here means only:

> *If an effect of this form existed, rotating the apparatus would make it
> detectable with the stated sensitivity.*

Reality is decided by hardware.

---

## Bottom Line

The spinner exists to **move a hypothetical signal into a testable channel**.

It does not create signals.  
It does not amplify physics.  
It makes falsification possible.

That is its only job.
