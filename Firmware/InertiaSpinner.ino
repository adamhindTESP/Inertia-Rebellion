// InertiaSpinner.ino - Firmware for Spinner Torsion Balance
#include <AccelStepper.h>  // ← FIXED

// Pins (adjust as needed)
#define STEPPER_STEP_PIN 2
#define STEPPER_DIR_PIN 3
#define COIL_PWM_PIN 9       // Magnetic torque coil (0-255 PWM)
#define PHOTO_ANALOG_PIN A0  // Optical lever photodiode

// Stepper setup (A4988 driver, 200 steps/rev)
AccelStepper stepper(AccelStepper::DRIVER, STEPPER_STEP_PIN, STEPPER_DIR_PIN);
float f_spin = 0.001;  // Hz (rotation freq)
long steps_per_rev = 200;  // Adjust for your stepper/microstepping
long target_speed = steps_per_rev * f_spin;  // Steps/s

// Data acquisition
unsigned long last_log = 0;
unsigned long log_interval = 1000;  // ms (1 Hz logging)

// Setup
void setup() {
  Serial.begin(9600);
  pinMode(COIL_PWM_PIN, OUTPUT);
  analogWrite(COIL_PWM_PIN, 0);  // Coil off

  stepper.setMaxSpeed(1000);     // Max steps/s
  stepper.setSpeed(target_speed); // Set rotation speed

  Serial.println("Inertia Spinner Firmware v0.1");
  Serial.println("Time (ms), Theta (ADC), Status");
}

// Loop
void loop() {
  // Rotate stepper
  stepper.runSpeed();

  // Log data
  if (millis() - last_log >= log_interval) {
    int theta_raw = analogRead(PHOTO_ANALOG_PIN);  // Read photodiode (0-1023)
    Serial.print(millis());
    Serial.print(",");
    Serial.print(theta_raw);
    Serial.print(",");
    Serial.println("OK");  // Add more status if needed
    last_log = millis();
  }

  // Optional: Calibration torque (e.g., via serial command)
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'C') {  // Calibrate: brief torque pulse
      analogWrite(COIL_PWM_PIN, 128);  // Half power
      delay(100);
      analogWrite(COIL_PWM_PIN, 0);
    }
  }
}
