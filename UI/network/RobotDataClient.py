__author__ = 'Matt'

# from RobotData import RobotData
from DataTransferProtocol import receiveData
import socket

import threading

# from DataTransferProtocol import sendData, receiveData
# test_dataBox = [RobotData()]


SERVER_IP = '192.168.1.137'


##
# A class that manages data transfer to the server(probably the robot that is producing data)
#   It first connects to server and then receives data from it
#
class RobotDataClient(threading.Thread):

    def __init__(self, dataBox):

        self.dataBox = dataBox

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_address = ('192.168.1.137', 10000)
        # server_address = ('localhost', 10000)
        server_address = (SERVER_IP, 10000)
        self.socket.connect(server_address)

        self.socket.setblocking(0)

        threading.Thread.__init__(self)

        return

    def run(self):

        while True:
            try:
                self.dataBox[0] = receiveData(self.socket)
            except Exception:
                doNothing = 0

        return
