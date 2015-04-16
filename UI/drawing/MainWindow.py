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
from UI.ManualControl import drawManualControl, handleDriveClick


##
# A class that does high level drawing of the screen
#
class Application(Frame):

    def __init__(self, dataBox, uiData, master=None, width=1000, height=1000):
        Frame.__init__(self, master=master, width=width, height=height)

        self.dataBox = dataBox
        self.uiData = uiData

        self.canvas = Canvas(width=width, height=height)
        self.canvas.grid()

        self.canvasElements = []
        self.canvasElements.append(
            CanvasElement(400, 0, 200,
                          lambda c, x, y, s: drawManualControl(c, x, y, s, self.uiData),
                          lambda event, x, y, s: handleDriveClick(event, x, y, s, self.uiData)
              )
        )

    def onClick(self, event):

        print event.x

        for c in self.canvasElements:
            if None != c.onClickFunc:
                # noinspection PyChainedComparisons
                if event.x > c.x and event.x < c.x+c.size and event.y > c.y and event.y < c.y+c.size:
                    c.onClickFunc(event)
                    return
        return

    def redraw(self):

        self.canvas.delete("all")




        drawWheelDisplay(self.canvas, 0, 0, 200, self.dataBox[0])

        drawRockerBogie(self.canvas, 200, 0, 200, self.dataBox[0].leftArm, True)
        drawRockerBogie(self.canvas, 200, 200, 200, self.dataBox[0].rightArm, False)



        for c in self.canvasElements:
            c.draw(self.canvas)

        # drawManualControl(self.canvas, 400, 000, 200, self.uiData)

        self.after(10, self.redraw)
        return


class CanvasElement:

    def __init__(self, x, y, size, drawFunc, onClickFunc=None):

        self.x = x
        self.y = y
        self.size = size

        self.drawFunc = drawFunc
        self.onClickFunc = onClickFunc

        return

    def draw(self, canvas):
        self.drawFunc(canvas, self.x, self.y, self.size)

    def onClick(self, event):
        return

