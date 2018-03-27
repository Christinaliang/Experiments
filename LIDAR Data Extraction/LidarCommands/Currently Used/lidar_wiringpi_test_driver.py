import time
from constants import *

# Use GPIO naming convention
wiringpi.wiringPiSetupGpio()

# set SERVO_PIN to PWM output
wiringpi.pinMode(SERVO_PIN, wiringpi.GPIO.PWM_OUTPUT)

# set PWM mode to milliseconds
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

#divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = 0.01

while True:
    for pulse in range(50, 250, 1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)
    for pulse in range(250, 50, -1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)