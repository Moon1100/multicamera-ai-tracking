#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get, post, run, route, request, template, static_file
from PCA9685 import PCA9685
import threading
import socket #ip
import os
import time
import redis


pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# Set servo parameters
HPulse = 1500  # Sets the initial Pulse
HStep = 0    # Sets the initial step length
VPulse = 1500  # Sets the initial Pulse
VStep = 0    # Sets the initial step length (constant movement up)
pwm.setServoPulse(1, VPulse)
pwm.setServoPulse(0, HPulse)



def move(step, direction):
    global HStep, VStep

    if direction == 'horizontal':
        HStep = step
        VStep = 0
    elif direction == 'vertical':
        HStep = 0
        VStep = step


def timerfunc():
    global HPulse, VPulse, HStep, VStep, pwm, t

    if HStep != 0:
        HPulse += HStep
        if HPulse >= 2500: 
            HPulse = 2500
            HStep = 0 

        if HPulse <= 500:
            HPulse = 500
            HStep = 0 

        # set channel 2, the Horizontal servo
        pwm.setServoPulse(0, HPulse)

    if VStep != 0:
        VPulse += VStep
        if VPulse >= 2500: 
            VPulse = 2500
            VStep = 0 
        if VPulse <= 500:
            VPulse = 500
            VStep = 0 
        # set channel 3, the vertical servo
        pwm.setServoPulse(1, VPulse)
    # restart the timer
    t = threading.Timer(0.02, timerfunc)
    t.setDaemon(True)
    t.start()

 


t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()


# r = redis.Redis(host='localhost', port=6379, db=0)
# p = r.pubsub()
# p.subscribe('my_channel')#for testing socket
# p.subscribe('1')

if __name__ == '__main__':
    try:
        move(-100, 'horizontal')
        time.sleep(2)
        move(-50, 'horizontal')
        time.sleep(2)
        move(50, 'veritcal')
        time.sleep(2)
        move(-50, 'vertical')
        time.sleep(2)
      

        # while True:
        #     pass        
    except KeyboardInterrupt:
        print("Exiting")
