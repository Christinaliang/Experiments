
__author__="Sully Cothran"
__copyright__="October 26, 2015"
__version__= 0.5

import math, time
import datetime as dt
from constants import *

def decodeHMZ(string,angle,scanStartAngle):
    #get the first letter of the result string
    firstLetter = string[0]
    lastLetter = string[len(string)-1]

    #set the resolution (for default, .25 degrees per scan)
    resolution = 0.25
    
    #output data
    dataOutput = ""

    #init the result lists
    dists = []
    x = []
    y = []
    z = []
    phis = []
    thetas = []

    # #pre calculate sine of phi and cosine of phi
    # sinePhi = math.sin(math.pi/2)
    # cosPhi = math.cos(math.pi/2)

    #set the number of chars per result based off of first letter of result string
    NUM_CHARS = 3

    #for each set of char values, decode the distance value and determine cartesian coords
    count = 0
    for i in range(NUM_CHARS - 1, len(string)-1, NUM_CHARS):

        # record phi
        phis.append(angle)

        # Just decode an N-letter section of the data
        dist = decodeShort(string[i-(NUM_CHARS-1):i+1])
        dists.append(dist)

        #get the current angle of the scanner for this value (may need to be changed for values)
        currentAngle = math.radians(scanStartAngle + count*RESOLUTION)
        thetas.append(currentAngle)

        #find the cartesian coordinates
        xCoord = dist*math.cos(currentAngle)
        yCoord = dist*math.sin(currentAngle)
        # zCoord = 0    # value*cosPhi

        yc = yCoord*math.cos(angle)
        zc = yCoord*(-1*math.sin(angle))

        yCoord = yc
        zCoord = zc

        # print coords
        xCoord = smallToZero(xCoord)
        yCoord = smallToZero(yCoord)
        zCoord = smallToZero(zCoord)

        dataOutput += "Angle: " + str(math.degrees(currentAngle)) + " Dist: " + str(dist/10) +  " X: " + str(xCoord) + " Y: " + str(yCoord) + " Z: " + str(zCoord) + '\n'
        #add values to results
        x.append(xCoord)
        y.append(yCoord)
        z.append(zCoord)
        count += 1

    # print "Final Count: " + str(count)
    # print "Distances: ", dists
    return x, y, z, scanStartAngle + count*resolution, dataOutput, phis, thetas, dists

def splitNparts(string, n):
    doSplit = True
    strList = []
    while(doSplit):
        if string == "":
            return strList
        if(len(string) < n):
            strList.append(string)
            return strList
        else:
            strList.append(string[0:n])
            string = string[n:len(string)]


def smallToZero(val):
    if abs(val) < .001:
        return 0
    return val

def decodeShort(dataStr):
    result = 0
    for i in range(len(dataStr)):
        index = len(dataStr)-1-i
        #Get the lower value
        temp = (ord(dataStr[index]) - 0x30) << (i*6)

        #put the value together with rest
        result += temp

    return result

def generateStampedFileName():
    timestamp = dt.datetime.now()
    return "test_vectors_{}_{}_{}_{}_{}_{}.xlsx".format(timestamp.year, timestamp.month, timestamp.day,\
           timestamp.hour, timestamp.minute, timestamp.second)

##
# debugPrint
#
# Description: prints the specified string only when debug boolean is set to True
#
# __params__
##
def debugPrint(string, lvl):
    if DEBUG_LEVEL >= lvl:
        print "{}:\n{}".format(DEBUG_SRC[lvl], string)
    return


## UNIT TESTS FOR DECODE ##
debugPrint("Unit test 1", UTILITY)
X, Y, Z, scanAngle, dataOutput, TH, PHI, DIST= decodeHMZ(str('0CB0'), 0, 0)
if dataOutput == str('Angle: 0.0 Dist: 123 X: 1234.0 Y: 0 Z: 0\n'): debugPrint( "Long Decode Passed.\n", UTILITY)
else: debugPrint("Long decode failed with {}\n".format(dataOutput), UTILITY)

debugPrint( "Unit test 2", UTILITY)
result = decodeShort(str('CB'))
if str(result) == str('1234'): debugPrint("Short decode Passed.\n", UTILITY)
else: debugPrint( "Short decode failed with {}".format(result), UTILITY)

debugPrint( "Unit test 3", UTILITY)
result = splitNparts("HelloHelloHello",5)
if result == ["Hello", "Hello","Hello"]: debugPrint( "Split 5 Parts Passed.\n", UTILITY)
else: debugPrint( "Split 5 Failed with {}".format(result), UTILITY)

debugPrint( "Unit test 4", UTILITY)
result = splitNparts("HelloHelloHello",4)
if result == ["Hell", "oHel","loHe","llo"]: debugPrint("Split 4 Parts Passed.\n", UTILITY)
else: debugPrint( "Split 4 Failed with {}".format(result), UTILITY)