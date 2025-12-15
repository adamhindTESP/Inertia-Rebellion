# Build Guide — Inertia Rebellion Apparatus

This directory provides step-by-step instructions for assembling the **Inertia Rebellion Apparatus**, including both Tier 1 (Static Pendulum) and Tier 2 (Spinner Upgrade). Follow the guide sequentially and consult the BOM for all components. Visual aids are strongly recommended for precise assembly.

---

## Professional Assessment

This Build Guide has been reviewed for clarity, phasing, integration, and safety.

| Aspect | Assessment | Value |
|---|---|---|
| Phasing | Clear separation between Tier 1 (Validation) and Tier 2 (Science Run) | Prevents wasted effort on Tier 2 if Tier 1 fails |
| Clarity | Steps are concise and goal-oriented | Easy for any contributor to follow |
| Integration | Explicit references to BOM, CAD_FILES, and Validation Gates 1-4 | Ensures all documentation works together |
| Safety / Best Practices | Includes warnings about fibers, vibration, and documentation | Upholds safety and reproducibility standards |

---

## Tier 1: Static Pendulum Assembly

### 1.1 Purpose
Tier 1 establishes the baseline apparatus for:

- Noise floor characterization
- Calibration of torsion constant (`kappa`) and damping (`gamma`)
- Verification of angular readout resolution

> **Important:** Complete Tier 1 assembly and pass Validation Gates 1-4 before proceeding to Tier 2.

### 1.2 Required Files

- BOM: `BOM_Tier1_Static_Pendulum.csv`  
- CAD files: `/CAD_FILES/`  
- Assembly guide: this `README.md`  

### 1.3 Assembly Steps

1. **Prepare the Torsion Fiber**  
   - **Action:** Cut the Tungsten fiber to the required length (e.g., 30 cm). Secure the fiber's top end using the clamp onto the fixed support post.  
   - **Goal:** Minimize pre-twist and ensure stable mounting.  

2. **Install the Asymmetric Mass**  
   - **Action:** Attach the Carbon Fiber Rod to the lower fiber end. Secure Tungsten (heavy) and Aluminum (light) masses to the rod ends, maximizing the center-of-mass (COM) offset relative to the fiber axis.  
   - **Goal:** Verify the assembly hangs freely and is visually balanced horizontally.  

3. **Set up Optical Readout**  
   - **Action:** Mount the Laser Diode and Position Sensitive Detector (PSD) on the rigid base plate. Attach the small mirror to the dumbbell rod. Align the laser spot onto the PSD sensor center.  
   - **Goal:** Connect PSD outputs to the high-resolution ADC and verify angular resolution ≤ 1×10⁻⁸ rad/√Hz.  

4. **Install Calibration Coils**  
   - **Action:** Mount custom-wound calibration coils horizontally around the dumbbell rod. Ensure the rod magnets align within the coil center plane. Connect to DAC current source.  
   - **Goal:** Prepare for Gate 2: Torque calibration (K_I).  

5. **Validation Gates 1–4**  
   - Confirm torsion fiber integrity, readout sensitivity, damping Q, and residual motion.  
   - Only proceed to Tier 2 if all gates pass.

---

## Tier 2: Spinner Upgrade Assembly

### 2.1 Purpose
Tier 2 adds rotation to the apparatus, shifting the signal to sidereal sidebands (`f_spin ± f_sid`).

### 2.2 Required Files

- BOM: `BOM_Tier2_Spinner_Upgrade_DRAFT.md`  
- CAD files: `/CAD_FILES/`  

### 2.3 Assembly Steps

1. **Mount the Motor**  
   - **Action:** Install stepper or geared DC motor per BOM. Ensure smooth rotation (~1 rev / 1000 s).  

2. **Install Slip Ring**  
   - **Action:** Route power and signal lines through the slip ring to avoid cable twisting. Verify continuity.  

3. **Attach Rotation Encoder**  
   - **Action:** Mount encoder to track platform angle (`theta_spin`). Connect to acquisition system.  

4. **Integrate Tier 1 Pendulum**  
   - **Action:** Secure pendulum assembly to rotating platform. Check all clearances and balance.  

5. **Test Rotation and Readout**  
   - **Action:** Rotate slowly and verify the readout produces expected signals. Align with demodulation software.

---

## Notes and Best Practices

- Follow all **safety guidelines** when handling torsion fibers and heavy masses.  
- Use **high-precision components**; substitutions may reduce sensitivity.  
- Maintain a vibration-free and draft-free environment during assembly.  
- Document all measurements for traceability.  
- Include visual references wherever possible for fiber alignment, mass installation, and optical readout.

---

This README serves as the **main entry point for assembly**, linking the BOM, CAD files, and validation protocol to ensure reproducibility and contributor clarity.
