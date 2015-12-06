#!/usr/bin/env python
print("""
This is the CV Monitor with RaspiCam.

Press CTRL+C to exit.
""")

import dot3k.lcd as lcd
import dot3k.backlight as backlight
import time, datetime, copy, math, psutil
import dot3k.joystick as j
import picamera
import os
import subprocess

screen_on = True;
image_num = 0;
picture_waiting = False;

reset_initiated = False;

@j.on(j.UP)
def handle_up(pin):
    global screen_on
    global reset_initiated
    print("Up pressed!")
    #print(screen_on)

    if screen_on:
        backlight.rgb(0, 0, 0)
        screen_on = False
    else:
        backlight.rgb(200, 200, 200)
        screen_on = True

    reset_initiated = False


@j.on(j.BUTTON)
def handle_button(pin):
    print("Button pressed!")
    global image_num
    global reset_initiated
    global picture_waiting

    if picture_waiting!=True:
        picture_waiting = True
        image_num = image_num + 1
        camera.capture('image' + format(image_num,'03') + '.jpg')
        print 'image file: image' + format(image_num,'03') + '.jpg'

        lcd.set_cursor_position(13, 2)
        lcd.write(format(image_num,'03'))
        reset_initiated = False
        picture_waiting = False
    else:
        print 'waiting on image to return'


@j.on(j.DOWN)
def handle_down(pin):
    print("Down pressed!")    
    global image_num
    global reset_initiated

    if reset_initiated == False:
        reset_initiated = True
        print("first time")
    else:
        lcd.set_cursor_position(0, 0)
        lcd.write("SHUTTING DOWN   ")
        os.system("sudo shutdown now");


@j.on(j.LEFT)
def handle_left(pin):
    print("LEFT pressed!")

    
@j.on(j.RIGHT)
def handle_right(pin):
    print("RIGHT pressed!")


def get_ip_addr():
    ipaddr_command = 'ip address list | grep inet | grep -v 127.0.0 | cut -d " " -f 6 | cut -d "/" -f 1'
    p = subprocess.Popen(ipaddr_command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return p.stdout.read()

    



ip = get_ip_addr()

print "IP: " + ip

lcd.set_cursor_position(0, 0)
lcd.write("IP: " + ip)

lcd.set_cursor_position(0, 1)
lcd.write("CPU: ")

lcd.set_cursor_position(13, 1)
lcd.write("IMG")

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


    lcd.set_cursor_position(5, 1)
    lcd.write(str(cpu_avg*100))


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

