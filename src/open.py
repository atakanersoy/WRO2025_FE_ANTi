# --- Module Imports ---
import pyb, time
from machine import Pin, I2C, SPI
import sensor

# --- Servo Control ---
servo_timer = pyb.Timer(4, freq=50)
servo = servo_timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin("PB8"))

SV_CENTER = 2300
SV_LEFT = 2750
SV_RIGHT = 1850

def sv(position):
    pulse = SV_CENTER
    if position < 240:
        pulse = SV_CENTER + (240 - position) * 2
    else:
        pulse = SV_CENTER - (position - 240) * 2
    pulse = max(SV_RIGHT, min(SV_LEFT, pulse))
    servo.pulse_width(pulse)

# --- Motor PWM Control ---
motor_timer = pyb.Timer(1, freq=20000)
m1 = motor_timer.channel(2, pyb.Timer.PWM, pin=Pin('PA9'))
m2 = motor_timer.channel(3, pyb.Timer.PWM, pin=Pin('PA10'))

def mc(speed):
    if speed > 0:
        m1.pulse_width_percent(speed)
        m2.pulse_width_percent(0)
    elif speed < 0:
        m1.pulse_width_percent(0)
        m2.pulse_width_percent(-speed)
    else:
        m1.pulse_width_percent(0)
        m2.pulse_width_percent(0)

# --- Camera Setup ---
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.skip_frames(time=500)

thresholds = {
    "orange": [(30, 60, 10, 30, 5, 25)],
    "blue": [(0, 40, -10, 10, -20, -5)],
    "line": [(30, 80, 0, 0, 0, 0)]
}

# --- Button Input ---
btn_pin = Pin("PC4", Pin.IN, Pin.PULL_UP)
def btn():
    while btn_pin.value():
        pyb.delay(10)
    while not btn_pin.value():
        pyb.delay(10)

# --- 2-Pin Encoder ---
enc_a = Pin('PF13', Pin.IN)
enc_b = Pin('PF3', Pin.IN)
encoder = 0

def enc_handler(pin):
    global encoder
    if enc_a.value():
        encoder += 1
    else:
        encoder -= 1

enc_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=enc_handler)

def read_encoder():
    return abs(encoder)

# --- Gyroscope Reading X-Axis Only ---
spi = SPI(5, baudrate=1000000, polarity=1, phase=1)
cs_pin = Pin("PF6", Pin.OUT_PP, Pin.PULL_UP)

def read_gyro():
    cs_pin.low()
    spi.write(bytearray([0x28 | 0x80]))  # OUTX_L_G register
    low = spi.read(1)[0]
    spi.write(bytearray([0x29 | 0x80]))  # OUTX_H_G register
    high = spi.read(1)[0]
    cs_pin.high()

    raw = (high << 8) | low
    if raw >= 32768:
        raw -= 65536

    return raw * 0.035  # X-axis only

# --- ToF Sensor ---
i2c = I2C(2)
tof_address = 0x29

def read_distance():
    result = i2c.readfrom_mem(tof_address, 0x1E, 2)
    return (result[0] << 8) | result[1]

# --- Vision Processing ---
def detect_line():
    img = sensor.snapshot()
    dark_pixels = 0
    for y in range(20, 100, 10):
        for x in range(0, 320, 20):
            r, g, b = img.get_pixel(x, y)
            if r < 50 and g < 50 and b < 50:
                dark_pixels += 1
    return dark_pixels > 30

def detect_color():
    img = sensor.snapshot()
    orange_detected, blue_detected = False, False
    for y in range(10, 100, 10):
        for x in range(10, 300, 20):
            r, g, b = img.get_pixel(x, y)
            if r > 60 and g < 40:
                orange_detected = True
            if b > 60 and r < 40:
                blue_detected = True
    return orange_detected, blue_detected

# --- Detection Function ---
def detect():
    """
    Performs all environmental detection tasks:
    - Checks for lines
    - Scans for colors
    - Reads distance sensor
    - Monitors gyro
    """
    line_detected = detect_line()
    colors_detected = detect_color()
    current_distance = read_distance()
    rotation_rate = read_gyro()

    if line_detected:
        # Adjust steering when line detected
        sv(240 + 30 if line_detected else 240)
        
    if current_distance < 100:
        # Emergency stop for close obstacles
        mc(0)
        pyb.delay(500)
    return line_detected, colors_detected, current_distance, rotation_rate

# --- Motion Functions ---
def move(cm, speed=30):
    global encoder
    encoder = 0
    target = int(abs(cm) * 12)
    direction = 1 if cm > 0 else -1
    mc(speed * direction)
    while read_encoder() < target:
        detect()
    mc(0)

def turn(angle, speed=30):
    direction = 1 if angle > 0 else -1
    sv(240 + direction * 60)
    mc(speed * direction)
    pyb.delay(1000)
    mc(0)
    sv(240)

# --- Main Execution ---
btn()  # Wait for button press to start
print("Start")

cw = 0  # Clockwise direction (1 = CW, -1 = CCW, 0 = undecided)
remaining_cm = 150  # Total distance to travel after marker detection
steps = [(50, 0), (11, 0), (11, 0), (11, 0)]  # Movement segments (distance, pause)

# --- Main Navigation Loop ---
# Phase 1: Initial movement while scanning for color markers
for cm, _ in steps:
    if cw != 0:  # Skip if detected direction
        break

    # State 1: Move forward specified distance
    move(cm)

    # State 2: Check for color markers after each move
    orange, blue = detect_color()

    # State 3: Determine turn direction based on colors
    if orange and blue:  # Both colors = turn clockwise
        cw = 1 # (favor orange)
    elif orange:  # Orange only = turn clockwise
        cw = 1
    elif blue:  # Blue only = turn counter-clockwise
        cw = -1

    # State 4: Update remaining distance
    remaining_cm -= cm

# Phase 2: Complete remaining distance if no markers found
if cw == 0:  # Default to clockwise if no markers detected
    cw = 1

# State 5: Final straight movement
move(remaining_cm)

# Phase 3: 12-corner pattern execution
for corner in range(12):
    # State 6: Turn 90 degrees in determined direction
    turn(cw * 90)
    detect()  # Check surroundings

    # State 7: Special case for final corner
    if corner == 11:
        move(130)  # Final long move
        break

    # State 8: Standard movement between corners
    move(290)

# Phase 4: Shutdown
mc(0)  # Stop motors
pyb.standby()  # Enter low-power mode
