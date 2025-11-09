# open.py
# Vehicle control for open challenge maintaining distance to inner wall.
# MicroPython code.
# This script controls an autonomous vehicle in an open course challenge.
# It uses a camera for black wall detection to follow the inner wall, combined with IMU sensor fusion,
# gyroscope for heading, encoder for odometry, and front ToF sensor for distance measurement.
# The vehicle navigates a rectangular course, maintains consistent distance to the inner wall using camera guidance,
# detects corners using orange/blue markers, and performs precise 90-degree turns at each corner.
# The vehicle optimizes speed for straight sections and slows down for cornering maneuvers.

import pyb
from machine import Pin, UART, SPI, I2C
import math
import sensor

# Initialize camera sensor
sensor.reset()  # Reset camera settings
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 for color detection
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.set_vflip(True)  # Vertically flip the image for reverse mounting
sensor.set_hmirror(True)  # Horizontally mirror the image for reverse mounting
sensor.skip_frames(time=500)  # Skip initial frames to stabilize the sensor

# Gyroscope setup (LSM6DSOX) for reading X-axis angular rate
spi = SPI(5, baudrate=1000000, polarity=1, phase=1)  # Initialize SPI bus 5
cs_pin = Pin("PF6", Pin.OUT_PP, Pin.PULL_UP)  # Chip select pin for gyro

def read_gyro():
    # Read low and high bytes from OUTX_L_G and OUTX_H_G registers
    cs_pin.low()
    spi.write(bytearray([0x28 | 0x80]))  # Address for OUTX_L_G with read bit
    low = spi.read(1)[0]
    spi.write(bytearray([0x29 | 0x80]))  # Address for OUTX_H_G with read bit
    high = spi.read(1)[0]
    cs_pin.high()
    raw = (high << 8) | low  # Combine high and low bytes
    if raw >= 32768:
        raw -= 65536  # Convert to signed 16-bit value
    return raw * 0.035  # Scale raw value to degrees per second (adjust scale factor based on sensitivity setting)

# Front ToF sensor setup for initial distance measurement
i2c = I2C(2)  # Initialize I2C bus 2
tof_address = 0x29  # Default address for VL53L1X front ToF sensor

def read_distance():
    # Read 2 bytes from register 0x1E (distance result)
    result = i2c.readfrom_mem(tof_address, 0x1E, 2)
    return (result[0] << 8) | result[1]  # Combine to get distance in mm

# Servo setup for steering
SERVO_MIN = 1525  # Minimum pulse width for servo
SERVO_CENTER = 2200  # Center pulse width
SERVO_MAX = 2900  # Maximum pulse width
servo_timer = pyb.Timer(4, freq=50)  # Timer for 50Hz PWM
servo = servo_timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin(2))  # PWM on used pin 2
servo.pulse_width(SERVO_CENTER)  # Initialize to center

def set_steering(pos):
    # Convert position (0-480) to pulse width, clamped to min/max
    pos = max(0, min(480, pos))
    if pos < 240:
        pulse = SERVO_CENTER - (240 - pos) * (SERVO_CENTER - SERVO_MIN) // 240
    else:
        pulse = SERVO_CENTER + (pos - 240) * (SERVO_MAX - SERVO_CENTER) // 240
    servo.pulse_width(int(pulse))

# Motor setup for drive
motor_timer = pyb.Timer(1, freq=20000)  # High freq for smooth PWM
motor_forward = motor_timer.channel(2, pyb.Timer.PWM, pin=Pin(3))  # Forward PWM on pin 3
motor_reverse = motor_timer.channel(3, pyb.Timer.PWM, pin=Pin(6))  # Reverse PWM on pin 6

def set_speed(speed):
    # Set motor speed (-100 to 100), using PWM percent
    speed = max(-100, min(100, int(speed)))
    if speed > 0:
        motor_forward.pulse_width_percent(100)
        motor_reverse.pulse_width_percent(100 - speed)
    elif speed == 0:
        motor_forward.pulse_width_percent(100)
        motor_reverse.pulse_width_percent(100)
    else:
        motor_forward.pulse_width_percent(100 + speed)
        motor_reverse.pulse_width_percent(100)

set_speed(0)  # Start stopped

# UART for communication with slave MCU (sensors: left/right ToF, encoder)
uart = UART(9, baudrate=115200, bits=8, parity=None, stop=1)

tof_left = 0  # Left ToF distance
tof_right = 0  # Right ToF distance
encoder = 0.0  # Encoder value (distance in mm)
uart_buffer = b''  # Buffer for UART data

