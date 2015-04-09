__author__ = 'Matt'

from UI.RobotData import RobotData
import socket

import threading

#cPicke is faster
try:
    import cPickle as pickle
except ImportError:
    import pickle

test_dataBox = [RobotData()]


##
# A class that manages data transfer to the server(probably the robot that is producing data)
#   It first connects to server and then receives data from it
#
class RobotDataClient(threading.Thread):

    def __init__(self, dataBox):

        self.dataBox = dataBox

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 10000)
        self.socket.connect(server_address)

        threading.Thread.__init__(self)

        return

    def run(self):

        while True:
            self.receiveData()

        return

    ##
    # receiveData
    #
    # Description: Receive a serialized object string from the server and reformat it to an actual RobotData object
    #
    def receiveData(self):

        # first we get a string that says how long the serialized string is
        length = int(self.socket.recv(10))

        # We receive and convert a serialized object string to an actual RobotData object
        data_string = self.socket.recv(length)
        self.dataBox[0] = pickle.loads(data_string)
