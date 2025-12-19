## 6. Serial Data Logging

The firmware outputs raw, time-stamped measurements over USB serial
for offline analysis. No filtering, demodulation, or signal conditioning
is performed onboard.

### 6.1 Output Format

The firmware emits **one CSV line per sample** at a fixed rate.

**CSV header:**

Time_ms,Theta_ADC,Status

**Field definitions:**

- `Time_ms`  
  Milliseconds since MCU reset, obtained from `millis()`.

- `Theta_ADC`  
  Raw ADC reading from the optical lever photodiode  
  (integer range: 0–1023).

- `Status`  
  ASCII status field. Currently always `"OK"` during normal operation.
  Reserved for future fault or diagnostic flags.

**Example output:**

Time_ms,Theta_ADC,Status
12345,512,OK
13345,510,OK

No header row is required for parsing, but one is emitted at startup
for human readability.

---

### 6.2 Sampling Rate

- Default logging rate: **1 Hz**
- Controlled via `log_interval = 1000 ms`

This rate is chosen to:
- Match numerical simulation assumptions
- Minimize serial bandwidth usage
- Avoid implicit filtering

Higher sampling rates are not required for the Tier-1 validation pipeline.

---

### 6.3 Calibration Pulse Behavior

When the serial command:

C

is received:

- A **brief magnetic calibration pulse** is applied
- Pulse duration: ~100 ms
- Coil power: fixed PWM value

**Important:**  
Calibration pulses are **not explicitly flagged in the CSV output**.
Their presence must be inferred during analysis by:
- Known command timing
- Observed angular response

This behavior is intentional and documented.
