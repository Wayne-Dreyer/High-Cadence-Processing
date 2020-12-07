import tkinter as tk
from FOB import *

class tempDataObject:
    def __init__(self):
        self.selectedWindow = None

    def changeSelectedGUI(self, newGUI):
        if(not isinstance(newGUI, tk.Tk)):
            raise IncorrectTypeException
        if(self.selectedWindow != None):
            self.selectedWindow.destroy()
        self.selectedWindow = newGUI
