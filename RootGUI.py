#This file was created by Tate Hagan

import tkinter as tk #Imports the GUI framework
from GUIHandler import GUIHandler #Imports the Singleton for GUI Switching

#Imports GUIs
from InputGUI import InputGUI #For running prototype
#from InputGUISoloDebug import InputGUI #For testing Input GUI Component
#from InputGUINoErrCatch import InputGUI #For testing prototype
hasResource = True
try:
    import resource as resource #used for limiting use of computer resources
except ImportError:
    hasResource = False
if(hasResource):
    from LimitResourcesWin import LimitResourcesWin
from CheckPixelsPrompt import CheckPixelsPrompt
from ZoomedPrompt import ZoomedPrompt
from OrbitPrompt import OrbitPrompt
from ProcessingWindow import ProcessingWindow
from Photometry_GUI import PhotometryGUI
from Output_GUI import OutputGUI

class RootGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("High Cadence Optical Transient Searches using Drift Scan Images") #Sets the window title
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Create the GUI Handler to allow for window switching
        guiHandler = GUIHandler.getInstance()
        guiHandler.setRoot(self)
    
        self.frames = {}
        for F in (InputGUI, CheckPixelsPrompt, ZoomedPrompt, OrbitPrompt, ProcessingWindow, PhotometryGUI, OutputGUI):
            page_name = F.__name__
            frame = F(parent=container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        if(hasResource):
            F = LimitResourcesWin
            page_name = F.__name__
            frame = F(parent=container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        guiHandler.setWindow("InputGUI")
        
    def show_frame(self, page_name):
        for F in self.frames.values():
            F.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
    
    def setPhotometryGUIData(self, fig, dataObject):
        frame = self.frames["PhotometryGUI"]
        frame.photoGUI(fig, dataObject)
        
    def setOutputGUIData(self, fig, dataObject, outputString):
        frame = self.frames["OutputGUI"]
        frame.outputGUI(fig, dataObject, outputString)
        
    def setMultipleOutputGUIData(self, figs, dataObject, outputString):
        frame = self.frames["OutputGUI"]
        frame.multipleOutputGUI(figs, dataObject, outputString)
        
    def setCheckPixelsPromptData(self, data):
        frame = self.frames["CheckPixelsPrompt"]
        frame.startWindow(data)
    
    def setZoomedPromptData(self, data):
        frame = self.frames["ZoomedPrompt"]
        frame.startWindow(data)
        
    def setOrbitPromptData(self, data):
        frame = self.frames["OrbitPrompt"]
        frame.startWindow(data)