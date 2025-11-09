# obstacle.py
# Vehicle control for obstacle challenge using camera-based detection and sensor fusion.
# MicroPython code.
# This script controls an autonomous vehicle in an obstacle course.
# It uses a camera for color detection (red, green, magenta obstacles), combined camera with IMU sensor fusion, 
# gyroscope for heading, and encoder for odometry.
# The vehicle navigates a rectangular course, avoids obstacles based on color (red: right avoid, green: left avoid),
# The formed path by avoiding obstacles is the shortest path possible around each obstacle and the vehicle goes as fast as possible without losing control,
# detects magenta for parking, and performs maneuvers using PID for steering.

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

# Front ToF sensor setup for obstacle distance
i2c = I2C(2)  # Initialize I2C bus 2
tof_address = 0x29  # Default address for VL53L1X front ToF sensor

def read_distance():
    # Read 2 bytes from register 0x1E (distance result)
    result = i2c.readfrom_mem(tof_address, 0x1E, 2)
    return (result[0] << 8) | result[1]  # Combine to get distance in mm

# Servo setup for steering
SERVO_MIN = 1775  # Minimum pulse width for servo
SERVO_CENTER = 2575  # Center pulse width
SERVO_MAX = 3275  # Maximum pulse width
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
TARGET_DIST = 150  # Target distance to obstacles in mm

