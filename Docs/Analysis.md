# Analysis — Signal Extraction, Demodulation, and Null Tests (Tier-1)

This document defines the **authoritative Tier-1 analysis pipeline** for the Inertia Rebellion AIRM torsion-balance experiment.

The pipeline is:
- Deterministic
- Pre-registered  
- Fully reproducible
- Strictly constrained to model-predicted observables

No adaptive tuning, frequency scanning, or post-hoc selection is permitted.

## 1. Analysis Philosophy

The Tier-1 analysis is governed by four principles:

1. **Raw-data primacy**  
   All analysis begins from unfiltered, timestamped firmware output.

2. **Model-limited detection**  
   Only signals explicitly predicted by the AIRM model are tested.

3. **Phase coherence requirement**  
   A valid signal must remain phase-coherent relative to known reference frequencies.

4. **Mandatory falsification**  
   Every positive channel has a corresponding null or control channel.

Failure of any null test invalidates the run.

## 2. Input Data Definition (Firmware v0.1)

### 2.1 Raw CSV Output

The frozen Tier-1 firmware (`InertiaSpinner.ino`) outputs **one CSV row per sample**:

Time_ms,Theta_ADC,Status
12345,512,OK
13345,510,OK


**Field definitions:**
- `Time_ms` — milliseconds since MCU reset (`millis()`)
- `Theta_ADC` — raw optical-lever ADC value (integer, 0–1023)  
- `Status` — always `"OK"` (reserved for diagnostics)

### 2.2 Calibration Pulses

Magnetic calibration pulses (`C` serial command) are **not explicitly flagged** in the CSV.

Their presence is inferred during analysis using:
- Known command timing
- Observed angular response

This behavior is intentional and documented.

## 3. Preprocessing (Minimal & Reversible)

Only the following preprocessing steps are permitted:

t = Time_ms / 1000.0          # Convert to seconds
theta_adc = Theta_ADC         # Raw ADC units  
theta_rad = theta_adc * K     # Fixed calibration factor (from Gate 4)
Optional (must be reported if used):
•	Removal of samples during known calibration windows (± several seconds)
•	Linear detrending over multi-hour timescales
No frequency-domain filtering is allowed prior to demodulation.


## 4. Target Signal Model

### 4.1 AIRM Prediction

The AIRM model predicts a parametric modulation of inertia, producing a slow modulation of the pendulum's resonance frequency.

The expected signal appears at known sideband frequencies:

$$f_\mathrm{target} = f_\mathrm{spin} \pm f_\mathrm{sid}$$

where:
- $f_\mathrm{spin} = 0.001\ \mathrm{Hz}$ (firmware constant)
- $f_\mathrm{sid} \approx 1.16\times10^{-5}\ \mathrm{Hz}$ (sidereal)

### 4.2 Observable Quantity

Primary observable: angular displacement $\theta(t)$ or derived instantaneous phase/frequency deviation $\delta f(t)$.

Same observable definition used for all baseline and spinner runs.

## 5. Demodulation Procedure

### 5.1 Reference Frequencies (Fixed a priori)

f_spin     = 0.001 Hz (firmware)
f_sid      = 1.16e-5 Hz (astronomical)  
f_spin + f_sid
f_spin - f_sid


**No frequency scanning permitted.**

### 5.2 Quadrature Demodulation

For each $f_\mathrm{ref}$:

$$I = \langle\theta(t) \cos(2\pi f_\mathrm{ref} t)\rangle$$
$$Q = \langle\theta(t) \sin(2\pi f_\mathrm{ref} t)\rangle$$
$$A = \sqrt{I^2 + Q^2}$$

### 5.3 Integration Time

24–48 hours minimum for Tier-1 runs.

## 6. Detection Metric

### 6.1 Signal-to-Noise Ratio

$$\mathrm{SNR} = \frac{A_\mathrm{signal}}{\sigma_\mathrm{noise}}$$

$\sigma_\mathrm{noise}$ from nearby frequencies or baseline runs.

### 6.2 Decision Threshold (Fixed)

**SNR > 10** → Candidate signal (GO)  
**SNR ≤ 10** → Null result (NO-GO)

## 7. Mandatory Null & Falsification Tests

### 7.1 Baseline (No-Spinner)
**Expected:** No signal at $f_\mathrm{spin} \pm f_\mathrm{sid}$

### 7.2 Wrong-Frequency (±2-5%)
**Expected:** $A \to$ noise floor

### 7.3 Phase-Scrambling  
**Expected:** Coherent signal vanishes

### 7.4 Calibration-Window Exclusion
**Expected:** Signal amplitude unchanged

## 8. Cross-Checks

- Symmetry between $f_\mathrm{spin}+f_\mathrm{sid}$ and $f_\mathrm{spin}-f_\mathrm{sid}$
- Stability across 12h windows
- No correlation with 1 Hz logging or ADC drift
- No $f_\mathrm{spin}$ harmonics

## 9. Reporting Requirements

Run ID: YYYYMMDD-T1-ANALYSIS-v1
Firmware: v0.1 [commit]
Data SHA256: [hash]
SNR(f_spin+f_sid): X.XX ± 0.XX
Null tests: [PASS/FAIL]


## 10. Interpretation Boundaries

**Can do:**
- Detect/constrain model-predicted modulations
- Establish $\alpha$ upper bounds

**Cannot do:**
- Identify unknown signals
- Prove physical origin
- Replace replication

