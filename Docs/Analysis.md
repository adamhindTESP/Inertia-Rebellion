# Analysis — Signal Extraction, Demodulation, and Null Tests (Tier-1)

This document defines the **authoritative Tier-1 analysis pipeline** for the Inertia Rebellion AIRM torsion-balance experiment.

The pipeline is:

- Deterministic  
- Pre-registered  
- Fully reproducible  
- Strictly constrained to model-predicted observables  

No adaptive tuning, frequency scanning, or post-hoc selection is permitted.

---

## 1. Analysis Philosophy

Tier-1 analysis is governed by four principles:

1. **Raw-data primacy**  
   All analysis begins from unfiltered, timestamped firmware output.

2. **Model-limited detection**  
   Only signals explicitly predicted by the AIRM model are tested.

3. **Phase coherence requirement**  
   A valid signal must remain phase-coherent relative to known reference frequencies.

4. **Mandatory falsification**  
   Every positive channel has a corresponding null or control channel.  
   Failure of any null test invalidates the run.

---

## 2. Input Data Definition (Firmware v0.1)

### 2.1 Raw CSV Output

The frozen Tier-1 firmware (`InertiaSpinner.ino`) outputs **one CSV row per sample**:

Time_ms,Theta_ADC,Status
12345,512,OK
13345,510,OK

**Field definitions**

- `Time_ms` — milliseconds since MCU reset (`millis()`)  
- `Theta_ADC` — raw optical-lever ADC value (integer, 0–1023)  
- `Status` — always `"OK"` in Tier-1 (reserved for diagnostics)

### 2.2 Calibration Pulses

Magnetic calibration pulses (serial command `C`) are **not explicitly flagged** in the CSV.

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

where `K` is a fixed calibration factor obtained from Tier-1 Gate-4 torque calibration.

**Optional (must be reported if used):**

- Removal of samples during known calibration windows (± several seconds)  
- Linear detrending over multi-hour timescales  

**No frequency-domain filtering** is allowed prior to demodulation.

---

## 4. Target Signal Model

### 4.1 AIRM Prediction

The AIRM model predicts a parametric modulation of inertia, producing a slow modulation of the torsional resonance frequency. The expected signal appears at known sideband frequencies:

\[
f_\text{target} = f_\text{spin} \pm f_\text{sid}
\]

where:

- \(f_\text{spin} = 0.001\ \text{Hz}\) (firmware constant)  
- \(f_\text{sid} \approx 1.16\times10^{-5}\ \text{Hz}\) (sidereal)

### 4.2 Observable Quantity

Primary observable(s):

- angular displacement \(\theta(t)\), and/or  
- instantaneous frequency deviation \(\delta f(t)\) derived from phase-based demodulation.

The same observable definition is used for all baseline and spinner runs.

---

## 5. Demodulation Procedure

### 5.1 Reference Frequencies (Fixed a priori)

Tier-1 analysis uses only the following fixed frequencies:

- \(f_\text{spin}\)  
- \(f_\text{sid}\)  
- \(f_\text{spin} + f_\text{sid}\)  
- \(f_\text{spin} - f_\text{sid}\)

**No frequency scanning is permitted.**

### 5.2 Quadrature Demodulation (Conceptual)

For a chosen reference frequency \(f_\text{ref}\), the analysis forms coherent in-phase and quadrature components of an observable \(x(t)\) (either \(\theta(t)\) or \(\delta f(t)\)):

\[
I = \langle x(t)\cos(2\pi f_\text{ref} t)\rangle,\quad
Q = \langle x(t)\sin(2\pi f_\text{ref} t)\rangle
\]

The recovered amplitude is:

\[
A = \sqrt{I^2 + Q^2}.
\]

**Implementation note:**  
In practice, the analysis may first demodulate at the carrier frequency \(f_0\) to obtain \(\delta f(t)\), and then coherently project \(\delta f(t)\) at \(f_\text{target}\), as documented in the simulation methods. This is considered equivalent at Tier-1.

### 5.3 Integration Time

Tier-1 runs require **24–48 hours** of continuous data to resolve sidereal sidebands and suppress noise through coherent averaging.

---

## 6. Detection Metric

### 6.1 Signal-to-Noise Ratio

Detection significance is quantified as:

\[
\text{SNR} = \frac{A_\text{signal}}{\sigma_\text{noise}},
\]

where:

- \(A_\text{signal}\) is the recovered coherent amplitude at the model-predicted frequency,  
- \(\sigma_\text{noise}\) is estimated from nearby frequencies and/or baseline runs with \(\alpha = 0\).

### 6.2 Decision Threshold (Fixed)

- **SNR > 10** → Candidate signal (**GO**)  
- **SNR ≤ 10** → Null result (**NO-GO**)

This threshold is fixed a priori and not tuned post-hoc.

---

## 7. Mandatory Null & Falsification Tests

Each Tier-1 run must include all of the following:

### 7.1 Baseline (No Spinner)

- Spinner disabled.  
- **Expected:** No signal at \(f_\text{spin} \pm f_\text{sid}\).

### 7.2 Wrong-Frequency Test (±2–5%)

- Evaluate the identical pipeline at intentionally offset frequencies  
  (e.g., \(f = (1\pm0.02)f_\text{target}\)).  
- **Expected:** Recovered amplitude consistent with noise floor.

### 7.3 Phase-Scrambling

- Randomize phase segments or time-shuffle data.  
- **Expected:** Any coherent component vanishes.

### 7.4 Calibration-Window Exclusion

- Exclude windows containing calibration pulses and re-run analysis.  
- **Expected:** Signal amplitude at \(f_\text{target}\) unchanged within errors.

Failure of any null or falsification test invalidates the run.

---

## 8. Cross-Checks

Recommended cross-checks include:

- Symmetry between \(f_\text{spin}+f_\text{sid}\) and \(f_\text{spin}-f_\text{sid}\)  
- Stability of amplitude and phase across 12-hour sub-windows  
- No correlation with the 1-Hz logging cadence or ADC drift  
- Absence of harmonics at \(n f_\text{spin}\)

---

## 9. Reporting Requirements

Each analyzed run must report:

- Run ID: `YYYYMMDD-T1-ANALYSIS-v1`  
- Firmware version and commit hash  
- Analysis code commit or tag  
- SHA-256 hash of raw CSV data  
- SNR at \(f_\text{spin}+f_\text{sid}\) (and optionally \(f_\text{spin}-f_\text{sid}\))  
- Pass/Fail status for each null and falsification test

---

## 10. Interpretation Boundaries

**Permitted**

- Detecting or constraining model-predicted modulations at \(f_\text{spin}\pm f_\text{sid}\)  
- Translating null results into upper bounds on the AIRM coupling parameter \(\alpha\)

**Not permitted**

- Claiming discovery of unknown or un-modeled signals  
- Asserting physical origin without validation and independent replication  
- Using Tier-1 analysis to replace experimental confirmation

---

**Status:** **FREEZE-READY — Tier-1 Analysis**  
**Tier-1 Stack:** hardware + firmware + simulation + theory + analysis
