try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    try:
        from tkinter import *
    except ImportError:
        exit()


class MARSControlConsole(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, background="black")
        master.configure(background="black")
        try:
            # Fake the sensor table
            sampletableImage = PhotoImage(file="images/SampleTable.png")
            sensorTable = Label(image=sampletableImage)
            sensorTable.image = sampletableImage
            sensorTable.grid(row=0, column=0, rowspan=2, sticky=W, padx=5)
        except tkinter.TclError:
            ""
        try:
            # Fake the video feed
            sampleVideoImage = PhotoImage(file="images/VideoSample.png")
            videoFeed = Label(image=sampleVideoImage)
            videoFeed.image = sampleVideoImage
            videoFeed.grid(row=0, column=1, sticky=N, padx=5, pady=5)
        except tkinter.TclError:
            ""
        try:
            # Fake the controls console
            inputArea = Label(image=sampleControlAreaImage)
            inputArea.image=sampleControlAreaImage
            inputArea.grid(row=1, column=2, sticky=N+S+E+W, padx=5, pady=5)
        except tkinter.TclError:
            ""
        try:
            # Fake an arena map
            sampleLocationImage = PhotoImage(file="images/LocationSample.png")
            locationvisualizer = Label(image=sampleLocationImage)
            locationvisualizer.image = sampleLocationImage
            locationvisualizer.grid(row=0, column=2, padx=5, pady=5)
        except tkinter.TclError:
            ""
        try:
            # Fake the transport status visualizer
            SampleTransportViz = PhotoImage(file="images/TransporterStatusImage.png")
            transportVisualizer = Label(image=SampleTransportViz)
            transportVisualizer.image = SampleTransportViz
            transportVisualizer.grid(row=1, column=1, padx=5, pady=5)
        except tkinter.TclError:
            ""

root = Tk()
app = MARSControlConsole(master=root)
#TODO: Consider adding a redraw() method once things are changing
app.mainloop()
root.destroy()