#This file was created by Tate Hagan
import tkinter as tk
from SingletonInstanceException import SingletonInstanceException #Error to be thrown when attempting to create another instance of a singleton
from IncorrectTypeException import IncorrectTypeException #Error to be thrown when setRoot is given invalid input
from InvalidWindowException import InvalidWindowException #Error to be thrown when setWindow is given invalid input
from NoRootException import NoRootException #Error to be thrown when a function requires the root, but it has not been set

class GUIHandler:
    __instance__ = None
    
    def __init__(self): #Singleton constructor. Throwing the error ensures only one instance is created
        if( not (GUIHandler.__instance__ is None)):
            raise SingletonInstanceException("Multiple GUIHandlers not allowed")
        
        self.root = None #This field is used to store the root GUI window. Initially, it is None, as we have to receive the value as input via the setRoot method
        self.locked = False #This field will be used to ensure the program waits for the Photometry GUI. Initially, it is set to False, as we are not in the Photometry GUI
    
    @staticmethod
    def getInstance(): #The singleton get instance method
        if(GUIHandler.__instance__ is None):
            GUIHandler.__instance__ = GUIHandler()
        return GUIHandler.__instance__
    
    def setRoot(self, inRoot): #Provides this object with access to the root GUI.
        if(not isinstance(inRoot, tk.Tk)):
            raise IncorrectTypeException("Root must be of type RootGUI")
        self.root = inRoot
    
    def setWindow(self, inWindow): #Changes the window to the given input
        if( (not (inWindow == "InputGUI")) and (not (inWindow == "PhotometryGUI")) and (not (inWindow == "OutputGUI")) and (not (inWindow == "LimitResourcesWin")) and (not(inWindow == "CheckPixelsPrompt")) and (not (inWindow == "ZoomedPrompt")) and (not (inWindow == "OrbitPrompt")) and (not (inWindow == "ProcessingWindow")) ):
            raise InvalidWindowException("Window must be either \"InputGUI\", \"PhotometryGUI\" or \"OutputGUI\"")
        if(self.root is None):
            raise NoRootException("Root has not been set or has been closed")
        self.root.show_frame(inWindow)
        
    def closeRoot(self): #Closes the root window
        if(not (self.root is None)): #We do not throw an error if root wasn't set, because this function is supposed to quit root anyway
            self.root.quit()
            self.root = None
        
    def setPhotometryGUIData(self, fig, dataObject): #Passes data to the Photometry GUI via the RootGUI
        if(self.root is None):
            raise NoRootException("Root has not been set or has been closed")
        self.root.setPhotometryGUIData(fig, dataObject)
        
    def setOutputGUIData(self, fig, dataObject, outputString): #Passes data to the Output GUI via the RootGUI
        if(self.root is None):
            raise NoRootException("Root has not been set or has been closed")
        self.root.setOutputGUIData(fig, dataObject, outputString)
    
    def setMultipleOutputGUIData(self, figs, dataObject, outputString):
        if(self.root is None):
            raise NoRootException("Root has not been set or has been closed")
        self.root.setMultipleOutputGUIData(figs, dataObject, outputString)
    
    def setCheckPixelsPromptData(self, data):
        if(self.root is None):
            raise NoRootException("Root has not been set or has been closed")
        self.root.setCheckPixelsPromptData(data)
    
    def setZoomedPromptData(self, data):
        if(self.root is None):
            raise NoRootException("Root has not been set or has been closed")
        self.root.setZoomedPromptData(data)
    
    def setOrbitPromptData(self, data):
        if(self.root is None):
            raise NoRootException("Root has not been set or has been closed")
        self.root.setOrbitPromptData(data)
    
    def lock(self): #Sets the locked field to true. Used by Photometry to ensure the program waits for the Photometry GUI
        self.locked = True
    
    def unlock(self): #Sets the locked field to false. Used by the Photometry GUI when it exits to allow the program to continue
        self.locked = False
    
    def getLock(self): #Retrieves the locked field. Used by Photometry to loop while the value is true
        return self.locked