# Color thresholds in LAB for find_blobs (L_min, L_max, A_min, A_max, B_min, B_max)
th = {
    "R": [(25, 65, 35, 75, -10, 20)],  # Red obstacle
    "G": [(30, 70, -40, -10, 10, 50)],  # Green obstacle
    "OB": [(5,60,5,20,0,25),(5,60,5,80,-80,-25)],  # Orange/Blue (combined or alternative)
    "BK": [(0,25,-10,20,-15,10)],  # Black (not used in obstacles)
    "M": [(40, 80, 60, 90, -20, 30)]  # Magenta for parking
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
outer_dist = 30  # Pixel offset for outer obstacles
inner_dist = 30  # Pixel offset for inner
turn_tol = 5  # Tolerance for turn completion in degrees
max_turn_tol = 80  # Max tolerance for passing obstacles
corner_count = 0  # Track corners navigated
direction = 0  # 1 for CW, -1 for CCW
corner_cd = 2000  # Min time ms between corner detections
last_corner_time = pyb.millis()  # Last corner detection time
min_ps, max_ps = 15, 30  # Partial speeds
min_fs, max_fs = 35, 45  # Full speeds
min_ms, min_ws = 15, 20  # Maneuver/wall speeds
current_speed = min_ps  # Current motor speed
target_speed = max_ps  # Target speed for ramp
state = 'determine_direction'  # State machine start
target_heading = 0  # Desired heading
last_heading = 0  # Last target
lost_heading = 0  # Heading when lost color
cam_error = 0  # Camera position error
heading_error = 0  # Heading error
last_color = None  # Last detected color (0 red, 1 green)
no_color_count = 0  # Counter for no color detection

# PID parameters
kp, ki, kd = 2, 0.001, 0.1  # Gains
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
    # Section 1: Direction Determination and Initial Maneuver
    # This loop determines the driving direction (CW or CCW) based on side ToF distances.
    # It performs an initial parking-like maneuver to align the vehicle.
    # States: 'determine_direction' -> 'park1' -> 'park2' -> 'park3'
    # Uses ToF to decide direction, then adjusts steering and speed to turn 90 degrees.
    while True:
        fetch_data(b'r')
        now = pyb.millis()
        dt = (now - last_time) / 1000.0
        last_time = now
        gyro = read_gyro()
        angle += gyro * dt
        delta_enc = encoder - last_enc
        last_enc = encoder
        odometry_x += delta_enc * math.cos(math.radians(angle))
        odometry_y += delta_enc * math.sin(math.radians(angle))
        if state == 'determine_direction':
            # Compare left and right ToF to set direction (smaller left: CW, else CCW)
            if tof_left > 0 and tof_right > 0:
                direction = 1 if tof_left < tof_right else -1
                set_steering(0 if direction == 1 else 480)
            elif direction == 0 and pyb.elapsed_millis(start) > 2000:
                direction = -1
                set_steering(480)
            if direction != 0:
                pyb.delay(5)
                current_speed = -min_ps
                target_speed = -max_ps
                state = 'park1'
        elif state == 'park1':
            # Small initial turn (24 degrees) to align
            heading_error = ((((direction * 24) % 360) - angle + 180) % 360) - 180
            if abs(target_speed - current_speed) == 0: target_speed = -min_ps
            current_speed += min(1, max(-1, target_speed - current_speed))
            set_steering(0 if direction == 1 else 480)
            set_speed(current_speed)
            if abs(heading_error) < turn_tol:
                current_speed = min_ps
                target_speed = max_ps
                state = 'park2'
        elif state == 'park2':
            # Continue to 90 degrees turn
            heading_error = ((((direction * 90) % 360) - angle + 180) % 360) - 180
            if abs(heading_error) < 30: current_speed += min(1, max(-1, target_speed - current_speed))
            set_steering(480 if direction == 1 else 0)
            set_speed(current_speed)
            if abs(heading_error) < 15:
                fetch_data(b'z')
                state = 'park3'
        elif state == 'park3':
            # Fine-tune the 90 degree turn with PID
            heading_error = ((((direction * 90) % 360) - angle + 180) % 360) - 180
            kp, ki, kd = 2, 0.001, 0.5
            error = heading_error
            if encoder >= 50:
                no_color_count = 0  # Reset for main loop
                state = 'no_color1' if direction == 1 else 'no_color'
                target_speed = max_fs
                break
            pid_integral = max(-100, min(100, pid_integral + error * ki))
            steer = error * kp + pid_integral + (error - last_error) * kd
            last_error = error
            current_speed += min(2, max(-2, target_speed - current_speed))
            set_speed(current_speed)
            set_steering(240 + steer)
    # Section 2: Main Navigation Loop
    # Navigates the course, detecting and avoiding obstacles.
    # Uses camera to detect colors, adjusts path based on color and direction.
    # Tracks corners using orange/blue detection with cooldown.
    # States: 'no_color', 'follow_color', 'lost_color', 'pass_color'
    # Transitions to U-turn when 13 corners reached.
    while True:
        fetch_data(b'r')
        now = pyb.millis()
        dt = (now - last_time) / 1000.0
        last_time = now
        gyro = read_gyro()
        angle += gyro * dt
        delta_enc = encoder - last_enc
        last_enc = encoder
        odometry_x += delta_enc * math.cos(math.radians(angle))
        odometry_y += delta_enc * math.sin(math.radians(angle))
        heading_diff = ((target_heading - angle + 180) % 360) - 180
        if pyb.elapsed_millis(last_corner_time) > corner_cd:
            ob_error, ob_det = detect_region("OB")
            if ob_det:
                corner_count += 1
                last_corner_time = pyb.millis()
                pid_integral = 0
                if corner_count < 13: target_heading = (direction * 90 * corner_count) % 360
                heading_diff = ((target_heading - angle + 180) % 360) - 180
        red_error, red_det = detect_region("R")
        green_error, green_det = detect_region("G")
        magenta_error, mag_det = detect_region("M")
        detected = False
        if red_det or green_det or mag_det:
            detected = True
            no_color_count = 0
            if red_det:
                offset = outer_dist if direction == -1 else inner_dist
                cam_error = red_error - (CAM_CENTER - offset)  # Keep red on left (offset -30 px)
                last_color = 0
            elif green_det:
                offset = inner_dist if direction == -1 else outer_dist
                cam_error = green_error - (CAM_CENTER + offset)  # Keep green on right (offset +30 px)
                last_color = 1
            elif mag_det:
                offset = inner_dist if direction == -1 else -inner_dist  # CCW: right, CW: left
                cam_error = magenta_error - (CAM_CENTER + offset)
            state = 'follow_color'
            if mag_det and read_distance() < 100: state = 'enter_park'
        else: no_color_count += 1
        if corner_count >= 13:
            fetch_data(b'z')
            state = 'u_turn1'  # Start U-turn maneuver after 3 full laps
            target_speed = max_fs
            break
        if state in ('no_color', 'no_color1'):
            # Basic navigation with obstacle scanning
            kp, ki, kd = 1.2, 0.003, 0.35
            error = heading_diff * 1.2
            if detected and abs(cam_error) < 45: state = 'follow_color'
        elif state == 'follow_color':
            # Object following with balanced control
            kp, ki, kd = 1.1, 0.002, 0.6
            error = cam_error * 0.25 + heading_diff * 0.15
            if not detected: 
                if no_color_count > 2: state = 'lost_color'
        elif state == 'lost_color':
            # Search pattern with memory of last position
            kp, ki, kd = 1.3, 0.002, 0.4
            search_offset = 15 * (1 if last_color == 0 else -1)
            error = heading_diff + search_offset
            if detected: state = 'follow_color'
            elif no_color_count > 6: state = 'pass_color'
        elif state == 'pass_color':
            # Large maneuver with progressive adjustment
            kp, ki, kd = 1.4, 0.001, 1.2
            avoidance_angle = 35 * (-1 if last_color == 0 else 1)
            error = heading_diff + avoidance_angle
            if abs(heading_diff) < 12: state = 'no_color'
        target_speed = min_fs if state in ('lost_color', 'pass_color') else max_fs
        set_led("R" if last_color == 0 else "G" if detected else "off")
        pid_integral = max(-100, min(100, pid_integral + error * ki))
        steer = error * kp + pid_integral + (error - last_error) * kd
        last_error = error
        current_speed += min(2, max(-2, target_speed - current_speed))
        set_speed(current_speed)
        set_steering(240 + steer)
    # Section 2.5: 180° U-Turn Maneuver
    # This loop performs a 180-degree turn to reverse direction after completing the rectangular course.
    # It uses absolute gyro angle targeting 180° regardless of starting orientation.
    # States: 'u_turn1' -> 'u_turn2' -> 'u_turn3'
    # Uses aggressive steering initially, then PID for precise alignment to 180°.
    while True:
        fetch_data(b'r')
        now = pyb.millis()
        dt = (now - last_time) / 1000.0
        last_time = now
        gyro = read_gyro()
        angle += gyro * dt
        # Calculate heading error to absolute 180° target
        heading_error = (((180 - angle + 180) % 360) - 180)
        if state == 'u_turn1':
            # Initial turn entry with aggressive steering to establish rotation toward 180°
            kp, ki, kd = 2.5, 0.001, 1.5
            error = heading_error
            target_speed = min_fs  # Controlled speed for maneuver
            # Apply strong steering in the shortest direction to 180°
            base_steer = 120 if heading_error > 0 else -120  # Steer toward 180°
            pid_integral = max(-100, min(100, pid_integral + error * ki))
            steer = base_steer + error * kp + pid_integral + (error - last_error) * kd
            last_error = error
            current_speed += min(2, max(-2, target_speed - current_speed))
            set_speed(current_speed)
            set_steering(240 + steer)
            # Transition when 60° progress achieved
            if abs(heading_error) < 120:
                state = 'u_turn2'
                pid_integral = 0  # Reset I for main turn phase
        elif state == 'u_turn2':
            # Main turning phase with maintained steering toward 180°
            kp, ki, kd = 2.0, 0.001, 1.2
            error = heading_error
            target_speed = min_fs
            # Maintain steering with reduced aggression as we approach target
            base_steer = 80 if heading_error > 0 else -80
            pid_integral = max(-100, min(100, pid_integral + error * ki))
            steer = base_steer + error * kp + pid_integral + (error - last_error) * kd
            last_error = error
            current_speed += min(2, max(-2, target_speed - current_speed))
            set_speed(current_speed)
            set_steering(240 + steer)
            # Transition when close to target (within 45 degrees)
            if abs(heading_error) < 45:
                state = 'u_turn3'
                target_speed = min_ps  # Reduce speed for precise alignment
        elif state == 'u_turn3':
            # Final alignment with precise control to exact 180°
            kp, ki, kd = 3.0, 0.001, 2.0
            error = heading_error
            target_speed = min_ps
            # Pure PID control for fine alignment
            pid_integral = max(-100, min(100, pid_integral + error * ki))
            steer = error * kp + pid_integral + (error - last_error) * kd
            last_error = error
            current_speed += min(2, max(-2, target_speed - current_speed))
            set_speed(current_speed)
            set_steering(240 + steer)
            # Complete U-turn when precisely aligned to 180°
            if abs(heading_error) < turn_tol:
                # Reverse travel direction after U-turn
                direction = -direction
                # Update target heading for new direction
                target_heading = 180  # Facing 180°
                
                fetch_data(b'z')  # Reset slave encoders
                
                # Transition to parking approach
                state = 'end_park1'
                target_speed = max_fs
                break
        # Fail-safe - break if U-turn takes too long (5 seconds)
        if pyb.elapsed_millis(now) > 5000:
            state = 'end_park1'
            break
    # Section 3: Parking Maneuver
    # Enters parking spot upon magenta detection.
    # Follows magenta wall with camera offset based on direction.
    # Uses angle and odometry for positioning after passing magenta.
    # States: 'end_park1' to 'end_park7' for sequenced maneuver.
    # Relies on camera for following, switches to odometry/angle after.
    while True:
        fetch_data(b'r')
        now = pyb.millis()
        dt = (now - last_time) / 1000.0
        last_time = now
        gyro = read_gyro()
        angle += gyro * dt
        delta_enc = encoder - last_enc
        last_enc = encoder
        odometry_x += delta_enc * math.cos(math.radians(angle))
        odometry_y += delta_enc * math.sin(math.radians(angle))
        heading_diff = ((target_heading - angle + 180) % 360) - 180
        magenta_error, mag_det = detect_region("M")
        if mag_det:
            offset = 30 if direction == -1 else -30  # CCW: right, CW: left
            cam_error = magenta_error - (CAM_CENTER + offset)
        else:
            cam_error = 0
        if state == 'end_park1':
            # Approach and follow magenta wall
            kp, ki, kd = 3, 0.001, 3
            error = heading_diff + cam_error * 0.4
            if abs(heading_error) < turn_tol and encoder > 50 and not mag_det:
                fetch_data(b'p')  # Pause slave if needed
                state = 'end_park2'
        elif state == 'end_park2':
            # Continue forward using odometry after passing magenta
            kp, ki, kd = 1, 0.001, 0.5
            error = heading_diff
            if odometry_x > 450:  # Use odometry to reach position
                target_heading = (direction * 90 * 2) % 360
                state = 'end_park3'
        elif state == 'end_park3':
            # Turn into the spot based on angle
            kp, ki, kd = 3, 0.001, 3
            error = heading_diff
            if abs(heading_diff) < 10:
                fetch_data(b'p')
                state = 'end_park4'
        elif state == 'end_park4':
            # Adjust forward position with odometry
            kp, ki, kd = 2.5 if direction == 1 else 3.5, 0.001, 3 if direction == 1 else 4
            error = heading_diff
            if odometry_y > (62.5 if direction == 1 else 170):
                state = 'end_park5'
        elif state == 'end_park5':
            # Reverse turn for parallel alignment
            heading_error = ((target_heading - (direction * 73) - angle + 180) % 360) - 180
            current_speed += min(2, max(-2, target_speed - current_speed))
            set_steering(0 if direction == 1 else 480)
            set_speed(current_speed)
            if abs(heading_error) < 30:
                current_speed = -min_ps
                target_speed = -min_ps
                state = 'end_park6'
        elif state == 'end_park6':
            # Final reverse using angle
            heading_error = ((target_heading - (direction * 73) - angle + 180) % 360) - 180
            kp, ki, kd = 2, 0.001, 2
            error = heading_error
            if abs(heading_error) < turn_tol:
                state = 'end_park7'
        elif state == 'end_park7':
            # Straighten and stop
            heading_error = heading_diff
            current_speed += min(2, max(-2, target_speed - current_speed))
            set_steering(0 if direction == 1 else 480)
            set_speed(current_speed)
            if abs(heading_error) < 7:
                set_speed(0)
                set_steering(240)
                break
        if state not in ('end_park7', 'end_park5'):
            pid_integral = max(-100, min(100, pid_integral + error * ki))
            steer = error * kp + pid_integral + (error - last_error) * kd
            last_error = error
            current_speed += min(2, max(-2, target_speed - current_speed))
            set_speed(current_speed)
            set_steering(240 + steer * (-1 if state == 'end_park6' else 1))
except:
    error_flag = 1
    set_led("M")
finally:
    set_speed(0)
    set_steering(240)
    pyb.delay(50 if not error_flag else 2000)
    pyb.standby()