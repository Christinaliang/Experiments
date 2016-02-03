__author__ = 'Jaimiey'

####### GENERAL PURPOSE CONSTANTS #######
OPERATION_SUCCESS = 0
OPERATION_FAILURE = -1

# indexes of lidar data in processedDataArrays
X_IDX = 0
Y_IDX = 1
Z_IDX = 2
D_IDX = 3
PHI_IDX = 4
TH_IDX = 5


# Starting theta angle of our scans
START_ANGLE = 0

#Scanner offset from rotation point (0,0,0)
Y_OFFSET = 51.84
Z_OFFSET = 0

# Resolution of LIDAR scans. this should change based on grouping
RESOLUTION = 0.25

####### DEBUG MESSAGE CONSTANTS #######
# Debug level for different message levels.
# 0 = only essential messages
# 1 = print ROSta messages
# 2 = print producer and consumer messages
# 3 = print producer and consumer data
# 4 = print data as it is processed (for use in utility.py)
ROSTA = 1
SOCKET_MSG = 2
SOCKET_DATA = 3
UTILITY = 4
SERVO_DRIVER = 5
DEBUG_LEVELS = [ROSTA, SERVO_DRIVER, SOCKET_MSG]


####### SERVO CONTROL CONSTANTS #######
#initial setup
# pwm frequency is 50 Hz
PWM_FREQ = 50
# connect to BCM pin 21 on RPi
SERVO_PIN = 21

# pwm range is 1.8 to 11.9
PWM_MIN = 1.8
PWM_MAX = 11.9
DEGREE_MIN = 0
DEGREE_MAX = 200


Y_OFFSET = 51.84
Z_OFFSET = 0
