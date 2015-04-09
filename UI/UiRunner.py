__author__ = 'Matt'


import threading
from UI.drawing.MainWindow import *
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

    def __init__(self, dataBox):
        threading.Thread.__init__(self)
        self.dataBox = dataBox

    def run(self):
        root = Tk()
        app = Application(self.dataBox, master=root)
        app.after(10, app.redraw)
        app.mainloop()
        root.destroy()
        return

