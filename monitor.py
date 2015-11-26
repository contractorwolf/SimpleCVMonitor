#!/usr/bin/env python
print("""
This example shows you how to create animations on Display-o-Tron!
You should see a collection of animated icons on your display.

Press CTRL+C to exit.
""")

import dot3k.lcd as lcd
import dot3k.backlight as backlight
import time, datetime, copy, math, psutil
import dot3k.joystick as j
import picamera



screen_on = True;
image_num = 0;

@j.on(j.UP)
def handle_up(pin):
    global screen_on
    print("Up pressed!")
    print(screen_on)

    if screen_on:
        backlight.rgb(0, 0, 0)
        screen_on = False
    else:
        backlight.rgb(200, 200, 200)
        screen_on = True




@j.on(j.BUTTON)
def handle_button(pin):
    print("Button pressed!")
    image_num = image_num + 1
    
    global image_num
    camera.capture('image' + format(image_num,'03') + '.jpg')
    print 'image file: image' + format(image_num,'03') + '.jpg'

    lcd.set_cursor_position(13, 2)
    lcd.write(format(image_num,'03'))


    





lcd.write('CV Monitor v1')
lcd.set_cursor_position(0, 1)
lcd.write("CPU: ")

lcd.set_cursor_position(12, 1)
lcd.write("img:")

cpu_sample_count = 200
cpu_samples = [0] * cpu_sample_count
hue = 0.0


lcd.set_contrast(52)

backlight.rgb(200, 200, 200)


camera = picamera.PiCamera();

while True:
    cpu_samples.append(psutil.cpu_percent() / 100.0)
    cpu_samples.pop(0)

    cpu_avg = sum(cpu_samples) / cpu_sample_count

    #turns the white led array to reflect the CPU load 
    backlight.set_graph(cpu_avg)

    #display 3 lines on the LCD
    lcd.set_cursor_position(5, 1)
    lcd.write(str(cpu_avg*100))

    lcd.set_cursor_position(10, 1)
    lcd.write("% ")


    lcd.set_cursor_position(13, 2)
    lcd.write(format(image_num,'03'))

    

    lcd.set_cursor_position(0, 2)
    t = datetime.datetime.now().strftime("%H:%M:%S")
    lcd.write(t)

    time.sleep(0.05)
