from Photometry_GUI import *
from tempDataOutput import *
from tempDataObject import *
from GUIHandler import GUIHandler
from RootGUI import RootGUI
import Photometry_GUI

figure = getPlot()

dataObject = tempDataObject()

root = tk.Tk()

container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)
frames = {}
F = PhotometryGUI
page_name = F.__name__
frame = F(parent=container)
frames[page_name] = frame
frame.grid(row=0, column=0, sticky="nsew")
showframe = frames[page_name]
showframe.tkraise()

self = None

F.photoGUI(self, figure, dataObject)

root.mainloop()
