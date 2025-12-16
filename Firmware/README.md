# Firmware for Inertia Rebellion – Spinner Apparatus

This directory contains **Arduino firmware** for the AIRM Spinner torsion balance. It controls all Phase 1 hardware subsystems.

---

## Hardware Functions

- **Stepper Motor**: Pin 2 (STEP), Pin 3 (DIR) — f_spin = 0.001 Hz rotation  
- **Magnetic Coil**: Pin 9 (PWM) — calibration torque pulses  
- **Optical Lever**: A0 (ADC) — θ(t) readout (0–1023 raw)  
- **Serial**: USB — 1 Hz CSV logging  
  Format: `Time(ms),Theta(ADC),Status`

---

## Features

- Continuous rotation at exact AIRM sideband frequency (f_spin = 1/1000 Hz)
- Real-time θ(t) logging at 1 Hz (matches simulation sampling rate)
- Calibration mode (`C` command → 100 ms torque pulse)
- Low jitter stepper timing (<1 ms)
- Vacuum ready (no SD card; serial over USB)

---

## Quick Start

1. Install Arduino IDE from https://arduino.cc  
2. Tools → Manage Libraries → Search **AccelStepper** → Install  
3. File → Open → `InertiaSpinner.ino`  
4. Tools → Board → **Arduino Uno** (or Nano)  
5. Tools → Port → Select your Arduino  
6. Upload → Open Serial Monitor (9600 baud)

### Expected Serial Output

Inertia Spinner Firmware v0.1
Time (ms),Theta (ADC),Status
12345,512,OK
12346,510,OK
…

---

## Wiring Diagram

Arduino Uno / Nano
├── Pin 2  → A4988 STEP (via spinner rotation stage)
├── Pin 3  → A4988 DIR
├── Pin 9  → MOSFET gate → magnetic calibration coil
├── A0     → photodiode (optical lever readout)
├── GND    → common ground
└── 5V     → stepper driver Vcc (if required)

Full schematics: `/hardware/spinner_schematics.pdf`

---

## Serial Commands

- `C` — 100 ms magnetic torque pulse (calibration)
- `S` — status report  
  Example output: `rotation:OK, theta:512`

---

## Data Pipeline

Serial output (1 Hz CSV)
↓
Copy CSV → analysis/load_spinner_data.py
↓
Quadrature demodulation → δf(t)
↓
AIRM sideband detection → α < 1e-10

---

## Expansion Roadmap

- [ ] PID rotation control (stable f_spin ±1%)
- [ ] SD card logging for long vacuum runs
- [ ] Temperature monitoring for Q-factor stability
- [ ] ESP32 port with WiFi data streaming
- [ ] Real-time FFT for pre-filtering

---

## Troubleshooting

- **No rotation**: Check A4988 enable pin and current limit
- **Jerky motion**: Reduce `setMaxSpeed()` to 500
- **Noisy θ signal**: Add 10 nF capacitor from A0 to GND
- **Serial garble**: Verify 9600 baud setting

---

## Hardware Compatibility

- **Tested**: Arduino Uno R3, Arduino Nano, A4988 driver, NEMA 17 stepper  
- **Alternatives**: ESP32 (GPIO 18/19), DRV8825 driver, 28BYJ-48 stepper  

See `/hardware/BOM.md` for exact components.

---

**Phase 1 Complete** — Ready for Spinner integration testing.

