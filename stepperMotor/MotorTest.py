import serial
ser = serial.Serial('/dev/tty.usbmodem411', 9600)

while True:
    desiredDegree = raw_input('How many degrees do you want to rotate? \n')
    ser.write(desiredDegree)

# Drive Function
# parameters we want are
# direction, velocity, time
# CASES: +degree (left turn)
#        -degree (right turn)
#        0 degree (straight)
#        +- 90 degree (perpendicular)



# Pivot Function
# parameters we want are
# angular velocity, direction
# CASES: clockwise, direction = 1
#        counter-clockwise direction = 0

# Pack/Unpack function