def fetch_data(command, timeout=50):
    # Send command to slave and parse response
    global tof_left, tof_right, encoder, uart_buffer
    uart.write(command)
    if command in (b'z', b'p'): return True  # No response needed
    start_time = pyb.millis()
    while pyb.elapsed_millis(start_time) < timeout:
        if uart.any():
            uart_buffer += uart.read(uart.any())
            if b'\n' in uart_buffer:
                line, uart_buffer = uart_buffer.split(b'\n', 1)
                if command == b'r' and line.count(b',') == 2:
                    parts = line.split(b',')
                    tof_left = int(parts[0])
                    tof_right = int(parts[1])
                    encoder = float(parts[2])
                    return True
    return False  # Timeout

# Button for start
button_pin = Pin('A0', Pin.IN, Pin.PULL_UP)
def wait_button(release=True):
    # Wait for button press (and release if specified)
    while button_pin.value(): pyb.delay(1)
    if release:
        while not button_pin.value(): pyb.delay(1)

# RGB LED for status
led_pins = [pyb.Pin(p, pyb.Pin.OUT_PP) for p in ("PE3", "PC13", "PF4")]  # R, G, B pins
def set_led(color):
    # Set LED color based on string code (e.g., 'R' red, 'G' green, 'M' magenta, 'off')
    led_pins[0].value(0 if color in 'ROMWY' else 1)  # Red on/low for certain colors
    led_pins[1].value(0 if color in 'GOCWY' and (color != 'O' or pyb.millis() % 1 < 1) else 1)  # Green, with blink for 'O'
    led_pins[2].value(0 if color in 'BCMW' else 1)  # Blue

# Camera parameters
CAM_WIDTH = 316  # Effective width after windowing if applied
CAM_HEIGHT = 115  # Effective height
CAM_CENTER = CAM_WIDTH // 2  # Center for error calculation

# Color thresholds in LAB for find_blobs (L_min, L_max, A_min, A_max, B_min, B_max)
th = {
    "BK": [(0, 25, -10, 20, -15, 10)],  # Black threshold for wall following
    "O": [(5, 60, 5, 20, 0, 25)],  # Orange for corner detection
    "B": [(5, 60, 5, 80, -80, -25)],  # Blue for corner detection
}

def detect_region(color_key, roi=(0, 0, CAM_WIDTH, CAM_HEIGHT)):
    # Use find_blobs to detect regions of the specified color threshold
    # Returns error (deviation from center) and detection flag
    img = sensor.snapshot()  # Capture image
    blobs = img.find_blobs(th[color_key], roi=roi, pixels_threshold=200, area_threshold=200, merge=True)  # Find blobs with params
    if blobs:
        # Take the largest blob for reliability
        largest_blob = max(blobs, key=lambda b: b.pixels())
        center_x = largest_blob.cx()  # Centroid x
        return center_x - CAM_CENTER, True  # Error from center
    return 0, False  # No detection

# Navigation parameters
direction = 0  # 0 unknown, 1 for CW, -1 for CCW
corner_count = 0  # Track corners navigated
corner_cd = 2000  # Min time ms between corner detections
last_corner_time = pyb.millis()  # Last corner detection time
min_fs, max_fs = 55, 75  # Full speeds
current_speed = max_fs  # Current motor speed
target_speed = max_fs  # Target speed for ramp
turn_tol = 5  # Tolerance for turn completion in degrees
state = 'initial_forward'  # State machine start
target_heading = 0  # Desired heading
no_black_count = 0  # Counter for no black line detection
min_segment_dist = 300  # Minimum distance before allowing turn
final_forward = 475  # Final forward distance after last corner

# PID parameters
kp, ki, kd = 2, 0.001, 1  # Gains
pid_integral = 0  # Integral term
last_error = 0  # Last error for derivative

angle = 0.0  # Current angle from gyro integration
odometry_x = 0.0  # Odometry X position
odometry_y = 0.0  # Odometry Y position
last_enc = 0.0  # Last encoder value

# Wait for slave ready
start = pyb.millis()
while pyb.elapsed_millis(start) < 10000:
    if uart.any() and uart.read(1) == b'\x01': break
uart.read(uart.any())  # Clear buffer

fetch_data(b'r')  # Initial fetch

# ---------- IMU CALIBRATION ------------
# Perform 10-second gyroscope calibration to determine zero offset
# This collects gyro samples to calculate average drift and improve heading accuracy
calibration_samples = 1000
calibration_sum = 0.0
calibration_count = 0
calibration_start = pyb.millis()

while calibration_count < calibration_samples and pyb.elapsed_millis(calibration_start) < 10000:
    gyro_sample = read_gyro()
    calibration_sum += gyro_sample
    calibration_count += 1
    pyb.delay(10)  # 10ms between samples

if calibration_count > 0:
    gyro_zero_offset = calibration_sum / calibration_count
else:
    gyro_zero_offset = 0.0

set_led("B")  # Blue LED for waiting
wait_button()  # Wait for start button
set_led("off")  # Off after start

fetch_data(b'z')  # Reset slave
start = pyb.millis()
last_time = pyb.millis()
error_flag = 0

