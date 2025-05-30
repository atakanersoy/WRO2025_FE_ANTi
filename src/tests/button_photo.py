import sensor,pyb
from machine import Pin

r,g,b=[pyb.Pin(p,pyb.Pin.OUT_PP)for p in("PE3","PC13","PF4")]
def l(c):r.low()if c in'ROMW'else r.high();g.low()if c in'GOCW'and(c!='O'or pyb.millis()%1<1)else g.high();b.low()if c in'BCMW'else b.high()
bt = Pin('PC4', Pin.IN, Pin.PULL_UP)
def btn(r=1):
    while bt.value(): pyb.delay(10)
    while r and not bt.value(): pyb.delay(10)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.HVGA)
sensor.skip_frames(time=500)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False, exposure_us=10000)
sensor.set_vflip(True)
sensor.set_hmirror(True)

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
