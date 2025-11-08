import sensor,pyb
from machine import Pin

# RGB LED for status
led_pins = [pyb.Pin(p, pyb.Pin.OUT_PP) for p in ("PE3", "PC13", "PF4")]  # R, G, B pins
def l(color):
    # Set LED color based on string code (e.g., 'R' red, 'G' green, 'M' magenta, 'off')
    led_pins[0].value(0 if color in 'ROMWY' else 1)  # Red on/low for certain colors
    led_pins[1].value(0 if color in 'GOCWY' and (color != 'O' or pyb.millis() % 1 < 1) else 1)  # Green, with blink for 'O'
    led_pins[2].value(0 if color in 'BCMW' else 1)  # Blue
# Button for start
button_pin = Pin('PC4', Pin.IN, Pin.PULL_UP)
def btn(release=1):
    # Wait for button press (and release if specified)
    while button_pin.value(): pyb.delay(1)
    if release:
        while not button_pin.value(): pyb.delay(1)

# Initialize camera sensor
sensor.reset()  # Reset camera settings
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 for color detection
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.set_vflip(True)  # Vertically flip the image for reverse mounting
sensor.set_hmirror(True)  # Horizontally mirror the image for reverse mounting
sensor.skip_frames(time=500)  # Skip initial frames to stabilize the sensor

image_counter = 1  # Initialize image counter

while 1:
    l("B")
    # Button wait
    btn()
    l("off")

    # When button is pressed:
    filename = "image_" + str(image_counter) + ".jpg"
    print("Saving image as:", filename)
    sensor.snapshot().save(filename)
    print("Done! Press button again to take another photo.")

    image_counter += 1  # Increment counter for next image
