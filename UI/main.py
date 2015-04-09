__author__ = 'Matt'

##
# This file starts the UI and network communications each in their own thread
#
#

from UI.UiRunner import *
from UI.network.RobotDataClient import *

# Makeshift global variable.
#   Pass around the array and change it's contents to change it globally
theData = [RobotData()]

# The objects that do everything
dataClient = RobotDataClient(theData)
uiRunner = UiRunner(theData)

# start the threads
dataClient.start()
uiRunner.start()