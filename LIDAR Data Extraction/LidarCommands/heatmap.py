#===============================================================================
# heatmap.py
# heatmap generator given, x, y, and intensity data
# author: Taylor Stadeli
# date: Oct. 22, 2015
#
#===============================================================================
import matplotlib.pyplot as plt
import numpy as np
import random
import pickle

with open('test_vectors_2018_2_5_19_3_59.dat', 'rb') as f:
    dataArrays = pickle().load(f)



x = dataArrays[0]
y = dataArrays[1]
z = dataArrays[2]


##generate some random data
#x = []
#y = []
#z = []
#intensity = []
#for i in range (0, 2000):
#    x.append(i)
#for i in range (0, 2000):
#    y.append(i)
#for j in range(0,2000):
#    z = []
#    for i in range (0, 2000):
#        z.append(random.randint(1, 100))
#    intensity.append(z)


#setup the 2D grid with Numpy
x, y = np.meshgrid(x, y)

#convert intensity (list of lists) to a numpy array for plotting
intensity = np.array(intensity)

#plug the data into pcolormesh,
plt.pcolormesh(x, y, intensity)
plt.colorbar() #need a colorbar to show the intensity scale
plt.show() 
