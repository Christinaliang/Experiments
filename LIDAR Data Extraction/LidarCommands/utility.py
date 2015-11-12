__author__="Sully Cothran"
__copyright__="October 26, 2015"
__version__= 0.10

#from testScript import *
import math

global debug

def decode(string,angle,scanStartAngle):
    #get the first letter of the result string
    firstLetter = string[0:1]

    #set the resolution (for default, .25 degrees per scan) (for testing, using 45 degrees per scan
    resolution = 0.25

    #get the whole result string except for first letter
    string = string[:len(string)-1]

    #init the result lists
    results = []
    coordList = []

    #pre calculate sine of phi and cosine of phi
    sinePhi = math.sin(angle)
    cosPhi = math.cos(angle)

    #set the number of chars per result based off of first letter of result string
    numChars = 3

    #for each set of char values, decode the distance value and determine cartesian coords
    count = 0
    for i in range(numChars - 1,len(string),numChars):

        #Get the middle value(upper for 2char decoding, middle for 3char decoding (shift left logically 8)
        middle = int(ord(string[i - 1])) - 0x30 << 6
        #Get the lower value
        lower = int(ord(string[i])) - 0x30
        #put values together
        value = middle + lower
        #if we are using 3char decoding, find the upper part
        if numChars == 3:
            #shift left logically 16
            upper = (int(ord(string[i - 2])) - 0x30 << 12)
            #put the value together with rest
            value =  upper + value
        #get the current angle of the scanner for this value (may need to be changed for values)
        currentAngle = math.radians(scanStartAngle + count*resolution)

        #print angle
        # debugPrint("Angle of Scan: " + str(math.degrees(currentAngle)))

        #find the cartesian coordinates
        coords = (value*sinePhi*math.cos(currentAngle),value*sinePhi*math.sin(currentAngle),value*cosPhi)
        #display those coords
        # print coords

        #add values to results
        coordList.append(coords)
        results.append(value)
        # debugPrint(value)
        count += 1
    return (results, coordList)

def decodeHMZ(string,angle,scanStartAngle):
    #get the first letter of the result string
    firstLetter = string[0:1]

    #set the resolution (for default, .25 degrees per scan) (for testing, using 45 degrees per scan
    resolution = 0.25

    #get the whole result string except for first letter
    string = string[:len(string)-1]

    #init the result lists
    # results = []
    # coordList = []
    x = []
    y = []
    z = []

    #pre calculate sine of phi and cosine of phi
    sinePhi = math.sin(angle)
    cosPhi = math.cos(angle)

    #set the number of chars per result based off of first letter of result string
    numChars = 3

    #for each set of char values, decode the distance value and determine cartesian coords
    count = 0.0
    for i in range(numChars - 1,len(string),numChars):

        #Get the middle value(upper for 2char decoding, middle for 3char decoding (shift left logically 8)
        middle = int(ord(string[i - 1])) - 0x30 << 6
        #Get the lower value
        lower = int(ord(string[i])) - 0x30
        #put values together
        value = middle + lower
        #if we are using 3char decoding, find the upper part
        if numChars == 3:
            #shift left logically 16
            upper = (int(ord(string[i - 2])) - 0x30 << 12)
            #put the value together with rest
            value =  upper + value
        #get the current angle of the scanner for this value (may need to be changed for values)
        currentAngle = math.radians(scanStartAngle + count*resolution)

        if(count % 5 == 0):
            print currentAngle
        # debugPrint("Angle of Scan: " + str(math.degrees(currentAngle)))

        #find the cartesian coordinates
        # coords = (value*sinePhi*math.cos(currentAngle),value*sinePhi*math.sin(currentAngle),value*cosPhi)
        xCoord = value*sinePhi*math.cos(currentAngle)
        yCoord = value*sinePhi*math.sin(currentAngle)
        zCoord = value*cosPhi
        #display those coords
        # print coords
        xCoord = smallToZero(xCoord)
        yCoord = smallToZero(yCoord)
        zCoord = smallToZero(zCoord)
        #add values to results
        x.append(xCoord)
        y.append(yCoord)
        z.append(zCoord)
        count += 1.0
    return x, y, z

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


# result, coords = decode("0005005005005005005005",math.pi/2)

#for testing purposes
# for y in range(10,-10,-1):
# 	row = ""
# 	for x in range(-10,10):
# 		found = False
# 		count = 0
# 		for coord in coords:
# 			if int(coord[0]) == x and int(coord[1]) == y:
#
# 				found = True
# 				break
# 			count += 1
# 		if x == 0 and y == 0:
# 			row += "+"
# 		elif found:
# 			row += str(count)[0]
# 		elif x == 0:
# 			row += "|"
# 		elif y == 0:
# 			row += "-"
# 		else:
# 			row += " "
# 	print row





