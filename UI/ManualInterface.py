try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *


class MARSControlConsole(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, background="black")
        master.configure(background="black")
        # Fake the sensor table
        sampletableImage = PhotoImage(file="images/SampleTable.png")
        sensorTable = Label(image=sampletableImage)
        sensorTable.image = sampletableImage
        sensorTable.grid(row=0, column=0, rowspan=2, sticky=W, padx=5)
        # Fake the video feed
        sampleVideoImage = PhotoImage(file="images/VideoSample.png")
        videoFeed = Label(image=sampleVideoImage)
        videoFeed.image = sampleVideoImage
        videoFeed.grid(row=0, column=1, sticky=N, padx=5, pady=5)
        # Fake the controls console
        sampleControlAreaImage = PhotoImage(file="images/ControlsConsole.png")
        inputArea = Label(image=sampleControlAreaImage)
        inputArea.image=sampleControlAreaImage
        inputArea.grid(row=1, column=2, sticky=N+S+E+W, padx=5, pady=5)
        # Fake an arena map
        sampleLocationImage = PhotoImage(file="images/LocationSample.png")
        locationvisualizer = Label(image=sampleLocationImage)
        locationvisualizer.image = sampleLocationImage
        locationvisualizer.grid(row=0, column=2, padx=5, pady=5)
        # Fake the transport status visualizer
        SampleTransportViz = PhotoImage(file="images/TransporterStatusImage.png")
        transportVisualizer = Label(image=SampleTransportViz)
        transportVisualizer.image = SampleTransportViz
        transportVisualizer.grid(row=1, column=1, padx=5, pady=5)

root = Tk()
app = MARSControlConsole(master=root)
#TODO: Consider adding a redraw() method once things are changing
app.mainloop()
root.destroy()