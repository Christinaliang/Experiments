__author__ = 'Matt'


class RobotData:

    def __init__(self):

        self.frontLeftWheel = wheel(0, 0.5, 0)
        self.frontRightWheel = wheel(0, 0.5, 0)
        self.midLeftWheel = wheel(0, 0.5, 0)
        self.midRightWheel = wheel(0, 0.5, 0)
        self.rearLeftWheel = wheel(0, 0.5, 0)
        self.rearRightWheel = wheel(0, 0.5, 0)

        self.currentLocation = location(0, 0)

class wheel:

    MAX_CURRENT = 5

    def __init__(self, theta, speed, current):
        # Rotation of wheels relative to body. 0 is East relative to the robot
        self.theta = theta

        # Speed wheels are being told to drive
        self.speed = speed

        # Current draw of wheel motors
        self.current = current

##
# This class defines the position of the robot. The arena is 3.78m by 7.38m. the expanded
# robot is 1.2x1.5
#
#  3.78 meters (x)           pi / 2 rads
#   +-----+-----+             |
#   |     |     |             N
#   |     |     | pi rads - W + E - 0 rads
#   |     |     |             S
#   |     |     |             |
#   |     |     |          3 pi / 2 rads
#   |     |     |
#   |     |     |  7.38 meters (y)
#   +-----+-----+
#       (0,0)
#
# The origin is located at the exact center of the arena. Relative north is
# facing the end of the arena (as shown above).
#
# Variables:
# x - denotes the x position of the center of the robot (meters). -1.89 <= x <= +1.89
# y - denotes the y position of the center of the robot (meters). 0 <= y <= 7.38
# theta - the number of radians turned from E(ast); as the unit circle
#
# TODO: use verification to make sure that the robot does not hit the edges/go outside the arena.
# TODO: functions about travel.
##
class location:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta