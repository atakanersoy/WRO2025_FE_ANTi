import pyb
import sensor
import image

redLED = pyb.LED(1) # built-in red LED
blueLED = pyb.LED(3) # built-in blue LED

# Initialize camera sensor
sensor.reset()  # Reset camera settings
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 for color detection
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.set_vflip(True)  # Vertically flip the image for reverse mounting
sensor.set_hmirror(True)  # Horizontally mirror the image for reverse mounting
sensor.skip_frames(time=500)  # Skip initial frames to stabilize the sensor

redLED.on()
sensor.skip_frames(time = 2000)

redLED.off()
blueLED.on()

print("You're on camera!")
sensor.snapshot().save("example.jpg")

blueLED.off()
print("Done! Reset the camera to see the saved image.")
