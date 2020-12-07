#This file was created by Tate Hagan
import tkinter as tk #imports the GUI framework
from tkinter import messagebox #messagebox is only imported if you explicitly state it, which is why this line is here
from tkinter import filedialog
import os #used for the isfile() method to check if a string refers to a file
from DataObject import DataObject #imports the Data Object to store data
from EmptyFileException import EmptyFileException #An exception that can be thrown by the Data Object methods called
from DataProcessor import * #imports the next component, which has its first function called when the 'Run' button is clicked
from GUIHandler import GUIHandler #For changing window back to Input GUI when the 'Back' button is clicked

class OrbitPrompt(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
    def startWindow(self, data):
        minOrbitsWidth = 30 #Cell size
        minOrbitsHeight = 5
        self.grid_columnconfigure(0, weight=1, minsize = minOrbitsWidth) #columns
        self.grid_columnconfigure(1, weight=1, minsize = minOrbitsWidth)
        self.grid_columnconfigure(2, weight=1, minsize = minOrbitsWidth)
        self.grid_columnconfigure(3, weight=1, minsize = minOrbitsWidth)
        self.grid_rowconfigure(0, weight=1, minsize = minOrbitsHeight) #rows
        self.grid_rowconfigure(1, weight=1, minsize = minOrbitsHeight)
        self.grid_rowconfigure(2, weight=1, minsize = minOrbitsHeight)
        self.grid_rowconfigure(3, weight=1, minsize = minOrbitsHeight)
        def tletooltipclicked():
            tk.messagebox.showinfo("Tle info", "Enter the absolute filepath for a tle file, either using the textbox or the browse button.\nBoth TLE and 3LE formats are accepted.")
        def tlebrowseclicked():
            filename = filedialog.askopenfilename()
            tlefile.delete(0, tk.END) #Clears existing text
            tlefile.insert(0, filename) #Inserts filename into entry
        def fitstooltipclicked():
            tk.messagebox.showinfo("Wcs info", "Enter the absolute filepath for a .fits file containing wcs information, either using the textbox or the browse button.")
        def fitsbrowseclicked():
            filename = filedialog.askopenfilename()
            fitsfile.delete(0, tk.END) #Clears existing text
            fitsfile.insert(0, filename) #Inserts filename into entry
        def goButtonClicked():
            tlefilename = tlefile.get()
            fitsfilename = fitsfile.get()
            if( (len(tlefilename) == 0) | (len(fitsfilename) == 0) ):
                tk.messagebox.showinfo("Invalid Input", "At least one input field is blank")
            else:
                if( (not os.path.isfile(tlefilename)) | (not os.path.isfile(fitsfilename)) ):
                    tk.messagebox.showinfo("Invalid File", "At least one file entered does not exist")
                elif( (not tlefilename.endswith(".txt")) | (not fitsfilename.endswith(".fits")) ):
                    tk.messagebox.showinfo("Invalid File", "Files must have correct extensions. Tle should be .txt, Wcs should be .fits")
                else:
                    try:
                        data.setTle(tlefilename) #Passes filenames and flag to Data Object constructor
                        data.setFits(fitsfilename)
                        guiHandler = GUIHandler.getInstance()
                        guiHandler.setWindow("ProcessingWindow")
                        try:
                            processData(data) #passes the data to the next component
                        except Exception as e:
                            guiHandler.setWindow("OrbitPrompt")
                            tk.messagebox.showerror("ERROR", "An unexpected error occurred.\n{}".format(e))
                    except EmptyFileException as emsg:
                        tk.messagebox.showinfo("Failure", "The files could not be read\n{}".format(emsg))
                        
        def backbuttonclicked():
            guiHandler = GUIHandler.getInstance()
            guiHandler.setWindow("InputGUI")
        tlelabel = tk.Label(master=self, text = "TLE Location:")
        tlelabel.grid(row=0, column=0)
        tletooltip = tk.Button(master=self, text="?", command=tletooltipclicked)
        tletooltip.grid(row=0, column=1)
        tlefile = tk.Entry(master=self)
        tlefile.grid(row=0, column=2)
        tlebrowse = tk.Button(master=self, text="Browse...", command=tlebrowseclicked) #Browses files
        tlebrowse.grid(row=0, column=3)
        fitslabel = tk.Label(master=self, text="WCS Location:")
        fitslabel.grid(row=1, column=0)
        fitstooltip = tk.Button(master=self, text="?", command=fitstooltipclicked)
        fitstooltip.grid(row=1, column=1)
        fitsfile = tk.Entry(master=self)
        fitsfile.grid(row=1, column=2)
        fitsbrowse=tk.Button(master=self, text="Browse...", command=fitsbrowseclicked) # Browses files
        fitsbrowse.grid(row=1, column=3)
        waitlabel = tk.Label(master=self, text="Processing Orbits information may take a few minutes.")
        waitlabel.grid(row=2, column=2)
        gobutton = tk.Button(master=self, text="Go", command=goButtonClicked) #Starts processing
        gobutton.grid(row=3, column=3)
        backbutton = tk.Button(master=self, text="Back", command=backbuttonclicked) #Goes back to input gui
        backbutton.grid(row=3, column=0)