_author__="Taylor Stadeli"
__copyright__="January 21, 2016"
__version__= 0.5

from utility import *


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
            popIndex = pop[i]
            x.pop(popIndex - count)
            y.pop(popIndex - count)
            z.pop(popIndex - count)
            count+=1


        exceldata = [[],[],[],[],[],[],[],[],[]]

        exceldata[0] = underX
        exceldata[1] = underY
        exceldata[2] = underZ
        exceldata[3] = overX
        exceldata[4] = overY
        exceldata[5] = overZ
        exceldata[6] = x
        exceldata[7] = y
        exceldata[8] = z

        return exceldata






