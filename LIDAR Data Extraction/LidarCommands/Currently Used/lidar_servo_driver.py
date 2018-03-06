__author__ = 'Jaimiey Sears, Sully Cothran'
__version__ = 2
#############################HEAD########################################
# This file is for the setup and control of the servo attached to the
# lidar mount.
#
# The servo is the high torque HS-645MG from HiTEC (www.hitecrcd.com)
#
# The code in this file is meant to be run on the RPi, and will not
# function as expected otherwise, due to the RPi.GPIO import only
# available on the RPi.
#########################################################################

import RPi.GPIO as GPIO
from utility import debugPrint
from constants import *

### ONE-TIME SETUP ###
GPIO.setmode(GPIO.BCM)
# Set up the pin as an output
GPIO.setup(SERVO_PIN, GPIO.OUT)
# make a PWM object with frequency PWM_FREQ
pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)#sets up pwm on servo pin to frequency 50Hz (20 ms polling rate)
pwm.start(0)

##
# runManual()
# Description: begin infinite loop of servo control
##
def runManual():
    while True:
        degree = int(float(input("What angle do you want me to turn to?\n")))
        if isinstance(degree, int) and degree >= DEGREE_MIN and degree <= DEGREE_MAX:
            turnTo(degree)
        else:
            print("Input should be a number of degrees [0, 180]")

##
# turnto()
# Description: write a PWM signal to the servo
#
# Perameters:
#   degree - the degree to turn to, where 0 is the minimum, and 200 is the maximum.
##
def turnTo(degree):
    if degree in range(DEGREE_MIN, DEGREE_MAX):
        pwm_duty_cycle = (degree * (PWM_MAX-PWM_MIN) / (DEGREE_MAX-DEGREE_MIN)) + PWM_MIN
        #Theoretically, duty cycle between 5% and 10% would be 0 to 180 degrees
        pwm.ChangeDutyCycle(pwm_duty_cycle)
    else:
        debugPrint("Degree input outside expected range", SERVO_DRIVER)

##
# stop()
# Description: stop writing PWM signals.
##
def stop():
    pwm.ChangeDutyCycle(0)
runManual()
