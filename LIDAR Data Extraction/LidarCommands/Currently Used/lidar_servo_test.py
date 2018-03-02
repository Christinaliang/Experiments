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

GPIO.setmode(GPIO.BOARD) #Use board pin numbering
GPIO.setup(SERVO_PIN, GPIO.OUT) #Setup SERVO_PIN to OUT
GPIO.output(SERVO_PIN, GPIO.LOW) #Turn off SERVO_PIN
state=False

def run():
    while True:
        input("Press any key to switch pin")
        if state:
            GPIO.output(SERVO_PIN, GPIO.LOW)
            state=False
        else:
            GPIO.output(SERVO_PIN, GPIO.HIGH)
            state=True
