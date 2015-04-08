try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
from drawing.TopDisplay import drawWheelDisplay
from data import *


class Application(Frame):

    d = data()

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.canvas = Canvas(width=800, height=600)
        self.canvas.grid()


    def redraw(self):

        self.canvas.delete("all")

        self.d.frontLeftWheel.theta += 0.1

        drawWheelDisplay(self.canvas, 0, 0, 200, self.d)

        self.after(10, self.redraw)
        return

root = Tk()
app = Application(master=root)
app.after(10, app.redraw)
app.mainloop()
root.destroy()