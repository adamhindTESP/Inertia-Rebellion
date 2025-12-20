# Falsification Test — Frequency Discrimination (Gate 0)

This document defines the **primary falsification test** used in the AIRM
numerical simulations to verify that the analysis pipeline is **frequency-selective**
and does **not** generate spurious coherent signals.

This test is mandatory for all Tier-1 numerical validation.

---

## Purpose

The falsification test answers a single question:

> **Does the analysis pipeline recover a signal only at the correct,
> model-predicted frequency — and collapse when evaluated elsewhere?**

A pipeline that recovers comparable amplitudes at incorrect frequencies
is **invalid**, regardless of apparent signal-to-noise ratio.

---

## Conceptual Basis

The AIRM framework predicts a coherent modulation at a **specific,
a priori defined frequency**:

\[
f_\text{true} = f_\text{spin} + f_\text{sid}
\]

The falsification test deliberately evaluates the recovered signal at a
nearby but incorrect frequency:

\[
f_\text{false} = (1 + \delta)\,f_\text{true}
\]

with a fixed offset:

\[
\delta = 0.02 \quad (2\%)
\]

This offset is chosen such that:

- It is **well outside** the Fourier resolution of a 48-hour integration
- It is **close enough** to expose spectral leakage or over-broad filters
- It does **not** overlap the correct sideband under any reasonable windowing

---

## Simulation Configuration

The falsification test uses the same physical and numerical model as the
main sensitivity simulations, including:

- High-Q torsional oscillator dynamics
- Externally prescribed inertia modulation at \( f_\text{true} \)
- Additive white Gaussian readout noise
- Quadrature demodulation at the carrier frequency \( f_0 \)
- Low-pass filtering, phase unwrapping, and frequency extraction

No additional assumptions are introduced.

---

## Analysis Procedure

For each realization:

1. Integrate the equation of motion with a nonzero injected coupling \( \alpha \)
2. Add Gaussian measurement noise
3. Perform quadrature (IQ) demodulation at the natural frequency \( f_0 \)
4. Low-pass filter I/Q channels to isolate slow phase evolution
5. Unwrap phase and remove linear trend
6. Convert phase slope to instantaneous frequency deviation:
   \[
   \delta f(t) = \frac{1}{2\pi}\,\frac{d\phi}{dt}
   \]
7. Coherently project \( \delta f(t) \) onto:
   - the **true** frequency \( f_\text{true} \)
   - the **false** frequency \( f_\text{false} \)

Recovered amplitudes are averaged over multiple noise realizations.

---

## Decision Metric

The falsification metric is the **amplitude ratio**:

\[
R = \frac{A(f_\text{false})}{A(f_\text{true})}
\]

where:
- \( A(f_\text{true}) \) is the recovered amplitude at the injected frequency
- \( A(f_\text{false}) \) is the recovered amplitude at the offset frequency

---

## Pass / Fail Criterion (Gate 0)

| Condition | Interpretation |
|---------|----------------|
| \( R < 0.1 \) | **PASS** — frequency discrimination confirmed |
| \( R \ge 0.1 \) | **FAIL** — pipeline insufficiently selective |

This threshold is fixed and not tuned post hoc.

A failure at this gate invalidates:
- sensitivity estimates,
- SNR calculations,
- and any downstream “GO” decision.

---

## Rationale

This falsification test guards against:

- Spectral leakage
- Over-broad filtering
- Accidental demodulation of unrelated components
- Pipeline bias toward coherence at arbitrary frequencies

A valid pipeline must **know where not to see a signal**.

---

## Scope and Interpretation

Passing this falsification test:

- **Does NOT** imply new physics
- **Does NOT** validate the AIRM hypothesis
- **DOES** demonstrate that the analysis pipeline is frequency-coherent and selective

This test establishes **methodological credibility only**.

---

## Status

- Falsification test: **Implemented**
- Threshold: **Fixed**
- Interpretation: **Methodological only**
- Tier-1 requirement: **Mandatory**

---

> **Principle:**  
> *A real signal survives being wrong.  
> A fake signal does not care where you look.*
