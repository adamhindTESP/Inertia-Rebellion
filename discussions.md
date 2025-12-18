# Discussion

## What These Simulations Do — and Do Not — Demonstrate

The simulations in this directory are **methodological**, not evidentiary.
They are designed to test whether a specific signal-processing pipeline can
recover a *known, externally injected modulation* under controlled numerical
conditions.

No claim is made that:
- anisotropic inertia exists,
- inertia can be externally modulated in reality,
- or that the modeled equation of motion represents a fundamental physical law.

The only question addressed here is:

> *If a signal of the assumed functional form were present at a given strength,
> would the analysis pipeline detect it reliably and reject nearby false signals?*

---

## Interpretation of a Numerical “GO”

A numerical **GO** outcome in these simulations means:

- The demodulation, filtering, and extraction chain is internally consistent
- The recovered signal scales correctly with injected amplitude \( \alpha \)
- The null distribution is well-behaved and Gaussian
- Matched filtering at the correct frequency outperforms nearby frequencies
- The signal-to-noise ratio exceeds the predefined decision threshold

It does **not** imply that:
- such a signal exists in nature,
- the modeled modulation is physically realizable,
- or that experimental detection is guaranteed.

Numerical GO is therefore a **necessary but not sufficient** condition
for advancing to hardware testing.

---

## Role of Null and Falsification Tests

Two failure modes are explicitly guarded against:

### 1. False Positives from Analysis Artifacts

Null runs (\( \alpha = 0 \)) establish the numerical noise floor.
Any nonzero recovered amplitude in these runs reflects:
- finite-time effects,
- filtering leakage,
- or stochastic fluctuations.

All reported signal-to-noise ratios are referenced to this null distribution,
not to idealized analytic expectations.

### 2. Frequency-Insensitive Pipelines

Falsification tests evaluate the recovered amplitude at a nearby but incorrect
frequency. A healthy pipeline must satisfy:

\[
A(f_{\mathrm{false}}) \ll A(f_{\mathrm{target}})
\]

Failure of this criterion indicates overfitting, spectral leakage,
or improper demodulation.

---

## Why a Phenomenological Model Is Used

The effective inertia modulation is introduced *by construction* as a
phenomenological term. This choice is deliberate:

- It avoids embedding speculative microphysics in the simulation
- It isolates the performance of the analysis pipeline
- It makes the falsification criteria explicit and auditable

Any physically motivated model proposed in the future would have to
reduce to this phenomenological form at the level of detectability
to be testable by the same pipeline.

---

## Noise Model Limitations

The simulations assume:
- additive Gaussian noise,
- stationarity over the run duration,
- and a known one-sided amplitude spectral density.

Real experimental systems may exhibit:
- non-Gaussian noise,
- drift,
- transient disturbances,
- or environmental couplings not represented here.

As a result, the reported sensitivities should be interpreted as **best-case**
benchmarks rather than guaranteed experimental performance.

---

## Relationship to Hardware Validation

These simulations correspond to **Tier-1 numerical validation** only.

They are intended to:
- guide required experimental sensitivity,
- inform integration time estimates,
- and identify analysis pitfalls before data is taken.

They do **not** replace:
- mechanical characterization,
- environmental isolation studies,
- calibration injections,
- or blind analysis protocols.

All physical claims must ultimately be decided by hardware measurements,
not numerical simulations.

---

## Failure Modes and Red Flags

The following outcomes should be interpreted as **NO-GO**, regardless of SNR:

- Comparable recovered amplitudes at correct and incorrect frequencies
- Strong sensitivity to filter tuning or windowing choices
- Non-Gaussian null distributions
- Recovered signals present in \( \alpha = 0 \) runs
- SNR inflation driven by trend removal or detrending artifacts

The code is structured to make these failures visible rather than hidden.

---

## Transparency and Reproducibility

All simulations:
- write full configuration metadata to disk,
- record derived parameters explicitly,
- and timestamp outputs for traceability.

Independent reproduction and criticism are not only allowed
but explicitly encouraged.

---

## Final Perspective

These simulations exist to enforce intellectual discipline.

They ensure that:
- analysis tools behave as expected,
- false confidence is minimized,
- and experimental effort is not wasted chasing numerical artifacts.

A positive numerical result is an *invitation to test hardware*,
not a conclusion about nature.
