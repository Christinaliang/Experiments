__author__ = 'Matt'

from UI.network.RobotDataClient import RobotDataClient
from RobotData import ManualControlData
from UI.network.DataTransferProtocol import sendData, receiveData

data = ManualControlData()
data.fl_articulation_angle = 350
data.fr_articulation_angle = 180
data.ml_articulation_angle = 0
data.mr_articulation_angle = 180
data.rl_articulation_angle = 0
data.rr_articulation_angle = 180

data.fl_drive_speed = 0
data.fr_drive_speed = 0
data.ml_drive_speed = 0
data.mr_drive_speed = 0
data.rl_drive_speed = 0
data.rr_drive_speed = 0

data.e_stop = False

client = RobotDataClient([None])

sendData(client.socket, data)

# Keep running the command, will E-STOP when program terminates
while True:
    try:
        receiveData(client.socket)
    except:
        print ""