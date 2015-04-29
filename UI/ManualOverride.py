__author__ = 'Matt'
import time
from UI.network.RobotDataClient import RobotDataClient
from UI.RobotData import ManualControlData
from UI.network.DataTransferProtocol import sendData, receiveData

data = ManualControlData()
data.fl_articulation_angle = 0
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
print "First command sent"
time.sleep(3)
data.e_stop = True
sendData(client.socket, data)
print "E-stop sent"
time.sleep(1)
client.socket.close()