try:
    # Section 1: Main Navigation Loop
    # This loop navigates the open course by following the inner wall using camera detection.
    # It uses front ToF sensor for initial approach, then switches to camera-based wall following.
    # The vehicle maintains consistent distance to the wall, detects corners using orange/blue markers,
    # and performs precise 90-degree turns at each corner.
    # States: 'initial_forward' -> 'follow_wall' -> 'turn_corner' -> 'follow_wall'
    # Uses IMU for initial straight driving, then camera for wall following with PID control.
    while True:
        fetch_data(b'r')
        now = pyb.millis()
        dt = (now - last_time) / 1000.0
        last_time = now
        gyro = read_gyro() - gyro_zero_offset  # Apply zero offset for accurate integration
        angle += gyro * dt
        delta_enc = encoder - last_enc
        last_enc = encoder
        odometry_x += delta_enc * math.cos(math.radians(angle))
        odometry_y += delta_enc * math.sin(math.radians(angle))
        
        heading_diff = ((target_heading - angle + 180) % 360) - 180
        
        # Corner detection with cooldown to prevent multiple detections
        if pyb.elapsed_millis(last_corner_time) > corner_cd:
            ob_error, ob_det = detect_region("O")
            bb_error, bb_det = detect_region("B")
            if ob_det or bb_det:
                corner_count += 1
                last_corner_time = pyb.millis()
                pid_integral = 0  # Reset integral on corner detection
                if corner_count < 13: 
                    target_heading = (direction * 90 * corner_count) % 360
                heading_diff = ((target_heading - angle + 180) % 360) - 180
        
        # Wall following using black wall detection
        if direction == -1:  # CCW
            roi = (0, CAM_HEIGHT-90, CAM_CENTER, 90)  # left wall roi
        else:  # CW
            roi = (CAM_CENTER, CAM_HEIGHT-90, CAM_CENTER, 90)  # right wall roi
        cam_error, black_det = detect_region("BK", roi=roi)
        no_black_count = 0 if black_det else no_black_count + 1
        
        # Final completion check after 12 corners
        if corner_count >= 12:
            if encoder >= final_forward:
                set_speed(-10)
                set_steering(240)
                break
        
        if state == 'initial_forward':
            # Initial approach using IMU only until front ToF reaches 800mm
            # This ensures straight approach before switching to camera guidance
            kp, ki, kd = 2, 0.001, 1
            error = heading_diff
            
            # During initial forward, detect orange or blue to set direction
            orange_error, orange_det = detect_region("O")
            blue_error, blue_det = detect_region("B")
            if direction == 0:  # Only set if unknown
                if orange_det and not blue_det:
                    direction = 1  # Orange first: CW
                elif blue_det and not orange_det:
                    direction = -1  # Blue first: CCW
            
            front_dist = read_distance()
            if front_dist <= 800:  # Switch to camera following when 800mm reached
                state = 'follow_wall'
                fetch_data(b'z')  # Reset encoder for new segment
                
        elif state == 'follow_wall':
            # Wall following state using camera guidance with IMU backup
            # Combines camera error with heading error for smooth wall tracking
            kp, ki, kd = 2, 0.001, 1
            wall_offset = -20  # Keep wall on left for CW navigation
            if black_det:
                error = cam_error * 0.3 + heading_diff * 0.7 - wall_offset
            else:
                error = heading_diff  # Fallback to IMU if wall lost
                
            # Transition to cornering when wall is lost and minimum distance traveled
            if no_black_count > 5 and encoder > min_segment_dist:
                state = 'turn_corner'
                corner_count += 1
                target_heading = (target_heading + direction * 90) % 360
                target_speed = min_fs  # Slow down for cornering
                no_black_count = 0
                    
        elif state == 'turn_corner':
            # Corner execution state using pure IMU guidance
            # Performs precise 90-degree turns based on gyro integration
            kp, ki, kd = 2.5, 0.001, 1.5
            error = heading_diff
            
            if abs(heading_diff) < turn_tol:
                state = 'follow_wall'
                target_speed = max_fs  # Resume full speed after turn
                fetch_data(b'z')  # Reset encoder for new straight segment
        
        # LED indication and PID control execution
        set_led("G" if black_det else "off")  # Green when wall detected
        pid_integral = max(-100, min(100, pid_integral + error * ki))
        steer = error * kp + pid_integral + (error - last_error) * kd
        last_error = error
        current_speed += min(2, max(-2, target_speed - current_speed))  # Smooth speed transitions
        set_speed(current_speed)
        set_steering(240 + steer)
        
except:
    error_flag = 1
    set_led("M")  # Magenta LED for error state
finally:
    # Clean shutdown procedure
    set_speed(0)
    set_steering(240)
    pyb.delay(500 if not error_flag else 2000)
    pyb.standby()