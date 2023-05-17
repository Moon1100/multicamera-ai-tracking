#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get, post, run, route, request, template, static_file
from PCA9685 import PCA9685
import threading
import socket #ip
import os
import time
import redis
import ast



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


r = redis.Redis(host='192.168.0.108', port=6379, db=0)
p = r.pubsub()
# p.subscribe('my_channel')#for testing socket
channel='1'
p.subscribe(f'{channel}')

if __name__ == '__main__':

    try:
        # print(f"Listening to channel: {channel}")

        # # Start listening to messages
        for message in p.listen():
            time.sleep(1)
            if message['type'] == 'message':
                data=message['data'].decode('utf-8')
                offset = ast.literal_eval(data)
                if offset[0]=='und'or offset[1]=='und':
                    print ('no target within frame')
                else:
                    print (offset)

                    
                    if offset[0]>20:
                        VStep-=1

                    elif offset[0]<20:
                        VStep+=1

                    else :
                       print ('Vertical Locked')
                    

                    

                    # if offset[1]>20:
                    #     HStep+=1

                    # elif offset[1]<20:
                    #     HStep-=1

                    # else :
                    #    print ('Horizontal Locked')





        # print('init')
        # time.sleep(2)
        # print('entering horizontal left')
        # move(-50, 'horizontal')
        # print('end horizontal left')

        # time.sleep(2)

        # print('entering horizontal right')
        # move(50, 'horizontal')
        # print('end horizontal right')

        # time.sleep(2)
        
        # print('entering vertical up')
        # move(50, 'vertical')
        # print('end vertical up')

        # time.sleep(2)

        # print('entering vertical down')
        # move(-50, 'vertical')
        # print('end vertical down')

        # time.sleep(2)
        # print('repositioning')
        # move(20, 'vertical')
        # time.sleep(2)
        # move(-25, 'horizontal')
        # time.sleep(2)
        # print('completed cycle')


      

        # while True:
        #     pass        
    except KeyboardInterrupt:
        print("Exiting")
