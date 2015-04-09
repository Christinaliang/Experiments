__author__ = 'Matt'

import threading
from UI.drawing.TopDisplay import *
from UI.RobotData import RobotData
from Tkinter import *

test = [0]


class A(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        return

    def run(self):
        while True:
            test[0] += 1
        return


class B(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        return

    def run(self):

        root_dataBox=[RobotData()]

        root = Tk()
        app = Application(root_dataBox, master=root)
        app.after(10, app.redraw)
        app.mainloop()
        root.destroy()

        return


class Application(Frame):

    def __init__(self, dataBox, master=None):
        Frame.__init__(self, master)

        self.dataBox = dataBox

        self.canvas = Canvas(width=800, height=600)
        self.canvas.grid()

    def redraw(self):

        self.canvas.delete("all")

        # self.dataBox[0].frontLeftWheel.theta += 360

        self.dataBox[0].frontLeftWheel.theta = test[0]
        drawWheelDisplay(self.canvas, 0, 0, 200, self.dataBox[0])

        self.after(10, self.redraw)
        return

a = A()
b = B()

a.start()
b.start()
