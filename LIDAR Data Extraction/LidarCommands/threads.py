
__author__="Jaimiey Sears"
__copyright__="October 26, 2015"
__version__= 0.15

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import Queue
import threading
import time
import socket
import logging
from utility import *
# import usb, binascii, math, argparse, struct, sys

#######################
#  UNIT TEST 1 START  #
#######################
def main():
    lt = LidarThreads(debug=False)

    # make the first string for reading LIDAR data
    lt.debugPrint("Starting")
    th1_stop = threading.Event()
    th1 = threading.Thread(target=lt.produce, args=(lt.dataQueue, th1_stop,), name="data_reader")
    lt.debugPrint("Done making thread 1")

    # make the second string to process the LIDAR data
    th2_stop = threading.Event()
    th2 = threading.Thread(target=lt.consume, args=(lt.dataQueue, th2_stop,), name="cartesian_converter")
    lt.debugPrint("done making thread 2")

    # start both strings
    th1.start()
    th2.start()

    # operation time = 3.0 seconds
    # time.sleep(3.0)

    # close the threads down
    while th1.isAlive():
        # th1_stop.set()
        th1.join(1.0)

    #print "producer stopped"

    while th2.isAlive():
        th2_stop.set()
        th2.join(1.0)

    #print "consumer stopped"
    #print "\n\n\n"
    #print "Final Data:"
    #print "__________________________"
    #print "=========================="
    #print "X = {}".format(lt.processedDataArrays[0])
    #print "Y = {}".format(lt.processedDataArrays[1])
    #print "Z = {}".format(lt.processedDataArrays[2])

    # th1_stop.set()
    # th2_stop.set()
    #
    # th1.join(1.0)
    # if th1.isAlive():
    # 	print "producer still running."
    # th2.join(1.0)
    # if th2.isAlive():
    # 	print "consumer still running."

    time.sleep(0.5)
    winSize = 200

    plt.scatter(lt.processedDataArrays[0],lt.processedDataArrays[1],c='r')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(-1*winSize,winSize)

    plt.scatter(lt.processedDataArrays[1],lt.processedDataArrays[2],c= 'b')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(-1*winSize,winSize)

    plt.scatter(lt.processedDataArrays[0],lt.processedDataArrays[2],c= 'g')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(-1*winSize,winSize)

    fig = plt.figure()
    print "Number of Data Points: " + str(len(lt.processedDataArrays[0]))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1*winSize,winSize)
    ax.set_ylim(-1*winSize,winSize)
    ax.set_zlim(-1*winSize,winSize)
    zArray = []
    #to see what order the data points are recived, lowest height is first
    #for i in range(0,len(lt.processedDataArrays[0])):
        #zArray.append(i)
    ax.scatter(lt.processedDataArrays[0],lt.processedDataArrays[1],lt.processedDataArrays[2],c=lt.processedDataArrays[2])

    commandFile = open("lidar_commands.txt",'w')
    commandFile.write("{}".format(lt.commandOutput))
    commandFile.close()

    commandFile = open("lidar_data.txt",'w')
    commandFile.write("{}".format(lt.dataOutput))
    commandFile.close()

    plt.show()
    lt.debugPrint("Done running threads")
    lt.debugPrint("exiting with code {}".format(lt.exit()))
    lt.debugPrint("queue size at exit: {}".format(lt.dataQueue.qsize()))
    raise SystemExit
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
    def __init__(self, debug=False):
        # don't forget: netsh interface ip set address "Local Area Connection" static 192.168.0.100
        global nhokreadings

        # controls a number of debug statements which should only print sometimes
        self.debug = debug

        self.commandOutput = ""
        self.dataOutput = ""

        self.slitAngle = -45

        #command to get data from the lidar
        self.command = 'MD'+'0000'+'1080'+'00'+'0'+'01'

        # establish communication with the sensor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.settimeout(0.1)
            self.socket.connect(("192.168.0.10", 10940))
        except socket.timeout, e:
            self.debugPrint("I can't connect. Exiting.")
            exit(-1)

        # dataQueue is a Queue of strings
        # each string representing a slice (scan)
        self.dataQueue = Queue.Queue()

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
        # self.socket.send('PP\n')

        while not stop_event.is_set():

            #simulate a move of the LIDAR scanner
            time.sleep(0.05)
            while dataQueue.qsize() > 0:
                pass
            self.slitAngle = -45
            inp = input("Enter Scan Angle: ")
            if not isinstance(inp,int):
                print "enter an integer"
                break
            angle = math.radians(int(inp))

            # get data from the LIDAR scanner
            self.socket.send("{}\n".format(self.command))
            #time.sleep(0.05) #simulate scan-time


            #data = "{0} : This_is_a_string_containing_data".format(counter)
            for i in range(0, 4500):
                try:
                    temp = self.socket.recv(4500)
                    #print "\nSocket.Recv: " + temp
                    #print len(temp)
                    data = temp.split("\n")
                    #print len(data)
                    data.reverse()
                except socket.timeout, e:
                    self.debugPrint("waiting for data")
                    break

                while data:
                    try:
                        str = data.pop()#.replace("\\","\\\\")
                        self.debugPrint("Producer : "+str)
                        dataQueue.put((str, angle))

                    except Queue.Full, e:
                        print "Data Queue is full."
                        continue
                counter += 1.0

        # close thread
        # raise SystemExit

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
        counter = 0
        xLines = []
        yLines = []
        zLines = []

        dataSet = ""
        while not stop_event.is_set():

            try:
                # get some data from the queue, process it to cartesian
                dataline, anglePhi = dataQueue.get(timeout=0.25)

                if dataline == "":
                    if not dataSet == "":
                        #print "Length of dataSet: " + str(len(dataSet))
                        for string in splitNparts(dataSet,64):
                            #print "String: " + string + '\n'
                            X, Y, Z, lastAngle, outVal = decodeHMZ(string, anglePhi, self.slitAngle)
                        
                            self.slitAngle = lastAngle

                            xLines = xLines + X
                            yLines = yLines + Y
                            zLines = zLines + Z
                    dataSet = ""
                    continue
                elif dataline == self.command:
                    counter = 0
                else:
                    counter += 1

                # self.debugPrint("Consumer: " + )
                self.debugPrint("Consumer: data= {}".format(dataline))

                self.commandOutput += dataline + '\n'
                if counter >= 5:
                    dataSet = dataSet + dataline
                    #print dataline
                    # dists, coords= decode(dataline, math.pi/2, 90)
                    

                # if counter == 5:
                #     print "Consumer: dists(mm)=", dists, "; coords=", coords
                #     print "\tqueue size= ", dataQueue.qsize()



            except Queue.Empty, e:
                self.debugPrint( "Data Queue is empty")
                continue

        self.processedDataArrays = (xLines, yLines, zLines)

    ##
    # debugPrint
    #
    # Description: prints the specified string only when debug boolean is set to True
    #
    # __params__
    ##
    def debugPrint(self, str):
        if self.debug:
            print str
        return

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


# run the program
main()