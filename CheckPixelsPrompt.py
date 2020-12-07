#This file was created by Tate Hagan
import tkinter as tk #imports the GUI framework
from tkinter import messagebox #messagebox is only imported if you explicitly state it, which is why this line is here
from DataObject import DataObject #imports the Data Object to store data
from InvalidCoordException import InvalidCoordException
from InvalidZoomFactorException import InvalidZoomFactorException
from DataProcessor import * #imports the next component, which has its first function called when the 'Run' button is clicked
from GUIHandler import GUIHandler #For changing window back to Input GUI when the 'Back' button is clicked

class CheckPixelsPrompt(tk.Frame):
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
        self.grid_rowconfigure(2, weight=1, minsize = minCoordHeight)
        self.grid_rowconfigure(3, weight=1, minsize = minCoordHeight)
        
        #event handlers
        def xcoordtooltipclicked():
            tk.messagebox.showinfo("x info", "The x coordinate to zoom into. This will be the x coordinate of the centre of the zoomed image")
        
        def ycoordtooltipclicked():
            tk.messagebox.showinfo("y info", "The y coordinate to zoom into. This will be the y coordinate of the centre of the zoomed image")
        
        def zoomfactortooltipclicked():
            tk.messagebox.showinfo("Zoom Factor info", "The magnification factor for the zoom. For example, entering '2' will cause a 2x magnification")
        
        def confirmCoords():
            try:
                xVal = int(xCoord.get())
                yVal = int(yCoord.get())
                zoomVal = float(zoomFactor.get())
                if( (xVal > 0) and (yVal > 0) and (zoomVal > 0.0)):
                    try:
                        data.setCheckX(xVal) #Passes input to Data Object
                        data.setCheckY(yVal)
                        data.setCheckFactor(zoomVal)
                        
                        guiHandler = GUIHandler.getInstance()
                        guiHandler.setWindow("ProcessingWindow")
                        try:
                            processData(data) #passes the data to the next component
                        except Exception as e:
                            guiHandler.setWindow("CheckPixelsPrompt")
                            tk.messagebox.showerror("ERROR", "An unexpected error occurred.\n{}".format(e))
                    except InvalidCoordException as ex1:
                        tk.messagebox.showinfo("Invalid Inputs", ex1)
                    except InvalidZoomFactorException as ex2:
                        tk.messagebox.showinfo("Invalid Inputs", ex2)
                else:
                    tk.messagebox.showinfo("Invalid Inputs", "Coordinates and zoom factor must be greater than 0")
            except ValueError:
                tk.messagebox.showinfo("Invalid Inputs", "Coordinates must be integers, Zoom Factor must be a real number")
        
        def backbuttonclicked():
            guiHandler = GUIHandler.getInstance()
            guiHandler.setWindow("InputGUI")
        
        #widgets
        xCoordLabel = tk.Label(master=self, text = "x")
        xCoordLabel.grid(row=0, column=0)
        xCoordTooltip = tk.Button(master=self, text="?", command=xcoordtooltipclicked)
        xCoordTooltip.grid(row=0, column=1)
        xCoord = tk.Entry(master=self)
        xCoord.grid(row=0, column=2)
        yCoordLabel = tk.Label(master=self, text="y")
        yCoordLabel.grid(row=1, column = 0)
        yCoordTooltip = tk.Button(master=self, text="?", command=ycoordtooltipclicked)
        yCoordTooltip.grid(row=1, column=1)
        yCoord = tk.Entry(master=self)
        yCoord.grid(row=1, column=2)
        zoomFactorLabel = tk.Label(master=self, text="Zoom Factor")
        zoomFactorLabel.grid(row=2, column=0)
        zoomFactorTooltip = tk.Button(master=self, text="?", command=zoomfactortooltipclicked)
        zoomFactorTooltip.grid(row=2, column=1)
        zoomFactor = tk.Entry(master=self)
        zoomFactor.grid(row=2, column=2)
        confirmButton = tk.Button(master=self, text="Confirm", command=confirmCoords) #Confirms input and starts processing
        confirmButton.grid(row=3, column=2)
        backbutton = tk.Button(master=self, text="Back", command=backbuttonclicked) #Goes back to input gui
        backbutton.grid(row=3, column=0)