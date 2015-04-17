__author__ = 'Matt'

##
# This file starts the UI and network communications each in their own thread
#
#

from UI.UiRunner import *
from UI.network.RobotDataClient import *
from UI.RobotData import ManualControlData

# Makeshift global variable.
#   Pass around the array and change it's contents to change it globally
robotData = [RobotData()]
uiData = ManualControlData()


# The objects that do everything
dataClient = RobotDataClient(robotData)
uiRunner = UiRunner(robotData, uiData, dataClient)

# start the threads
dataClient.start()
uiRunner.start()