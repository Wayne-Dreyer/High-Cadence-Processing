from Output_GUI import *
#from Photometry_GUI import *
from tempDataOutput import *
from tempDataObject import *
from GUIHandler import GUIHandler
from RootGUI import RootGUI
import Output_GUI

figure = getPlot()

dataObject = tempDataObject()

dataString = "This is a test string\n With more\nthan\n one line."
#dataString = None

root = tk.Tk()

container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)
frames = {}
F = OutputGUI
page_name = F.__name__
frame = F(parent=container)
frames[page_name] = frame
frame.grid(row=0, column=0, sticky="nsew")
showframe = frames[page_name]
showframe.tkraise()

self = None

F.outputGUI(self, figure, dataObject, dataString)

root.mainloop()
