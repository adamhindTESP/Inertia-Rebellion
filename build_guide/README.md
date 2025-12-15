# Build Guide — Inertia Rebellion Apparatus

This directory contains instructions for assembling the **Inertia Rebellion Apparatus**, including both Tier 1 (Static Pendulum) and Tier 2 (Spinner Upgrade) builds. Follow the steps sequentially and consult the BOM for all component specifications.

---

## Tier 1: Static Pendulum Assembly

### 1.1 Purpose
The Tier 1 build establishes the baseline apparatus for:

- Noise floor characterization
- Calibration of torsion constant (`kappa`) and damping (`gamma`)
- Verification of angular readout resolution

> **Important:** Complete Tier 1 assembly and validation before proceeding to Tier 2.

### 1.2 Required Files

- BOM: `BOM_Tier1_Static_Pendulum.csv`  
- Assembly instructions: This guide (`README.md`)  
- CAD files: `/CAD_FILES/` (mounts, bobbins, etc.)

### 1.3 Assembly Steps

1. **Prepare the torsion fiber**  
   - Cut to required length; ensure minimal pre-twist.  
   - Mount securely between support posts.

2. **Install the asymmetric mass**  
   - Attach Tungsten and Aluminum masses according to center-of-mass offset diagram.  
   - Verify balance and alignment.

3. **Set up optical readout**  
   - Position laser and photodiode assembly.  
   - Connect to external ADC module.  
   - Verify angular resolution (~1e-8 rad/√Hz).

4. **Initial calibration**  
   - Measure natural period `T0` and calculate torsion constant `kappa`.  
   - Record baseline noise PSD.

5. **Validation Gates 1–4**  
   - Confirm torsion fiber integrity, readout sensitivity, damping Q, and residual motion.  
   - Only proceed to Tier 2 if all gates pass.

---

## Tier 2: Spinner Upgrade Assembly

### 2.1 Purpose
Tier 2 introduces rotation to the apparatus, enabling detection of sidereal modulation sidebands (`f_spin ± f_sid`).

### 2.2 Required Files

- BOM: `BOM_Tier2_Spinner_Upgrade_DRAFT.md`  
- CAD files: `/CAD_FILES/` (motor mounts, slip rings, rotating platform)  

### 2.3 Assembly Steps

1. **Mount the motor**  
   - Use stepper or geared DC motor as specified in BOM.  
   - Ensure smooth rotation (~1 rev / 1000 s).

2. **Install slip ring**  
   - Route power and signal lines through the slip ring to avoid cable twisting.  
   - Verify electrical continuity.

3. **Attach rotation encoder**  
   - Mount encoder to track instantaneous platform angle (`theta_spin`).  
   - Connect encoder signals to data acquisition system.

4. **Integrate with Tier 1 pendulum**  
   - Secure pendulum assembly onto rotating platform.  
   - Confirm all clearances and balance.

5. **Test rotation and readout**  
   - Rotate slowly and verify the readout produces expected signals.  
   - Check alignment with demodulation software.

---

## Notes and Best Practices

- Follow all **safety guidelines** when handling torsion fibers and heavy masses.  
- Use **high-precision components**; substitutions may reduce sensitivity.  
- Keep assembly area free from vibration and drafts to maintain measurement accuracy.  
- Document all measurements in your lab notebook for traceability.  

---

This README serves as the main entry point for the build guide and provides context for **step-by-step assembly**, safety, and validation. Use it alongside the BOM and CAD files for a successful build.
