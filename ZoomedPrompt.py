#This file was created by Tate Hagan
import tkinter as tk #imports the GUI framework
from tkinter import messagebox #messagebox is only imported if you explicitly state it, which is why this line is here
from DataObject import DataObject #imports the Data Object to store data
from InvalidCoordException import InvalidCoordException
from InvalidZoomFactorException import InvalidZoomFactorException
from DataProcessor import * #imports the next component, which has its first function called when the 'Run' button is clicked
from GUIHandler import GUIHandler #For changing window back to Input GUI when the 'Back' button is clicked

class ZoomedPrompt(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
    def startWindow(self, data):
        #grid setup
        minCoordWidth = 30 #Cell size
        minCoordHeight = 5
        self.grid_columnconfigure(0, weight=1, minsize = minCoordWidth) #columns
        self.grid_columnconfigure(1, weight=1, minsize = minCoordWidth)
        self.grid_columnconfigure(2, weight=1, minsize = minCoordWidth)
        self.grid_rowconfigure(0, weight=1, minsize = minCoordHeight) #rows
        self.grid_rowconfigure(1, weight=1, minsize = minCoordHeight)
        
        #event handlers
        def zoomfactortooltipclicked():
            tk.messagebox.showinfo("Zoom Factor info", "The magnification factor for the zoom. For example, entering '2' will cause a 2x magnification")
        
        def confirmCoords():
            try:
                zoomVal = float(zoomFactor.get())
                if(zoomVal > 0.0):
                    try:
                        data.setZoomFactor(zoomVal)
                        
                        guiHandler = GUIHandler.getInstance()
                        guiHandler.setWindow("ProcessingWindow")
                        try:
                            processData(data) #passes the data to the next component
                        except Exception as e:
                            guiHandler.setWindow("ZoomedPrompt")
                            tk.messagebox.showerror("ERROR", "An unexpected error occurred.\n{}".format(e))
                    except InvalidZoomFactorException as ex1:
                        tk.messagebox.showinfo("Invalid Input", ex1)
                else:
                    tk.messagebox.showinfo("Invalid Inputs", "Coordinates and zoom factor must be greater than 0")
            except ValueError:
                tk.messagebox.showinfo("Invalid Inputs", "Coordinates must be integers, Zoom Factor must be a real number")
        
        def backbuttonclicked():
            guiHandler = GUIHandler.getInstance()
            guiHandler.setWindow("InputGUI")
        
        #widgets
        zoomFactorLabel = tk.Label(master=self, text="Zoom Factor")
        zoomFactorLabel.grid(row=0, column=0)
        zoomFactorTooltip = tk.Button(master=self, text="?", command=zoomfactortooltipclicked)
        zoomFactorTooltip.grid(row=0, column=1)
        zoomFactor = tk.Entry(master=self)
        zoomFactor.grid(row=0, column=2)
        confirmButton = tk.Button(master=self, text="Confirm", command=confirmCoords) #Confirms input and starts processing
        confirmButton.grid(row=1, column=2)
        backbutton = tk.Button(master=self, text="Back", command=backbuttonclicked) #Goes back to input gui
        backbutton.grid(row=1, column=0)