_author__="Taylor Stadeli, Lysa Pinto"
__copyright__="January 21, 2016"
__version__= 0.5

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D

##
# filter
#
# Description: filters data to locate pits and craters
#
# Parameters:
#   x,y,z - data points received from lidar after processing
##
def filterscans(x, y, z):

#loop through and find the median z height
        total = 0
        for i in range (0, len(z) -1):

            total = z[i] + total

        medianval = total/(len(z)-1)
        # the crater value will be categorized as the median +10
        overval  = medianval + 10
        # the pit value will be categorized as the median -10
        underval = medianval - 10



        overX = []
        overY = []
        overZ = []
        underX = []
        underY = []
        underZ = []
        pop = []


        #Loop through the z values and find which ones are over and under the median
        for i in range(0, len(z) -1):
            # if the value is under add the data point to the under lists
            if z[i] <= underval:
                newX = [x[i]]
                newY = [y[i]]
                newZ = [z[i]]

                underX =  underX + newX
                underY =  underY + newY
                underZ =  underZ + newZ



            #if the value is over add the data point to the over lists
            elif z[i] >= overval:
                newX = [x[i]]
                newY = [y[i]]
                newZ = [z[i]]

                overX =  overX + newX
                overY =  overY + newY
                overZ =  overZ + newZ

            #keep track of which data points to pop after the loop is finished
            else:

                newPop = [i]
                pop = pop + newPop

        # want to plot original points before removing any data
        #plot(x,y,z)

        # remove the data points that are in the over and under lists
        count = 0
        for i in range(0, len(pop) - 1):
            popIndex = pop[i - count]
            x.pop(popIndex)
            y.pop(popIndex)
            z.pop(popIndex)
            count+=1


        plotFilter(underX, underY, underZ, overX, overY,overZ, x, y, z)


##
# plot
#
# Description: 3D plot the points that have not yet been filtered
#
# Parameters:
#   x,y,z - data points received from lidar after processing
##
def plot(x,y,z):

    winSize = 1500
    plt.scatter(x,y,c='r')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(-1*winSize,winSize)

    plt.scatter(y,z, c= 'b')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(-1*winSize,winSize)

    plt.scatter(x,z,c= 'g')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(-1*winSize,winSize)

    fig = plt.figure()
   # print len(x)
    ax = fig.add_subplot(111)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1*winSize,winSize)
    ax.set_ylim(-1*winSize,winSize)
    ax.set_zlim(-1*winSize,winSize)
   # zArray = []
    #to see what order the data points are recived, lowest height is first
    #for i in range(0,len(lt.processedDataArrays[0])):
        #zArray.append(i)
    ax.scatter(x,y,z,c=z)





#commandFile = open("lidar_commands.txt",'w')
#commandFile.write("{}".format(lt.commandOutput))
#commandFile.close()

#commandFile = open("lidar_data.txt",'w')
#commandFile.write("{}".format(lt.dataOutput))
#commandFile.close()

    plt.show()




##
# plotFilter
#
# Description: 3D plot the points that have been filtered
#
# Parameters:
#   x,y,z - data points received from lidar after processing and filtering
##
def plotFilter(overX, overY, overZ, underX, underY, underZ, x, y, z):

    winSize = 1500
    #plt.scatter(x,y,c='r')
    #plt.xlim(-1*winSize,winSize)
    #plt.ylim(-1*winSize,winSize)

    #plt.scatter(y,z, c= 'b')
    #plt.xlim(-1*winSize,winSize)
    #plt.ylim(-1*winSize,winSize)

    #plt.scatter(x,z,c= 'g')
    #plt.xlim(-1*winSize,winSize)
    #plt.ylim(-1*winSize,winSize)


    fig = plt.figure()
    #print len(x)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1*winSize,winSize)
    ax.set_ylim(-1*winSize,winSize)
    ax.set_zlim(-1*winSize,winSize)
    zArray = []
    #to see what order the data points are recived, lowest height is first
    #for i in range(0,len(lt.processedDataArrays[0])):
        #zArray.append(i)
    ax.scatter(x,y,z,c='b')
    ax.scatter(overX,overY,overZ,c='g')
    ax.scatter(underX,underY,underZ,c='r')




    plt.show()