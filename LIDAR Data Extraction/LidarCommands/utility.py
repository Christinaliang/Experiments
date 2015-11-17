
__author__="Sully Cothran"
__copyright__="October 26, 2015"
__version__= 0.10

#from testScript import *
import math
import numpy as np

global debug


def decodeHMZ(string,angle,scanStartAngle):
    #get the first letter of the result string
    firstLetter = string[0:1]

    #set the resolution (for default, .25 degrees per scan)
    resolution = 0.25
    
    #output data
    dataOutput = ""

    #get the whole result string except for first letter
    # string = string[:len(string)-1]

    #init the result lists
    # results = []
    # coordList = []
    x = []
    y = []
    z = []

    #pre calculate sine of phi and cosine of phi
    
    sinePhi = math.sin(math.pi/2)
    cosPhi = math.cos(math.pi/2)

    #set the number of chars per result based off of first letter of result string
    numChars = 3

    #for each set of char values, decode the distance value and determine cartesian coords
    count = 0
    for i in range(numChars - 1, len(string)-1, numChars):

        #Get the lower value
        lower = ord(string[i]) - 48

        #Get the middle value(upper for 2char decoding, middle for 3char decoding (shift left logically 6)
        middle = (ord(string[i - 1]) - 48) << 6

        #shift left logically 12
        upper = (ord(string[i-2]) - 48) << 12

        #put the value together with rest
        value =  upper + middle + lower

        #get the current angle of the scanner for this value (may need to be changed for values)
        currentAngle = math.radians(scanStartAngle + count*resolution)

        #if value > 500:
        #    value =  0

        #if(count % 5 == 0):
        #    print currentAngle
        # debugPrint("Angle of Scan: " + str(math.degrees(currentAngle)))

        #find the cartesian coordinates
        # coords = (value*sinePhi*math.cos(currentAngle),value*sinePhi*math.sin(currentAngle),value*cosPhi)
        
        xCoord = value*math.cos(currentAngle)
        yCoord = value*math.sin(currentAngle)
        zCoord = 0#value*cosPhi

        yc = yCoord*math.cos(angle)
        zc = yCoord*(-1*math.sin(angle))

        yCoord = yc
        zCoord = zc
        #rotation_matrix = np.matrix(    (  (1,0,0),(0,math.cos(angle),-math.sin(angle)),(0,math.sin(angle),math.cos(angle))))
        
        #coord_matrix = np.matrix(((xCoord,yCoord,zCoord)))

        #result_matrix = coord_matrix * rotation_matrix

        #xCoord = result_matrix.item(0)
        #yCoord = result_matrix.item(1)
        #zCoord = result_matrix.item(2)

        #xCoord = xCoord*math.cos(angle) - yCoord*math.sin(angle)
        ##yCoord = yCoord*math.cos(angle) + zCoord*math.sin(angle)
        #zCoord = zCoord*math.cos(angle) - yCoord*math.sin(angle)
        #display those coords
        # print coords
        xCoord = smallToZero(xCoord)
        yCoord = smallToZero(yCoord)
        zCoord = smallToZero(zCoord)

        dataOutput += "Angle: " + str(math.degrees(currentAngle)) + " Dist: " + str(value/10) +  " X: " + str(xCoord) + " Y: " + str(yCoord) + " Z: " + str(zCoord) + '\n'
        #add values to results
        x.append(xCoord)
        y.append(yCoord)
        z.append(zCoord)
        count += 1
    # print "Final Count: " + str(count)
    return x, y, z, scanStartAngle + count*resolution, dataOutput

def smallToZero(val):
    if val < .001 and val >= -.001:
        return 0
    return val

##
# debugPrint
#
# Description: prints the specified string only when debug boolean is set to True
#
# __params__
##
def debugPrint(str):
    if debug is None:
        setDebug()

    if debug:
        print str
    return

def setDebug(ison=False):
    debug = ison


## UNIT TEST FOR DECODE ##
print "Unit test 1"
X, Y, Z, scanAngle, dataOutput = decodeHMZ(str('0CB0'), 0, 0)
if dataOutput == str('Angle: 0.0 Dist: 123 X: 1234.0 Y: 0 Z: 0\n'): print "Passed."
else: print "failed."



