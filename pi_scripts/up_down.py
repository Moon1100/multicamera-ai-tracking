import RPi.GPIO as GPIO
import time

# Set the GPIO pins for the PTZ motor
up_pin = 17
down_pin = 18

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(up_pin, GPIO.OUT)
GPIO.setup(down_pin, GPIO.OUT)

# Set the initial position to down
GPIO.output(up_pin, False)
GPIO.output(down_pin, True)

# Loop to move the PTZ up and down
while True:
    # Move up
    GPIO.output(up_pin, True)
    GPIO.output(down_pin, False)
    time.sleep(1)
    
    # Move down
    GPIO.output(up_pin, False)
    GPIO.output(down_pin, True)
    time.sleep(1)
