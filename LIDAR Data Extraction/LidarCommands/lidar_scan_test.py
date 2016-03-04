__author__ = 'Jaimiey'
__version__ = 1

from threads import main as runTest
import datetime as dt
from lidar_servo_driver import *

# Get information from user regarding number of test cases
try:
    ip = int(raw_input("Number of scans to do: "))
except ValueError:
    print "Not a valid number. Exiting"
    raise SystemExit

# run x tests, prompting for input
for i in range(ip):
    for j in range(3): print "----------------------------------"
    turnTo(180 + ANGLE_OFFSET)
    print "Beginning Scan {} at {}".format(i, dt.datetime.now())
    runTest()

print "\nAll Tests Complete at {}".format(dt.datetime.now())
