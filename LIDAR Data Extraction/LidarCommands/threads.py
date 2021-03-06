
__author__="Jaimiey Sears, Sully Cothran"
__copyright__="January 31, 2016"
__version__= 2

import queue
import threading
import socket
from utility import *
from constants import *
# from lidar_servo_driver import turnTo

##############################
#  PROGRAM MAIN ENTRY POINT  #
##############################
def main():
    lt = LidarThreads()

    # make the first string for reading LIDAR data
    debugPrint("Starting", ROSTA)
    th1_stop = threading.Event()
    th1 = threading.Thread(target=lt.produce, args=(lt.dataQueue, th1_stop,), name="data_reader")
    debugPrint("Done making thread 1", ROSTA)

    # make the second string to process the LIDAR data
    th2_stop = threading.Event()
    th2 = threading.Thread(target=lt.consume, args=(lt.dataQueue, th2_stop,), name="cartesian_converter")
    debugPrint("done making thread 2", ROSTA)

    # start both strings
    th1.start()
    th2.start()

    # close the threads down
    while th1.isAlive():
        # th1_stop.set()
        th1.join(1.0)

    debugPrint("producer stopped", ROSTA)

    while th2.isAlive():
        th2_stop.set()
        th2.join(1.0)

    debugPrint("consumer stopped", ROSTA)

    #save into an excel worksheet
    # wbSave('test_data/{}'.format(generateStampedFileName('.xlsx')), lt.processedDataArrays)

    th1_stop.set()
    th2_stop.set()

    debugPrint("Done running threads", ROSTA)
    debugPrint("exiting with code {}".format(lt.exit()), ROSTA)
    debugPrint("queue size at exit: {}".format(lt.dataQueue.qsize()), ROSTA)
#####################
## UNIT TEST 1 END ##
#####################


##
# Placeholder for cartesian conversion ftn
##
def sphericalToCartesian(data):
    time.sleep(0.005)
    #print("Placeholder: Cartesian map conversion")
    return data


##
# LidarThreads
# class controls threads for gathering LIDAR data
# **Version 0.10 the actual functions are simulated with time.sleep statements**
##
class LidarThreads():
    def __init__(self):
        # don't forget: netsh interface ip set address "Local Area Connection" static 192.168.0.100
        global nhokreadings

        self.commandOutput = ""
        self.dataOutput = ""

        self.slitAngle = START_ANGLE

        #command to get data from the lidar
        self.command = 'MD'+'0180'+'0900'+'00'+'0'+'01'

        # establish communication with the sensor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.settimeout(.1)
            self.socket.connect(("192.168.0.10", 10940))
        except socket.timeout as e:
            debugPrint("I can't connect. Exiting.", SOCKET_MSG)
            exit(-1)

        # dataQueue is a Queue of strings
        # each string representing a slice (scan)
        self.dataQueue = queue.Queue()

        self.processedDataArrays = []

    ##
    # produce
    #
    # Description: gets data from the LIDAR unit, puts it into the queue
    #
    # Parameters:
    #   dataQueue - queue to submit data to
    #   stop_event - event to listen to for exit
    ##
    def produce(self, dataQueue, stop_event):
        counter = 0
        angleDegrees = 0

        #while not stop_event.is_set():
        for i in range (0,10):

                # rotate the lidar to the correct degree setting
                # turnTo(angleDegrees)
                angleRadians = math.radians(int(angleDegrees))
                # move the angle 10 degrees for next run
                # TODO: move to bottom of fn
                angleDegrees += 10

                # wait for the Queue to empty so we don't overflow the buffer
                while dataQueue.qsize() > 0:
                  pass

                # get the starting theta angle
                self.slitAngle = START_ANGLE

                # send scan request to the LIDAR
                self.socket.send(("{}\n".format(self.command)).encode())


                # get rid of the intro information
                intro = self.socket.recv(21) #response message
                intro += self.socket.recv(26) #scan response intro
                # print intro
                # input("paused")
                debugPrint(intro, SOCKET_DATA)

                data = ''
                # receive data from the LIDAR
                for j in range(0, 1024):
                    try:
                        # time.sleep(0.01)
                        # get a line of data from the LIDAR queue
                        temp = self.socket.recv(66)
                        if len(temp) == 66:
                            data += temp[:-2].decode()
                        else:
                            data += temp[:-3].decode()

                        # format the data we've recieved
                        # data = temp.split("\n")
                        # data.reverse()
                    except socket.timeout as e:
                        debugPrint("waiting for data", SOCKET_MSG)
                        break

                try:
                    dataQueue.put((data, angleRadians))
                except queue.Full as e:
                    debugPrint("Data Queue is full.", SOCKET_MSG)
                    continue
                counter += 1.0

    ##
    # consume
    #
    # Description: consumes data from the queue
    #
    # Parameters:
    #   dataQueue - queue to consume from
    #   stop_event - the event to watch for quitting.
    ##
    def consume(self, dataQueue, stop_event):
        # TODO delete
        # counter = 0
        # xLines = []
        # yLines = []
        # zLines = []
        # phiLines = []
        # thetaLines = []
        # distLines = []
        #
        # dataSet = ""

        # emptied indicates whether the queue has been exhausted (primarily for debug printing purposes)
        emptied = False

        while not stop_event.is_set():
            try:
                # get a scan of data from the queue
                data, anglePhi = dataQueue.get(timeout=0.05)
                X, Y, Z, DISTS, PHIS, THETAS = decode_new(data, anglePhi)

                # print the data in a debug message
                debugPrint("X:{}\n\nY:{}\n\nZ:{}\n\nD:{}\n\nPH:{}\n\nTH:{}"
                           .format(X,Y,Z,DISTS,PHIS,THETAS), SOCKET_DATA)

                # add the data to the global variable
                self.processedDataArrays[X_IDX] += X
                self.processedDataArrays[Y_IDX] += Y
                self.processedDataArrays[Z_IDX] += Z
                self.processedDataArrays[D_IDX] += DISTS
                self.processedDataArrays[PHI_IDX] += PHIS
                self.processedDataArrays[TH_IDX] += THETAS

            except queue.Empty as e:
                if not emptied:
                    debugPrint( "Data Queue is empty", SOCKET_MSG)
                    emptied = True
                continue

    ##
    # exit
    #
    # Description: closes out the socket
    # returns: 0 on success, -1 on failure
    ##
    def exit(self):
        if not self.socket is None:
            self.socket.close()
            return 0
        else:
            return -1

