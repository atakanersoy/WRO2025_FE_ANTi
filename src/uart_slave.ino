// uart_slave.ino
// Sensor microcontroller firmware for providing ToF and encoder data over UART.
// This code runs on the sensor microcontroller and handles distance sensing and odometry.
// It communicates with the main vehicle controller via UART protocol.
// Features: Dual ToF sensor reading, quadrature encoder decoding, and odometry tracking.
// Compiled in Arduino IDE.

#include <Wire.h>

// --------- SERIAL CONFIG ---------
#define SERIAL_PORT Serial1  // Serial1: External hardware UART for main communication
                             // Serial: Internal USB serial for debugging (not used in main code)

// --------- HARDWARE PIN CONFIGURATION ---------
const int ENCODER_CHANNEL_A = 2;    // Encoder quadrature input A
const int ENCODER_CHANNEL_B = 3;    // Encoder quadrature input B

// --------- TOF SENSOR ADDRESSES ---------
const int LEFT_DISTANCE_SENSOR_ADDR = 0x29;   // Left ToF sensor I2C address
const int RIGHT_DISTANCE_SENSOR_ADDR = 0x2A;  // Right ToF sensor I2C address

// --------- ENCODER CONFIGURATION ---------
volatile long encoder_count = 0;               // Raw encoder pulse count
const float PULSES_PER_MILLIMETER = 3.024f;    // Calculated pulses per mm travel

// --------- WIRELESS DISABLE ---------
void disableWireless() {
  // Disable Bluetooth radio to reduce interference
  NRF_RADIO->POWER = 0;
}

// --------- FUNCTION PROTOTYPES ---------
void encoderInterruptService();
int readDistanceSensor(int sensor_address);
void processUARTCommand(char command);

// --------- ENCODER INTERRUPT SERVICE ROUTINE ---------
void encoderInterruptService() {
  // Basic quadrature decoding with direction detection
  static uint8_t old_state = 0;
  uint8_t new_state = (digitalRead(ENCODER_CHANNEL_A) << 1) | digitalRead(ENCODER_CHANNEL_B);
  
  if ((old_state == 0x2 && new_state == 0x0) || 
      (old_state == 0x0 && new_state == 0x1) ||
      (old_state == 0x1 && new_state == 0x3) || 
      (old_state == 0x3 && new_state == 0x2)) {
    encoder_count++;
  } else if ((old_state == 0x2 && new_state == 0x3) || 
             (old_state == 0x3 && new_state == 0x1) ||
             (old_state == 0x1 && new_state == 0x0) || 
             (old_state == 0x0 && new_state == 0x2)) {
    encoder_count--;
  }
  old_state = new_state;
}

// --------- DISTANCE SENSOR READ FUNCTION ---------
int readDistanceSensor(int sensor_address) {
  // Read distance from ToF sensor
  // Returns distance in millimeters
  
  Wire.beginTransmission(sensor_address);
  Wire.write(0x14);  // Distance register
  if (Wire.endTransmission() != 0) return -1;
  
  delayMicroseconds(100);  // Small delay for sensor processing
  
  Wire.requestFrom(sensor_address, 2);
  if (Wire.available() >= 2) {
    uint8_t msb = Wire.read();
    uint8_t lsb = Wire.read();
    int distance = (msb << 8) | lsb;
    
    // Apply bounds checking
    if (distance > 0 && distance < 4000) {
      return distance;
    }
  }
  return -1;  // Invalid reading
}

// --------- UART COMMAND PROCESSOR ---------
void processUARTCommand(char command) {
  // Process commands from main vehicle controller
  int left_dist = readDistanceSensor(LEFT_DISTANCE_SENSOR_ADDR);
  int right_dist = readDistanceSensor(RIGHT_DISTANCE_SENSOR_ADDR);
  float travel_distance = encoder_count / PULSES_PER_MILLIMETER;
  
  switch (command) {
    case 'r':  // Return all sensor readings: left_tof,right_tof,encoder
      SERIAL_PORT.print(left_dist); SERIAL_PORT.print(',');
      SERIAL_PORT.print(right_dist); SERIAL_PORT.print(',');
      SERIAL_PORT.println(travel_distance, 2);
      break;
      
    case 't':  // Left sensor only
      SERIAL_PORT.println(left_dist);
      break;
      
    case 'u':  // Right sensor only  
      SERIAL_PORT.println(right_dist);
      break;
      
    case 'e':  // Encoder travel distance
      SERIAL_PORT.println(travel_distance, 2);
      break;
      
    case 'z':  // Reset encoder counter
      encoder_count = 0;
      break;
      
    default:   // Unknown command - ignore
      break;
  }
}

// --------- SETUP FUNCTION ---------
void setup() {
  // Disable wireless communications first
  disableWireless();
  
  // Initialize serial communication
  SERIAL_PORT.begin(115200);
  
  // Initialize I2C bus
  Wire.begin();
  // Default clock speed
  
  // Configure encoder hardware
  pinMode(ENCODER_CHANNEL_A, INPUT_PULLUP);
  pinMode(ENCODER_CHANNEL_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCODER_CHANNEL_A), encoderInterruptService, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_CHANNEL_B), encoderInterruptService, CHANGE);
  
  // Sensor initialization delay
  delay(100);
  
  // Send ready indicator
  SERIAL_PORT.write(0x01);  // Standard ready byte
}

// --------- MAIN LOOP ---------
void loop() {
  // Command processing loop
  if (SERIAL_PORT.available() > 0) {
    char incoming_byte = SERIAL_PORT.read();
    processUARTCommand(incoming_byte);
  }
  
  // Small delay for stability
  delay(15);
}