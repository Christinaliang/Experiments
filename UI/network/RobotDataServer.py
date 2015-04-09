__author__ = 'Matt'

from UI.RobotData import RobotData
import socket

#cPicke is faster
try:
    import cPickle as pickle
except ImportError:
    import pickle

import threading


class robotDataDistributer(threading.Thread):

    def __init__(self):
        self.data = RobotData()
        threading.Thread.__init__(self)
        return

    def run(self):
        # configure the socket to receive incoming sockets
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 10000)
        s.bind(server_address)
        s.listen(1)

        while True:
            (clientsocket, address) = s.accept()
            print "Received connection from: " + address[0]
            cs = robotDataServer(clientsocket, self, address)
            cs.run()

        return


class robotDataServer(threading.Thread):

    def __init__(self, sock, distributor, address):

        self.socket = sock
        self.distributor = distributor
        self.address = address

        threading.Thread.__init__(self)

        return

    def run(self):
        try:

            while True:

                data_string = pickle.dumps(self.distributor.data)

                length = str(len(data_string))
                while len(length) < 10:
                    length = "0" + length

                self.socket.send(length)
                self.socket.send(data_string)

        except socket.error:
            print "Lost connection with " + self.address[0]
            return

        return

rdd = robotDataDistributer()
rdd.start()

while True:
    rdd.data.frontLeftWheel.theta += 0.01
    rdd.data.frontLeftWheel.theta %= 1000000