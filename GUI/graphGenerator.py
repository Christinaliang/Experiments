__author__ = 'sherryliao_1'

import numpy
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

##
# Graph
#
# Creates a constant time graph
#
# adapted from http://hardsoftlucid.wordpress.com/various-stuff/realtime-plotting/
#
##


class Graph(object):
    def __init__(self, title, xLabel, yLabel, yMin, yMax, root):
        # configure graph details
        self.xAchse = numpy.arange(0, 100, 1)
        self.yAchse = numpy.array([0]*100)
        self.yMin = yMin
        self.yMax = yMax
        self.fig = matplotlib.figure.Figure((3,3))
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True)
        self.ax.set_title(title)
        self.ax.set_xlabel(xLabel)
        self.ax.set_ylabel(yLabel)
        self.line1 = self.ax.plot(self.xAchse, self.yAchse, '-')

        # configure values for graph to display
        self.values = [0 for x in range(100)]

        # configure parent object and canvas
        self.parent = root
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)

        # bind event listener for updating data                TODO: needs to listen to data from arduino
        self.fig.canvas.mpl_connect('key_press_event', self.dataInputHandler)

    # listens to input from keyboard and adds input value to array for plotting
    def dataInputHandler(self, event):
        if event.key in ['0','1','2','3','4','5','6','7','8','9']:
            self.values.append(event.key)

    # keeps data moving at constant time, fills in "0" for input if no new data is available
    def inputGenerator(self):
        self.values.append(0)
        self.parent.after(50, self.inputGenerator)

    # plot the values to graph
    def realTimePlotter(self):
        numVisibleDataPoints = min(len(self.values), 1000)
        currentXAxis = numpy.arange(len(self.values) - numVisibleDataPoints, len(self.values), 1)

        self.line1[0].set_data(currentXAxis, numpy.array(self.values[-numVisibleDataPoints:]))
        self.ax.axis([currentXAxis.min(), currentXAxis.max(), self.yMin, self.yMax])
        self.canvas.draw()
        self.parent.after(50, self.realTimePlotter)