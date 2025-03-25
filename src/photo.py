import pyb
import sensor
import image

redLED = pyb.LED(1) # built-in red LED
blueLED = pyb.LED(3) # built-in blue LED

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # 320x240 px
#sensor.set_vflip(True) # Vertical flip
#sensor.set_hmirror(True) # Horizontal mirror

redLED.on()
sensor.skip_frames(time = 2000)

redLED.off()
blueLED.on()

print("You're on camera!")
sensor.snapshot().save("example.jpg")

blueLED.off()
print("Done! Reset the camera to see the saved image.")
