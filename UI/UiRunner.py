__author__ = 'Matt'


import threading
# from UI.ManualControl import drawDriveControl, handleDriveClick
from ManualControl import DriveControl
try:
    # for Python2
    from Tkinter import *
except ImportError:
    try:
        # for Python3
        from tkinter import *
    except ImportError:
        exit()


##
# A simple class that starts tkinter in its own thread
#
class UiRunner(threading.Thread):

    WIDTH = 800
    HEIGHT = 800

    def __init__(self, dataBox, uiData, dataClient):
        threading.Thread.__init__(self)
        self.dataBox = dataBox
        self.uiData = uiData
        self.dataClient = dataClient

        self.root = Tk()
        self.app = Frame(master=self.root, width=self.WIDTH, height=self.HEIGHT)
        self.canvas = Canvas(self.app, width=self.WIDTH, height=self.HEIGHT)

        self.canvas.bind("<Button-1>", self.onMousePress)
        self.canvas.bind("<B1-Motion>", self.onMouseMotion)
        self.canvas.bind("<ButtonRelease-1>", self.onMouseRelease)
        self.app.after(10, self.draw)
        self.canvas.pack()
        self.app.pack()

        self.canvasElements = []
        self.canvasElements.append(
            DriveControl(0, 0, 800, self.uiData, self.dataClient)
        )

    def run(self):
        # app = Application(self.dataBox, self.uiData, master=root, width=1000, height=1000)

        self.app.mainloop()
        self.root.destroy()
        return

    def onMousePress(self, event):
        for c in self.canvasElements:
            if None != c.onMousePress:
                # noinspection PyChainedComparisons
                if event.x > c.x and event.x < c.x+c.size and event.y > c.y and event.y < c.y+c.size:
                    c.onMousePress(event)
                    return
        return

    def onMouseMotion(self, event):
        for c in self.canvasElements:
            if None != c.onMouseMotion:
                # noinspection PyChainedComparisons
                if event.x > c.x and event.x < c.x+c.size and event.y > c.y and event.y < c.y+c.size:
                    c.onMouseMotion(event)
                    return
        return

    def onMouseRelease(self, event):
        for c in self.canvasElements:
            if None != c.onMouseRelease:
                # noinspection PyChainedComparisons
                if event.x > c.x and event.x < c.x+c.size and event.y > c.y and event.y < c.y+c.size:
                    c.onMouseRelease(event)
                    return
        return

    def draw(self):

        self.canvas.delete("all")

        for c in self.canvasElements:
            c.draw(self.canvas)

        self.app.after(10, self.draw)
        return


class CanvasElement:

    def __init__(self, x, y, size, drawFunc, onMousePress=None, onMouseMotion=None, onMouseRelease=None):

        self.x = x
        self.y = y
        self.size = size

        self.drawFunc = drawFunc
        self.onMousePress = onMousePress
        self.onMouseMotion = onMouseMotion
        self.onMouseRelease = onMouseRelease

        return

    def draw(self, canvas):
        self.drawFunc(canvas, self.x, self.y, self.size)

    def onClick(self, event):
        return