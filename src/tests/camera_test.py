import sensor
import time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # RGB565 or GRAYSCALE
sensor.set_framesize(sensor.QVGA)  # QVGA (320x240)
sensor.skip_frames(time=2000)
clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
