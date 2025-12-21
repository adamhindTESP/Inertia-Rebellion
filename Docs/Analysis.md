# Analysis — Signal Extraction, Demodulation, and Null Tests (Tier‑1)

This document defines the authoritative Tier‑1 analysis pipeline for the Inertia Rebellion AIRM torsion‑balance experiment.

The pipeline is:

- Deterministic  
- Pre‑registered  
- Fully reproducible  
- Strictly constrained to model‑predicted observables  

No adaptive tuning, frequency scanning, or post‑hoc selection is permitted.

---

## 1. Analysis Philosophy

Tier‑1 analysis is governed by four principles:

1. **Raw‑data primacy**  
   All analysis begins from unfiltered, timestamped firmware output.

2. **Model‑limited detection**  
   Only signals explicitly predicted by the AIRM model are tested.

3. **Phase coherence requirement**  
   A valid signal must remain phase‑coherent relative to known reference frequencies.

4. **Mandatory falsification**  
   Every positive channel has a corresponding null or control channel.  
   Failure of any null test invalidates the run.

---

## 2. Input Data Definition (Firmware v0.1)

### 2.1 Raw CSV Output

The frozen Tier‑1 firmware (`InertiaSpinner.ino`) outputs one CSV row per sample:

Time_ms,Theta_ADC,Status
12345,512,OK
13345,510,OK


**Field definitions**

- `Time_ms` — milliseconds since MCU reset (`millis()`)  
- `Theta_ADC` — raw optical‑lever ADC value (integer, 0–1023)  
- `Status` — always `"OK"` in Tier‑1 (reserved for diagnostics)

### 2.2 Calibration Pulses

Magnetic calibration pulses (serial command `C`) are not explicitly flagged in the CSV.

Their presence is inferred during analysis using:

- Known command timing  
- Observed angular response  

This behavior is intentional and documented.

---

## 3. Preprocessing (Minimal & Reversible)

Only the following preprocessing steps are permitted:

t_sec      = Time_ms / 1000.0
theta_adc  = Theta_ADC
theta_rad  = theta_adc * K


where `K` is a fixed calibration factor obtained from Tier‑1 Gate‑4 torque calibration.

**Optional (must be reported if used):**

- Removal of samples during known calibration windows (± several seconds)  
- Linear detrending over multi‑hour timescales  

No frequency‑domain filtering is allowed prior to demodulation.

---

## 4. Target Signal Model

### 4.1 AIRM Prediction

The AIRM model predicts a parametric modulation of inertia, producing a slow modulation of the torsional resonance frequency. The expected signal appears at known sideband frequencies:

f_target = f_spin ± f_sid

where:

- `f_spin = 0.001 Hz` (firmware constant)  
- `f_sid ≈ 1.16 × 10^-5 Hz` (sidereal)

### 4.2 Observable Quantity

Primary observables:

- angular displacement `theta(t)`, and/or  
- instantaneous frequency deviation `delta_f(t)` derived from phase‑based demodulation.

The same observable definition is used for all baseline and spinner runs.

---

## 5. Demodulation Procedure

### 5.1 Reference Frequencies (Fixed a priori)

Tier‑1 analysis uses only the following fixed frequencies:

'f_spin'
'f_sid'
'f_spin + f_sid'
'f_spin - f_sid'


No frequency scanning is permitted.

### 5.2 Quadrature Demodulation (Conceptual)

For a chosen reference frequency `f_ref`, the analysis forms coherent in‑phase and quadrature components of an observable `x(t)` (either `theta(t)` or `delta_f(t)`):

I = ⟨ x(t) · cos(2π f_ref t) ⟩
Q = ⟨ x(t) · sin(2π f_ref t) ⟩
A = sqrt(I^2 + Q^2)


**Implementation note:**  
In practice, the analysis may first demodulate at the carrier frequency `f0` to obtain `delta_f(t)`, and then coherently project `delta_f(t)` at `f_target`, as documented in the simulation methods. This is considered equivalent at Tier‑1.

### 5.3 Integration Time

Tier‑1 runs require 24–48 hours of continuous data to resolve sidereal sidebands and suppress noise through coherent averaging.

---

## 6. Detection Metric

### 6.1 Signal‑to‑Noise Ratio

Detection significance is quantified as:

SNR = A_signal / sigma_noise


where:

- `A_signal` is the recovered coherent amplitude at the model‑predicted frequency  
- `sigma_noise` is estimated from nearby frequencies and/or baseline runs with `alpha = 0`

### 6.2 Decision Threshold (Fixed)

- `SNR > 10` → Candidate signal (GO)  
- `SNR ≤ 10` → Null result (NO‑GO)

This threshold is fixed a priori and not tuned post‑hoc.

---

## 7. Mandatory Null & Falsification Tests

Each Tier‑1 run must include all of the following:

### 7.1 Baseline (No Spinner)

- Spinner disabled.  
- Expected: no signal at `f_spin ± f_sid`.

### 7.2 Wrong‑Frequency Test (±2–5%)

- Evaluate the identical pipeline at intentionally offset frequencies, e.g.  
  `f = (1 ± 0.02) · f_target`.  
- Expected: recovered amplitude consistent with noise floor.

### 7.3 Phase‑Scrambling

- Randomize phase segments or time‑shuffle data.  
- Expected: any coherent component vanishes.

### 7.4 Calibration‑Window Exclusion

- Exclude windows containing calibration pulses and re‑run analysis.  
- Expected: signal amplitude at `f_target` unchanged within errors.

Failure of any null or falsification test invalidates the run.

---

## 8. Cross‑Checks

Recommended cross‑checks include:

- Symmetry between `f_spin + f_sid` and `f_spin - f_sid`  
- Stability of amplitude and phase across 12‑hour sub‑windows  
- No correlation with the 1 Hz logging cadence or ADC drift  
- Absence of harmonics at `n · f_spin`

---

## 9. Reporting Requirements

Each analyzed run must report:

- Run ID: `YYYYMMDD-T1-ANALYSIS-v1`  
- Firmware version and commit hash  
- Analysis code commit or tag  
- SHA‑256 hash of raw CSV data  
- SNR at `f_spin + f_sid` (and optionally `f_spin - f_sid`)  
- Pass/Fail status for each null and falsification test

---

## 10. Interpretation Boundaries

**Permitted**

- Detecting or constraining model‑predicted modulations at `f_spin ± f_sid`  
- Translating null results into upper bounds on the AIRM coupling parameter `alpha`

**Not permitted**

- Claiming discovery of unknown or un‑modeled signals  
- Asserting physical origin without validation and independent replication  
- Using Tier‑1 analysis to replace experimental confirmation

---

**Status:** FREEZE‑READY — Tier‑1 Analysis  
**Tier‑1 Stack:** hardware + firmware + simulation + theory + analysis


