// InertiaSpinner.ino — AIRM Spinner firmware (Tier-1)
// Deterministic rotation + raw logging only. No filtering, no demodulation.

#include <AccelStepper.h>

// Pins (adjust as needed)
#define STEPPER_STEP_PIN 2
#define STEPPER_DIR_PIN 3
#define COIL_PWM_PIN 9       // Magnetic torque coil (0-255 PWM)
#define PHOTO_ANALOG_PIN A0  // Optical lever photodiode

// Stepper setup (A4988/DRV8825 driver)
AccelStepper stepper(AccelStepper::DRIVER, STEPPER_STEP_PIN, STEPPER_DIR_PIN);

// Rotation parameters
const float f_spin_hz = 0.001f;          // rotation frequency (Hz)
const long steps_per_rev = 200;          // FULL STEP count; adjust if microstepping
const float target_speed_sps = steps_per_rev * f_spin_hz; // steps/second

// Logging (1 Hz)
unsigned long last_log_ms = 0;
const unsigned long log_interval_ms = 1000;

// Calibration pulse (non-blocking)
volatile bool cal_active = false;
unsigned long cal_start_ms = 0;
const unsigned long cal_pulse_ms = 100;
const uint8_t cal_pwm = 128; // 0-255

void setup() {
  Serial.begin(9600);

  pinMode(COIL_PWM_PIN, OUTPUT);
  analogWrite(COIL_PWM_PIN, 0);

  stepper.setMaxSpeed(1000.0);
  stepper.setSpeed(target_speed_sps);

  // CSV header (matches firmware README)
  Serial.println("Time_ms,Theta_ADC,Status");
}

void loop() {
  // Keep stepper running
  stepper.runSpeed();

  // Handle serial commands (non-blocking)
  if (Serial.available()) {
    char cmd = (char)Serial.read();
    if (cmd == 'C' && !cal_active) {
      cal_active = true;
      cal_start_ms = millis();
      analogWrite(COIL_PWM_PIN, cal_pwm);
    }
  }

  // End calibration pulse (non-blocking)
  if (cal_active && (millis() - cal_start_ms >= cal_pulse_ms)) {
    analogWrite(COIL_PWM_PIN, 0);
    cal_active = false;
  }

  // Log at 1 Hz
  const unsigned long now = millis();
  if (now - last_log_ms >= log_interval_ms) {
    const int adc_raw = analogRead(PHOTO_ANALOG_PIN);

    Serial.print(now);
    Serial.print(",");
    Serial.print(adc_raw);
    Serial.print(",");
    Serial.println("OK");  // Status field

    last_log_ms = now;
  }
}
