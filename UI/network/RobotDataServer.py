__author__ = 'Matt'

from UI.RobotData import RobotData
import socket

import threading
from DataTransferProtocol import receiveData, sendData


##
# robotDataDistributor
#
# Description: Thread that accepts network connections from clients and spawns a new thread to handle the connection
#
class robotDataDistributor(threading.Thread):

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

        # Until the server closes, accept connections and spawn a thread to handle them
        while True:
            (clientsocket, address) = s.accept()
            print "Received connection from: " + address[0]
            cs = robotDataServer(clientsocket, self, address)
            cs.run()

        return


##
# robotDataServer
#
# Description: Handles a connection with a particular client. Receives commands and sends data about the robot.
#
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

                self.socket.setblocking(1)

                # Send the robot data to the client
                sendData(self.socket, self.distributor.data)

                # An extra exception because we have a non-blocking socket
                try:
                    self.socket.setblocking(0)

                    # Receive a command and add it to the command queue
                    newCommand = receiveData(self.socket)
                    commandQueue.append(newCommand)

                    # print manualControlCommand.go_forward

                except socket.error:
                    continue

        except socket.error as e:
            print "Lost connection with " + self.address[0]
            return

        return


commandQueue = []
rdd = robotDataDistributor()
rdd.start()

while True:

    # Process a command
    if len(commandQueue) > 0:
        command = commandQueue.pop(0)

        # TODO: stuff with the command
        print command.go_forward

    # Update Robot data

    rdd.data.frontLeftWheel.theta += 0.01
    rdd.data.frontLeftWheel.theta %= 1000000