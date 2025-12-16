# Analysis — Signal Extraction, Demodulation, and Null Tests

This document defines the **exact analysis pipeline** used to extract candidate AIRM signals from raw torsion-pendulum data and to reject false positives through predefined null tests.

The analysis is fully deterministic, pre-registered in structure, and designed to be reproducible by independent users using only the logged data files.

---

## 1. Analysis Philosophy

The analysis is guided by four principles:

1. **Raw-data primacy** — All analysis begins from unfiltered, timestamped measurements.
2. **Model-driven detection** — Only signals predicted by the AIRM model are tested.
3. **Phase coherence requirement** — Detection requires phase stability relative to known reference frequencies.
4. **Mandatory falsification** — Every positive channel has a corresponding null channel.

No adaptive tuning, frequency fishing, or post-hoc selection is permitted.

---

## 2. Input Data Definition

### 2.1 Raw Data Stream

The firmware outputs one CSV record per sample with the following fields:

- `timestamp_ms` — milliseconds since MCU reset
- `adc_raw` — optical lever readout (0–1023)
- `step_count` — cumulative stepper motor index
- `cal_flag` — 1 during calibration pulse, 0 otherwise

No filtering, averaging, or demodulation occurs in firmware.

---

### 2.2 Preprocessing (Minimal and Reversible)

The following preprocessing steps are permitted:

- Conversion of `adc_raw` to angular displacement using a fixed calibration factor
- Removal of samples flagged during calibration pulses (optional)
- Linear detrending over long timescales (hours), if required

No frequency-domain filtering is applied prior to demodulation.

---

## 3. Target Signal Model

### 3.1 AIRM Prediction

The AIRM model predicts a modulation of the effective moment of inertia:

- Modulation frequency components at  
  `f_spin ± f_sid`

where:

- `f_spin` is the controlled rotation frequency
- `f_sid` is the sidereal frequency

The observable is a **slow modulation of the pendulum’s resonance frequency or phase**, not a direct torque at `f_spin`.

---

### 3.2 Observable Quantity

The primary observable used in analysis is:

- Angular displacement θ(t), or
- Instantaneous phase / frequency deviation derived from θ(t)

The exact observable must be consistent across baseline and spinner-enabled runs.

---

## 4. Demodulation Procedure

### 4.1 Reference Frequencies

All reference frequencies are defined *a priori*:

- `f_spin` — measured from step timing
- `f_sid` — fixed astronomical constant
- Sidebands: `f_spin + f_sid`, `f_spin - f_sid`

No frequency scanning is allowed.

---

### 4.2 Quadrature Demodulation

For each target frequency `f_ref`, the signal is projected onto orthogonal basis functions:

- `cos(2π f_ref t)`
- `sin(2π f_ref t)`

This yields in-phase (I) and quadrature (Q) components.

The recovered amplitude is:

- `A = sqrt(I² + Q²)`

This method is phase-agnostic and immune to unknown phase offsets.

---

### 4.3 Integration Time

Demodulated signals are averaged over long durations (typically 24–48 hours) to suppress broadband noise.

Shorter integrations are permitted only for calibration and diagnostics.

---

## 5. Detection Metric

### 5.1 Signal-to-Noise Ratio (SNR)

Detection significance is quantified using:

- `SNR = A_signal / σ_noise`

where:

- `A_signal` is the recovered amplitude at the target frequency
- `σ_noise` is estimated from nearby off-target frequencies or baseline runs

---

### 5.2 Decision Threshold

The predefined detection criterion is:

- **SNR > 10** → Candidate signal (GO)
- **SNR ≤ 10** → Null result (NO-GO)

This threshold is fixed and not adjusted post hoc.

---

## 6. Null and Falsification Tests

Every analysis run must include the following null tests.

---

### 6.1 Baseline (No-Spinner) Test

**Procedure:**
- Perform identical analysis on data with rotation disabled.

**Expected Result:**
- No signal at `f_spin ± f_sid`

**Failure Condition:**
- Any statistically significant signal invalidates the dataset.

---

### 6.2 Wrong-Frequency Demodulation

**Procedure:**
- Demodulate at a frequency offset from the true sideband (e.g., +1–5%).

**Expected Result:**
- Signal amplitude collapses to noise floor.

**Purpose:**
- Confirms phase coherence requirement.

---

### 6.3 Phase Scrambling Test

**Procedure:**
- Randomize phase segments of the time series prior to demodulation.

**Expected Result:**
- Coherent signal vanishes.

---

### 6.4 Calibration-Flag Exclusion

**Procedure:**
- Remove all samples during calibration pulses.
- Repeat analysis.

**Expected Result:**
- Recovered signal unchanged.

---

## 7. Cross-Checks

The following consistency checks are performed:

- Sideband symmetry: `f_spin + f_sid` and `f_spin - f_sid`
- Stability across independent time windows
- Absence of correlation with step timing harmonics
- Independence from ADC mean offset

---

## 8. Reporting Requirements

Any reported result must include:

- Full description of preprocessing steps
- Exact reference frequencies used
- Integration duration
- All null-test outcomes
- Firmware and analysis version identifiers

No partial reporting is permitted.

---

## 9. Interpretation Boundaries

This analysis pipeline can:

- Detect or constrain coherent, model-predicted modulations
- Establish upper bounds on coupling strength

It cannot:

- Identify unknown signal morphologies
- Prove physical origin
- Replace independent replication

---

## 10. Status

- Analysis pipeline defined: Yes
- Null tests mandatory: Yes
- Detection thresholds fixed: Yes
- Reproducibility enabled: Yes

---

> **Principle:**  
> *A signal is not what appears — it is what survives being wrong.*
