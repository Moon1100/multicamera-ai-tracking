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

    last_message_time = 0
    try:
        
        for message in p.listen():
            
            if message['type'] == 'message':
                current_time = time.time()
                if current_time - last_message_time >= 1:
                    
                    data = message['data'].decode('utf-8')

                    offset = ast.literal_eval(data)
                    if offset[0] == 'und' or offset[1] == 'und':
                        print('no target within frame')
                        move(0, 'horizontal')
                        pass
                    else:

                        if offset[0] > 20:
                            move(1, 'horizontal')
                            print('moving right')

                        elif offset[0] < -20:
                            move(-1, 'horizontal')
                            print('moving left')

                        else:
                            move(0, 'horizontal')
                            print('Horizontal Locked')

                    if offset[0] == 'und' or offset[1] == 'und':
                        print('no target within frame')
                        move(0, 'vertical')
                        pass
                    else:

                        if offset[1] > 60:
                            move(-1, 'vertical')
                            print('moving up')

                        elif offset[1] < 30:
                            move(1, 'vertical')
                            print('moving down')

                        else:
                            move(0, 'vertical')
                            print('vertical Locked')

                    last_message_time = current_time  # Update last message time


                    # if offset[1]>20:
                    #     HStep+=1

                    # elif offset[1]<20:
                    #     HStep-=1

                    # else :
                    #    print ('Horizontal Locked')






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
        # move(0, 'vertical')
        # time.sleep(2)
        # move(0, 'horizontal')
        # time.sleep(2)
        print('completed cycle')


      

        # while True:
        #     pass        
    except KeyboardInterrupt:
        print("Exiting")
