__author__ = 'Matt'


class data:

    def __init__(self):

        self.frontLeftWheel = wheel(0, 0.5, 0)
        self.frontRightWheel = wheel(0, 0.5, 0)
        self.midLeftWheel = wheel(0, 0.5, 0)
        self.midRightWheel = wheel(0, 0.5, 0)
        self.rearLeftWheel = wheel(0, 0.5, 0)
        self.rearRightWheel = wheel(0, 0.5, 0)


class wheel:

    MAX_CURRENT = 5

    def __init__(self, theta, speed, current):
        # Rotation of wheels relative to body. 0 is facing forwards
        self.theta = theta

        # Speed wheels are being told to drive
        self.speed = speed

        # Current draw of wheel motors
        self.current = current