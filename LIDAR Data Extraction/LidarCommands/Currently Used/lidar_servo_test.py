__author__ = 'Alex Schendel'
__date__ = '26/02/2018'

#############################HEAD########################################
# This file is to test compatability between the RPi and the server motor
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
GPIO.setmode(GPIO.BCM) #Use board pin numbering
GPIO.setup(18, GPIO.OUT) #Setup SERVO_PIN to OUT

def run():
    GPIO.output(18, GPIO.LOW) #Turn off SERVO_PIN
    state=False;
    while True:#switch output either high or low
        input("Press any key to switch pin")
        if state:
            GPIO.output(18, GPIO.LOW)
            state=False
        else:
            GPIO.output(18, GPIO.HIGH)
            state=True
run()
