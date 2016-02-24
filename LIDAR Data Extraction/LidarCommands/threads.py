
__author__="Jaimiey Sears, Sully Cothran"
__copyright__="January 31, 2016"
__version__= 2

import Queue
import threading
import socket
from utility import *
from constants import *
from display import *
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
    wbSave('test_data/{}'.format(generateStampedFileName('.xlsx')), lt.processedDataArrays,False)

    th1_stop.set()
    th2_stop.set()

    filterscans(lt.processedDataArrays[0],lt.processedDataArrays[1],lt.processedDataArrays[2])


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
        except socket.timeout, e:
            debugPrint("I can't connect. Exiting.", SOCKET_MSG)
            exit(-1)

        # dataQueue is a Queue of strings
        # each string representing a slice (scan)
        self.dataQueue = Queue.Queue()

        self.processedDataArrays = [[],[],[],[],[],[]]

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

                # wait for the Queue to empty so we don't overflow the buffer
                # while dataQueue.qsize() > 0:
                #   pass

                # get the starting theta angle
                self.slitAngle = START_ANGLE

                for x in range(SCAN_AVERAGE_COUNT):
                    # send scan request to the LIDAR
                    self.socket.send("{}\n".format(self.command))

                    try:
                        # get rid of the intro information
                        intro = self.socket.recv(21) #response message
                        intro += self.socket.recv(26) #scan response intro
                    except:
                        pass
                    # input("paused")
                    debugPrint(intro, SOCKET_DATA)

                    data = ''
                    # receive data from the LIDAR
                    for j in range(0, 1024):
                        try:
                            # time.sleep(0.01)
                            # get a line of data from the LIDAR queue
                            temp = self.socket.recv(66)

                            debugPrint(temp, SOCKET_DATA)
                            if len(temp) == 66:
                                data += temp[:-2]
                            else:
                                data += temp[:-3]

                            # format the data we've recieved
                            # data = temp.split("\n")
                            # data.reverse()
                        except socket.timeout, e:
                            debugPrint("waiting for data", SOCKET_MSG)
                            break

                    try:
                        dataQueue.put((data, angleRadians))
                    except Queue.Full, e:
                        debugPrint("Data Queue is full.", SOCKET_MSG)
                        continue
                counter += 1.0
                angleDegrees += 10
                raw_input("Turn to {} degrees and press enter\n".format(angleDegrees))

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

        # emptied indicates whether the queue has been exhausted (primarily for debug printing purposes)
        emptied = False

        while not stop_event.is_set():

            if dataQueue.qsize() < SCAN_AVERAGE_COUNT:
                continue

            try:

                dataList = []
                for i in range(SCAN_AVERAGE_COUNT):
                    # get a scan of data from the queue
                    data, anglePhi = dataQueue.get(timeout=0.05)
                    dataList.append(data)

                X, Y, Z, DISTS, PHIS, THETAS = decode_new(dataList, anglePhi)

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

            except Queue.Empty, e:
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