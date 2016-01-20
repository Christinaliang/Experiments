__author__ = 'Jaimiey'
__version__ = 1

import RPi.GPIO as GPIO

#initial setup
FREQ = 50 #50 Hz
SERVO_PIN = 21 #BCM pin 21 on RPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, FREQ)
pwm.start(0)
#pwm range is 1.8 to 11.9
PWM_MIN = 1.8
PWM_MAX = 11.9
DEGREE_MIN = 0
DEGREE_MAX = 200

def run():
    while True:
        degree = input("What angle do you want me to turn to?\n")
        if isinstance(degree, int) and degree >= DEGREE_MIN and degree <= DEGREE_MAX:
            pwm_duty_cycle = (degree * (PWM_MAX-PWM_MIN) / (DEGREE_MAX-DEGREE_MIN)) + DEGREE_MIN
            pwm.ChangeDutyCycle(pwm_duty_cycle)
        else:
            print "Input should be a number of degrees [0, 200]"