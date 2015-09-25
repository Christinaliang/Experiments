#===============================================================================
# File Extraction.py
# CV image processing helper functions
# author: Jaimiey Sears
# date: Sep. 25, 2015

# NOTE: this code is derived from MATLAB code LIDAR_CSV_v8.m
# lines 193:222
#
#===============================================================================
import numpy as np
from scipy import misc

##
#extractObstacles
#Description: TODO
#
#Parameters:
#
#Return: A list of found obstacles.
##
def extractObstacles(inputThresholdMesh, circleColor):
	#do our feature extraction
	#TODO: implement erode function or find a python equivalent
	pitMatrix = erode(inputThresholdMesh)
	newRows = YMAX - YMIN
	newCols = XMAX - XMIN
	PitMatrix = scipy.misc.imresize(PitMatrix, newRows, newCols)
	
	#TODO: find a way to get rid of the non-competition area
	#equivalent to : pitMatrix = pitMatrix(1:2500, :)
	pitStats = regionProps(pitMatrix, properties=['Area', 'Centroid', 'MajorAxisLength', 'MinorAxisLength', 'Orientation','EquivDiameter']);
	
	for s in pitStats:
		#draw circles...
		#TODO: do this for ease of testing only. low priority
	return pitStats
	
