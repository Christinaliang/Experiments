__author__ = 'Matt'

try:
    # for Python2
    from Tkinter import *
except ImportError:
    try:
        # for Python3
        from tkinter import *
    except ImportError:
        exit()

from TopDisplay import drawWheelDisplay
from RockerBogieSide import drawRockerBogie


##
# A class that does high level drawing of the screen
#
class Application(Frame):

    def __init__(self, dataBox, master=None):
        Frame.__init__(self, master)

        self.dataBox = dataBox

        self.canvas = Canvas(width=800, height=600)
        self.canvas.grid()

    def redraw(self):

        self.canvas.delete("all")
        drawWheelDisplay(self.canvas, 0, 0, 200, self.dataBox[0])

        drawRockerBogie(self.canvas, 200, 0, 200, self.dataBox[0].leftArm, True)
        drawRockerBogie(self.canvas, 200, 200, 200, self.dataBox[0].rightArm, False)

        self.after(10, self.redraw)
        return
