__author__ = 'sherryliao_1'


from Tkinter import *
from PIL import ImageTk, Image
import graphGenerator as gg

# initialize frame
root = Tk()
root.wm_title("Robotics UI")

# initialize graphs
sgGraph = gg.Graph("Strain Gauge", "Time", "Force", 0, 10, root)

# <------------------fill up GUI-------------------------->
#   _______________________________________________
#   |                  |                           |
#   | Const.Image      |     Map                   |
#   |                  |                           |
#   |__________________|___________________________|
#   |                  |                           |
#   |                  |                           |
#   |  State Machine   |    Graphs                 |
#   |                  |                           |
#   |__________________|___________________________|
#
# <------------------------------------------------------->

# add picture of what robot sees
path = '../pictureLibrary/rover.jpg'                             #TODO - this must be updated to the picture taken by cam
constantTimeImage = ImageTk.PhotoImage(Image.open(path))
label = Label(image=constantTimeImage)
label.image = constantTimeImage
label.grid(row=0, columnspan=2)

# add map of where robot thinks it is
mapPath = '../pictureLibrary/rover2.jpg'                          #TODO - this must be updated draw image from sensor data
mapImage = ImageTk.PhotoImage(Image.open(mapPath))
label2 = Label(image=mapImage)
label2.image = mapImage
label2.grid(row=0, column=2, columnspan=4, sticky=W+E+N+S)

# add state machine information
label3 = Label(root, text="State machine information")
label3.grid(row=1, column=0, columnspan=2, sticky=W+E+N+S)

# draw strain gauge graph
sgGraph.canvas.show()
sgGraph.canvas.get_tk_widget().grid(row=1, column=2, columnspan=2, sticky=W+E+N+S)

# update graphs
root.after(50, sgGraph.inputGenerator)
root.after(50, sgGraph.realTimePlotter)

mainloop()
