__author__ = 'Matt'

from RobotDataClient import RobotDataClient
from UI.RobotData import ManualControlData
from DataTransferProtocol import sendData

data = ManualControlData()
data.fl_articulation_angle = 0
data.fr_articulation_angle = 0
data.ml_articulation_angle = 0
data.mr_articulation_angle = 0
data.rl_articulation_angle = 0
data.rr_articulation_angle = 0

data.fl_drive_speed = 0
data.fr_drive_speed = 0
data.ml_drive_speed = 0
data.mr_drive_speed = 0
data.rl_drive_speed = 0
data.rr_drive_speed = 0

client = RobotDataClient([None])

sendData(client.socket, data)
