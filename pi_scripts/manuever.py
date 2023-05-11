from gpiozero import Servo
import time

# Define GPIO pins for pan and tilt servos
pan_pin = 18
tilt_pin = 23

# Initialize pan and tilt servos
pan_servo = Servo(pan_pin)
tilt_servo = Servo(tilt_pin)

# Define pan and tilt angle ranges
pan_min_angle = -90
pan_max_angle = 90
tilt_min_angle = -90
tilt_max_angle = 90

# Define pan and tilt angle increments
pan_increment = 0.1
tilt_increment = 0.1

# Define initial pan and tilt angles
pan_angle = 50
tilt_angle = 50

# Function to move the pan servo to a given angle
def move_pan(angle):
    # Calculate PWM value from angle
    pwm = (angle + 90) / 180.0
    # Move servo to PWM value
    pan_servo.value = pwm
    # Wait for servo to reach position
    time.sleep(0.1)

# Function to move the tilt servo to a given angle
def move_tilt(angle):
    # Calculate PWM value from angle
    pwm = (angle + 90) / 180.0
    # Move servo to PWM value
    tilt_servo.value = pwm
    # Wait for servo to reach position
    time.sleep(0.1)

# Main loop
while True:
    # Increment pan angle
    pan_angle += pan_increment
    # Check if pan angle is outside of range
    if pan_angle > pan_max_angle:
        pan_angle = pan_min_angle
    elif pan_angle < pan_min_angle:
        pan_angle = pan_max_angle
    # Move pan servo to new angle
    move_pan(pan_angle)

    # Increment tilt angle
    tilt_angle += tilt_increment
    # Check if tilt angle is outside of range
    if tilt_angle > tilt_max_angle:
        tilt_angle = tilt_min_angle
    elif tilt_angle < tilt_min_angle:
        tilt_angle = tilt_max_angle
    # Move tilt servo to new angle
    move_tilt(tilt_angle)
