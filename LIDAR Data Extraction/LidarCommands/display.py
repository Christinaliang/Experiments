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

        # new lists to contain the data points that are the peaks
        overX = []
        overY = []
        overZ = []

    # new lists to contain the data points that are the valleys
        underX = []
        underY = []
        underZ = []

    # list to keep track of all the data that needs to be removed from the original list (the peaks and valleys)
        pop = []

        # set the ground to what the lidar is looking at the very last scan
        ground = z[len(z)-361]
        print(ground)
        for i in range (0, len(z)-1):
        #Loop through the z values and find which ones are under the ground
            # if the value is under add the data point to the under lists
            if z[i] <= ground-25:
                newX = [x[i]]
                newY = [y[i]]
                newZ = [z[i]]

                underX = underX + newX
                underY = underY + newY
                underZ = underZ + newZ

                newPop = [i]
                pop = pop + newPop


            #if the value is over add the data point to the over lists
            elif z[i] >= ground+25:
                newX = [x[i]]
                newY = [y[i]]
                newZ = [z[i]]

                overX = overX + newX
                overY = overY + newY
                overZ = overZ + newZ

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

    #winSize = 1500
    plt.scatter(x,y,c='r')
   # plt.xlim(-1*winSize,winSize)
    #plt.ylim(-1*winSize,winSize)

    plt.scatter(y,z, c= 'b')
    #plt.xlim(-1*winSize,winSize)
    #plt.ylim(-1*winSize,winSize)

    plt.scatter(x,z,c= 'g')
   # plt.xlim(-1*winSize,winSize)
   # plt.ylim(-1*winSize,winSize)

    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1*winSize,winSize)
    ax.set_ylim(-1*winSize,winSize)
    ax.set_zlim(-1*winSize,winSize)

    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')
    ax.set_zlabel('zlabel')
    ax.scatter(x,y,z,c='b')



    plt.show()




##
# plotFilter
#
# Description: 3D plot the points that have been filtered
#
# Parameters:
#   x,y,z - data points received from lidar after processing and filtering
##
def plotFilter(underX, underY, underZ, overX, overY, overZ, x, y, z):

    winSize = 10000
    plt.scatter(underX,underY,color='r')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(0,winSize)

    plt.scatter(overX,overY, color='g')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(0,winSize)

    plt.scatter(x,y,color ='b')
    plt.xlim(-1*winSize,winSize)
    plt.ylim(0,winSize)

    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.set_xlim(-1*winSize,winSize)
    #ax.set_ylim(-1*winSize,winSize)
    #ax.set_zlim(-1*winSize,winSize)

    #ax.set_xlabel('xlabel')
    #ax.set_ylabel('ylabel')
    #ax.set_zlabel('zlabel')

    #ax.scatter(x,y,z,c='b')
    #ax.scatter(overX,overY,overZ,c='r')
    #ax.scatter(underX,underY,underZ,c='g')




    plt.show()
