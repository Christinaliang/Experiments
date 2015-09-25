#===============================================================================
# File LIDAR_CV.py
# LiDAR computer vision image processing
# python pseudocode pass no.1
# author: Jaimiey Sears
# date: Sep. 25, 2015

# NOTE: this code is derived from MATLAB code LIDAR_CSV_v8.m
# lines 116:END
#
#===============================================================================

#numpy allows us to perform scientific computing
import numpy as np
#scipy introduces some image change functions from MATLAB
from scipy import misc
from scipy import ndimage

#resolution of the mesh we want to create
MESH_RESOLUTION = 500

#TODO: we may not need this section
#			VVV
#Hard-coded values to try and focus on the arena surface and not the walls.
#Ian: X(-2750,2000),Y(2000,6000)
#FieldOnly: X(-1500,1500),Y(2000,5500)
#			^^^

XMIN = -1300
XMAX = 1500
YMIN = 2000
YMAX = 5500

#linspace returns an array
xlin = np.linspace(XMIN,XMAX,MESH_RESOLUTION)
ylin = np.linspace(YMIN,YMAX,MESH_RESOLUTION)

mesh = np.meshgrid(xlin, ylin)
#f is a 3-D scatterPlot (?) of our data
f = scatteredInterpolant(Xabs.T, Yabs.T, Zabs.T) # << THIS IS ???? (see ComputerVisionFinalPaper-1.pdf)
#we want to transpose this info into a single mesh.
#Zmesh = f(Xmesh, Zmesh)

#TODO: some GUI display computing. not highest priority
#display as a 3-D mesh
#figure(1);
#mesh(Xmesh,Ymesh,Zmesh);
#xlabel('X');
#ylabel('Y');
#zlabel('Z');

#a 2x2 max filter is applied then the result is displayed in figure (2)
# ZmeshFiltered = ordfilt2(Zmesh,4,ones(2,2));
# figure(2);
# xlabel('X');
# ylabel('Y');
# zlabel('Z');
# title('2D box maximum filter');
# mesh(Xmesh,Ymesh,ZmeshFiltered);
## view([0 -90]);

#average value is 2266, although the walls mess with this quite a bit.
# median is roughly 2170 for the test data.
medianValue = median(median(ZmeshFiltered(:)));

#low pass: 2170 - detection level (mm)
#TODO: replace hard-coding with either constants or sliding threshold filter
low_pass_offset = 230
LOW_PASS_THRESHOLD = medianValue-low_pass_offset

#high pass: 2170 + detection level (mm).
high_pass_offset = 70;
HIGH_PASS_THRESHOLD = medianValue+high_pass_offset;

#apply thresholds to the zmesh
ZmeshThresholdedLOW = ZmeshFiltered < LOW_PASS_THRESHOLD;
ZmeshThresholdedHIGH = (ZmeshFiltered > HIGH_PASS_THRESHOLD);
ZmeshThresholded = (ZmeshThresholdedLOW *(-1000)) + (ZmeshThresholdedHIGH * (1000));

#get some.
extractObstacles(ZmeshThresholdedLOW, 'b');
extractObstacles(ZmeshThresholdedHIGH, 'r');
#Zmesh is put through a basic threshold filter to extract elements of different heights
#then ZmeshThresholded is displayed

#next, the object exctraction function is defined
#EDIT: moved to Extraction.py
	
#the other two functions are UI update functions and will not be used,
#although breaking this code up into subroutines may not be a bad idea



