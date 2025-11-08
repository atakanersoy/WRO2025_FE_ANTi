from machine import I2C
import time

# Front ToF sensor setup for initial distance measurement
i2c = I2C(2)  # Initialize I2C bus 2
tof_address = 0x29  # Default address for VL53L1X front ToF sensor

def read_distance():
    # Read 2 bytes from register 0x1E (distance result)
    result = i2c.readfrom_mem(tof_address, 0x1E, 2)
    return (result[0] << 8) | result[1]  # Combine to get distance in mm

while True:
    distance = read_distance()
    print(f"Distance: {distance} mm")
    time.sleep_ms(50)