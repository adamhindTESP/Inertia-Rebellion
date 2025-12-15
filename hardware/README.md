# Bill of Materials (BOM) — Inertia Rebellion Apparatus

This directory contains the definitive **Bill of Materials (BOM)** required to construct the Inertia Rebellion Apparatus. The BOM is version-controlled and separated by build phase to facilitate iterative, budget-conscious construction.

The build is divided into **two sequential phases**:

- **Tier 1:** Static Pendulum (Required Baseline)  
- **Tier 2:** Spinner Upgrade (Required for Sidereal Search)  

> **Note:** Do not order Tier 2 components until the Tier 1 apparatus has successfully passed Validation Gates 1–4.

---

## Tier 1: Static Pendulum (~$250 USD)

This is the essential, low-cost build for establishing:

- Noise floor
- Calibration constants (`kappa`, `K_I`)
- Angular resolution

This phase is mandatory for passing the **Gold Certification Protocol**.

### 1.1 File Location

- Data File: `BOM_Tier1_Static_Pendulum.csv`  
- Build Guide: `ASSEMBLY_GUIDE.md` (See Section 1.0)

### 1.2 Key Performance Components

| Component | Description | Notes / Specifications |
|-----------|-------------|----------------------|
| Torsion Fiber | Thin metal or quartz wire | Low torsion constant: `kappa ≈ 1e-4 N·m/rad`, period `T0 ≈ 60 s` |
| Optical PSD Readout | Laser + photodiode | Angular resolution ~1e-8 rad/√Hz; external ADC recommended |
| Asymmetric Mass | Tungsten + Aluminum | Creates center-of-mass offset for future Spinner upgrade |

---

## Tier 2: Spinner Upgrade (~$150 USD)

Adds the mechanics to rotate the apparatus, shifting the physics signal from Earth’s sidereal frequency to the **two sidebands** (`f_spin ± f_sid`).

### 2.1 File Location

- Data File: `BOM_Tier2_Spinner_Upgrade_DRAFT.md` (placeholder)  

### 2.2 Key Upgrade Components

| Component | Description | Notes / Specifications |
|-----------|-------------|----------------------|
| Motor | Low-speed, high-precision stepper or geared DC motor | Smooth rotation, `f_spin ≈ 1/1000 Hz` |
| Slip Ring | For transmitting power/signals | Prevents cable twisting on rotating platform |
| Rotation Encoder | High-resolution angle measurement | Essential for correct demodulation |

---

## Notes on Sourcing and Substitutions

- **Supplier Links:** Provided as examples; local or equivalent substitutes are encouraged.  
- **Precision Components:** High-precision resistors/capacitors (0.1% tolerance) should not be substituted.  
- **CAD Files:** See `/CAD_FILES/` for 3D printable mounts, coil bobbins, and other integration parts.

---

## Usage Instructions

1. Open the spreadsheet to review all components, quantities, and specifications.  
2. Verify compatibility with your target **I0, kappa, and gamma**.  
3. Reference `methods.md` for simulation-to-hardware parameter mapping.  
4. Begin with Tier 1; proceed to Tier 2 only after passing all validation checks.

---

This README serves as the **main entry point** for the BOM and provides context for both assembly and sourcing of components. Use `BOM_Tier1_Static_Pendulum.csv` for ordering parts for the initial build.
