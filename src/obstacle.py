# --- Module Imports ---
import pyb, time
from machine import Pin, I2C, SPI
import sensor

# --- Servo Control ---
servo_timer = pyb.Timer(4, freq=50)
servo = servo_timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin("PB8"))

SV_CENTER = 1775
SV_LEFT = 2575
SV_RIGHT = 3275

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

# --- Obstacle Detection Functions ---
def detect_red():
    """Scan for red pixels (similar to orange detection)"""
    img = sensor.snapshot()
    red_pixels = 0
    for y in range(10, 100, 10):
        for x in range(10, 300, 20):
            r, g, b = img.get_pixel(x, y)
            if r > 60 and g < 40 and b < 40:  # Strong red, low green/blue
                red_pixels += 1
    return red_pixels > 15  # Threshold for red detection

def detect_green():
    """Scan for green pixels (similar to blue detection)"""
    img = sensor.snapshot()
    green_pixels = 0
    for y in range(10, 100, 10):
        for x in range(10, 300, 20):
            r, g, b = img.get_pixel(x, y)
            if g > 60 and r < 40 and b < 40:  # Strong green, low red/blue
                green_pixels += 1
    return green_pixels > 15  # Threshold for green detection

def detect_magenta():
    """Scan for magenta pixels (red+blue combination)"""
    img = sensor.snapshot()
    magenta_pixels = 0
    for y in range(10, 100, 10):
        for x in range(10, 300, 20):
            r, g, b = img.get_pixel(x, y)
            if r > 50 and b > 50 and g < 30:  # Red+blue, low green
                magenta_pixels += 1
    return magenta_pixels > 15  # Threshold for magenta detection

def detect_obstacle():
    """
    Combined detection function
    Returns: (red_detected, green_detected, magenta_detected, distance)
    """
    return (
        detect_red(),
        detect_green(),
        detect_magenta(),
        read_distance()
    )

# --- Enhanced Motion Functions ---
def move(cm, speed=30, check_obstacles=True):
    """Move with continuous obstacle checking"""
    global encoder
    encoder = 0
    target = int(abs(cm) * 12)  # Convert cm to encoder ticks
    direction = 1 if cm > 0 else -1
    mc(speed * direction)
    
    while read_encoder() < target:
        if check_obstacles:
            red, green, magenta, dist = detect_obstacle()
            if magenta:  # Found parking spot
                mc(0)
                return "parking"
            if dist < 100:  # Obstacle too close
                mc(0)
                return "obstacle"
        pyb.delay(10)  # Small delay to prevent CPU overload
    
    mc(0)
    return "completed"

def turn(angle, speed=30, check_obstacles=True):
    """Turn with continuous obstacle checking"""
    direction = 1 if angle > 0 else -1
    sv(240 + direction * 60)  # Set steering angle
    mc(speed * direction)  # Start motors
    
    start_time = pyb.millis()
    turn_time = abs(angle) * 20  # ms per degree
    
    while (pyb.millis() - start_time) < turn_time:
        if check_obstacles:
            red, green, magenta, dist = detect_obstacle()
            if magenta:  # Found parking spot during turn
                mc(0)
                return "parking"
            if dist < 80:  # Obstacle very close during turn
                mc(0)
                return "obstacle"
        pyb.delay(10)
    
    mc(0)
    sv(240)  # Center steering
    return "completed"

def avoid_obstacle(direction):
    """Standard obstacle avoidance maneuver"""
    # Back up slightly
    move(-5, 20)
    
    if direction == "right":
        # Right turn maneuver
        turn(45, 25)
        move(20, 25)
        turn(-45, 25)
        move(30, 25)
        turn(-45, 25)
        move(20, 25)
        turn(45, 25)
    else:
        # Left turn maneuver
        turn(-45, 25)
        move(20, 25)
        turn(45, 25)
        move(30, 25)
        turn(45, 25)
        move(20, 25)
        turn(-45, 25)

# --- Main Obstacle Course Loop ---
btn()  # Wait for button press
print("Obstacle Course Start")

for lap in range(4):  # Four sides of course
    move(50, 30)  # Initial forward move
    
    while True:
        red, green, magenta, dist = detect_obstacle()
        
        if magenta:  # Parking spot detected
            move(10, 20)  # Move into parking spot
            turn(180, 30)  # Turn around
            print("Parked at magenta")
            mc(0)
            pyb.standby()
            break
            
        elif dist < 100:  # Obstacle too close
            mc(0)  # Emergency stop
            pyb.delay(500)
            
            if red and green:  # Both colors
                avoid_obstacle("right" if lap % 2 else "left")
            elif red:  # Red obstacle
                avoid_obstacle("right")
            elif green:  # Green obstacle
                avoid_obstacle("left")
            else:  # Unknown obstacle
                avoid_obstacle("right")
                
            break  # Continue to next segment
            
        elif not (red or green) and lap < 3:  # Normal corner
            turn(90, 30)  # Standard 90° turn
            break

mc(0)
pyb.standby()