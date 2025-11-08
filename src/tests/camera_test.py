import sensor
import time

# Initialize camera sensor
sensor.reset()  # Reset camera settings
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 for color detection
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.set_vflip(True)  # Vertically flip the image for reverse mounting
sensor.set_hmirror(True)  # Horizontally mirror the image for reverse mounting
sensor.skip_frames(time=500)  # Skip initial frames to stabilize the sensor

clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
