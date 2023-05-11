#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get, post, run, route, request, template, static_file
from PCA9685 import PCA9685
import threading
import socket #ip
import os
import time

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# Set servo parameters
HPulse = 1500  # Sets the initial Pulse
HStep = 0      # Sets the initial step length
VPulse = 1500  # Sets the initial Pulse
VStep = 0    # Sets the initial step length (constant movement up)
pwm.setServoPulse(1, VPulse)
pwm.setServoPulse(0, HPulse)



def move_up():
    global VStep
    VStep = -5


def move_down():
    global VStep
    VStep = 5


def move_left():
    global HStep
    HStep = 5


def move_right():
    global HStep
    HStep = -5

def timerfunc():
    global HPulse, VPulse, HStep, VStep, pwm

    if HStep != 0:
        HPulse += HStep
        if HPulse >= 2500: 
            HPulse = 2500
        if HPulse <= 500:
            HPulse = 500
        # set channel 2, the Horizontal servo
        pwm.setServoPulse(0, HPulse)

    if VStep != 0:
        VPulse += VStep
        if VPulse >= 2500: 
            VPulse = 2500
        if VPulse <= 500:
            VPulse = 500
        # set channel 3, the vertical servo
        pwm.setServoPulse(1, VPulse)

    # restart the timer
    t = threading.Timer(0.02, timerfunc)
    t.setDaemon(True)
    t.start()


t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()

if __name__ == '__main__':
    HStep = 5  
    try:
        while True:
            # Move camera to the left until the limit
            while HPulse > 500:
                move_left()
                time.sleep(0.02)

            # Move camera to the right until the limit
            while HPulse < 2500:
                move_right()
                time.sleep(0.02)

            # Move camera to the left until the limit
            while HPulse > 500:
                move_left()
                time.sleep(0.02)
    except KeyboardInterrupt:
        print("Exiting")
    
