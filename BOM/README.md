# Bill of Materials (BOM) — Inertia Rebellion Apparatus

This folder contains the full Bill of Materials (BOM) for building the Inertia Rebellion torsion pendulum and spinner-enabled apparatus.  

The BOM includes **all mechanical, electrical, and sensor components** required to replicate the experiment, along with recommended specifications and quantities.  

---

## Key Notes

- All components listed are **commercially available** from electronics suppliers (Digi-Key, Mouser, Amazon, etc.) unless otherwise noted.  
- Quantities reflect a **single experimental setup**.  
- Where tolerances matter (resistors, torsion constants, optical sensors), the recommended values are provided.  
- For electronics and sensors, see the **methods.md** for parameter context (e.g., damping, readout noise).  

---

## Example BOM Table

| Component | Description | Quantity | Notes / Specifications | Supplier Link |
|-----------|-------------|----------|----------------------|---------------|
| Torsion Fiber | Thin metal wire or quartz fiber | 1 | Length & diameter tuned to achieve I0 ≈ 1e-3 kg·m² | [Example](https://www.mcmaster.com/) |
| Disk / Rotor | Aluminum or brass | 1 | Mass and radius chosen to achieve desired moment of inertia | Local machine shop |
| Motor / Spinner | Precision stepper or brushless motor | 1 | Allows controlled slow rotation (f_spin ≈ 1/1000 Hz) | [Digi-Key](https://www.digikey.com/) |
| Optical Lever | Laser + photodiode | 1 | Readout of pendulum angle with noise ~1e-8 rad/√Hz | [Thorlabs](https://www.thorlabs.com/) |
| Capacitors | For optional low-noise electronics | Various | Small value MLCC or film types | Mouser / Digikey |
| Resistors | High-precision | Various | 0.01% tolerance recommended | Mouser / Digikey |
| Electronics Board | Custom PCB or breadboard | 1 | Hosts MOSFET / heater or readout electronics | DIY |
| Mechanical Frame | Aluminum or steel | 1 | Stable base to minimize vibration | Local fabrication |
| Miscellaneous | Screws, mounts, alignment tools | N/A | Necessary for assembly | Hardware store |

---

### File in this folder

- `hand_warmer_BOM.csv` or `.xlsx`: Complete, detailed spreadsheet of components with quantities, supplier links, and notes.

---

## How to Use

1. Open the spreadsheet to check **components, quantities, and recommended specifications**.  
2. Verify compatibility with your **desired I0, torsion constant kappa, and damping gamma**.  
3. Reference **methods.md** for component-specific parameters in simulation and hardware design.  
