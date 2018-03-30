__author__ = 'Jaimiey Sears, Sully Cothran, Alex Schendel'
__version__ = 2.1
#############################HEAD########################################
# This file is for the setup and control of the servo attached to the
# lidar mount.
#
# The servo is the high torque HS-645MG from HiTEC (www.hitecrcd.com)
# New servo is the cheap TowerPro SG-5010 from AdaFruit (https://www.adafruit.com/product/155)
#
# Servo motors use PWM (pulse width modulation) to control their angle.
# PWM is oscillating voltages. For example, a frequency of 50 means 50 Hz,
# or a refresh every 20 ms. The duty cycle is the percentage of the cycle that
# the voltage is high for. Duty Cycle runs from 0.0 to 100.0.
# By setting the constants in constants.py, you can control the angle of
# the servo here.
#
# The code in this file is meant to be run on the RPi, and will not
# function as expected otherwise, due to the RPi.GPIO import only
# available on the RPi.
#########################################################################

from utility import debugPrint
from constants import *

### ONE-TIME SETUP ###
#GPIO.setmode(GPIO.BCM)
# Set up the pin as an output
#GPIO.setup(SERVO_PIN, GPIO.OUT)
# make a PWM object with frequency PWM_FREQ
#pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)#sets up pwm on servo pin to frequency 50Hz (20 ms polling rate) on GPIO pin 18. All found in constants.py
#pwm.start(0)#set duty cycle to the halfway point

##
# turnto()
# Description: turn to specified degree
#
# Perameters:
#   degree - int to determine what angle to rotate the LIDAR to
##
def turnTo(degree):
    if degree in range(DEGREE_MIN, DEGREE_MAX):#Make sure degree is within bounds
        #pwm_duty_cycle = (degree * (PWM_MAX-PWM_MIN) / (DEGREE_MAX-DEGREE_MIN)) + PWM_MIN#degree times PWM/degree + PWM_MIN will result in the PWM duty cycle to set (do the math and see!)
        #pwm.ChangeDutyCycle(pwm_duty_cycle)
        debugPrint("Valid angle!", SERVO_DRIVER)
        #Tell Arduino what angle to turn to via ROS publish!
    else:
        debugPrint("Degree input outside expected range", SERVO_DRIVER)

##
# stop()
# Description: stop writing PWM signals.
##
def stop():
    pwm.ChangeDutyCycle(0)