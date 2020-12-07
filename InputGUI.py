#This file was created by Tate Hagan
import tkinter as tk #imports the GUI framework
from tkinter import messagebox #messagebox is only imported if you explicitly state it, which is why this line is here
from tkinter import filedialog
import os #used for the isfile() method to check if a string refers to a file
import time
from astropy.io import fits #Used to view the image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#The resource package is OS dependent for UNIX systems. The error catching here is because an error will occur on Windows systems
hasResource = True
try:
    import resource as resource #used for limiting use of computer resources
except ImportError:
    hasResource = False

from DataProcessor import * #imports the next component, which has its first function called when the 'Run' button is clicked
from DataObject import DataObject #imports the Data Object to store data
from GUIHandler import GUIHandler #imports the GUIHandler to change windows
from EmptyFileException import EmptyFileException #Errors thrown by DataObject which needs to be handled
from IncorrectTypeException import IncorrectTypeException

class InputGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        #event handlers
        def runclicked():
            selectedflag = flag.get()
            if(selectedflag == ''): #Checks if a flag is selected
                tk.messagebox.showinfo("Invalid Input", "No flag selected")
            else:
                snr = snrentry.get()
                try:
                    snrno = float(snr)
                    fitfilename = fitfile.get()
                    if(len(fitfilename) == 0):
                        tk.messagebox.showinfo("Invalid Input", "Fit file entry is blank")
                    else:
                        if(not os.path.isfile(fitfilename)):
                            tk.messagebox.showinfo("Invalid File", "File entered does not exist")
                        elif(not fitfilename.endswith(".fit")):
                            tk.messagebox.showinfo("Invalid File", "Image must be .fit")
                        else:
                            try:
                                data = DataObject(fitfilename, selectedflag, snrno) #Passes filenames and flag to Data Object constructor
                                try:
                                    if(selectedflag == 'Photoplot'): #This flag requires no additional info
                                        guiHandler = GUIHandler.getInstance()
                                        guiHandler.setWindow("ProcessingWindow")
                                        processData(data) #passes the data to the next component
                                    elif(selectedflag == 'Publication'): #This flag requires no additional info
                                        guiHandler = GUIHandler.getInstance()
                                        guiHandler.setWindow("ProcessingWindow")
                                        processData(data) #passes the data to the next component
                                    elif(selectedflag == 'CheckPixels'): #We need to get coordinates and zoom factor to zoom
                                        guiHandler = GUIHandler.getInstance()
                                        guiHandler.setCheckPixelsPromptData(data)
                                        guiHandler.setWindow("CheckPixelsPrompt")
                                    elif(selectedflag == 'Simulate'):
                                        guiHandler = GUIHandler.getInstance()
                                        guiHandler.setWindow("ProcessingWindow")
                                        processData(data) #passes the data to the next component
                                    elif(selectedflag == 'Zoomed'): #We need to get the zoom factor to zoom into candidates
                                        guiHandler = GUIHandler.getInstance()
                                        guiHandler.setZoomedPromptData(data)
                                        guiHandler.setWindow("ZoomedPrompt")
                                    elif(selectedflag == 'Orbits'): #This flag requires tle and wcs information
                                        guiHandler = GUIHandler.getInstance()
                                        guiHandler.setOrbitPromptData(data)
                                        guiHandler.setWindow("OrbitPrompt")
                                except Exception as e1:
                                    tk.messagebox.showerror("Error", "An error occurred while processing the data.\n{}".format(e1))
                                    guiHandler = GUIHandler.getInstance()
                                    guiHandler.setWindow("InputGUI")
                            except EmptyFileException as efemsg:
                                tk.messagebox.showerror("Invalid Files", "The files passed are invalid. They may be corrupted or incorrectly formatted.\n{}".format(efemsg))
                            except IncorrectTypeException as itemsg:
                                tk.messagebox.showerror("Invalid Type", "An input was an invalid type.\n{}.".format(itemsg))
                            except Exception as e2:
                                tk.messagebox.showerror("Error", "An error occurred while opening the files.\n{}".format(e2))
                except ValueError:
                    tk.messagebox.showinfo("Invalid Input", "SNR must be a number.")
        
        def fittooltipclicked():
            tk.messagebox.showinfo("Image Info", "Enter a .fit file. You may type in the full path or use the browse button to find it.")
            
        def fitbrowseclicked():
            filename = filedialog.askopenfilename()
            fitfile.delete(0, tk.END) #Clears existing text
            fitfile.insert(0, filename) #Inserts filename into entry
        
        def viewimageclicked():
            try:
                fitfilename = fitfile.get()
                with fits.open(fitfilename) as imghdul: #using the with keyword means that the file will be closed even if an exception is thrown
                    image = imghdul[0].data
                figure = plt.figure()
                plt.imshow(image)

                if figure is None:
                    tk.messagebox.showerror("Error", "Figure is null")

                imageWin = tk.Toplevel()
                imageWin.wm_title("Image Viewer")
                mainCanvas = tk.Canvas(imageWin, width=1600, height=900)
                mainCanvas.pack(fill="both", expand=True)
                figCanvas = FigureCanvasTkAgg(figure, master=mainCanvas)
                figCanvas.draw()
                figCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            except ValueError:
                tk.messagebox.showerror("Error", "Img filename is empty")
            except OSError:
                tk.messagebox.showerror("Error", "Img file is not the correct format or is corrupted")
               
        def snrtooltipclicked():
            tk.messagebox.showinfo("SNR Info", "Enter a number to be used as the Signal-Noise Ratio (default value is 10)\nIncreasing this value will decrease the number of candidate detections.")
         
        def limitresourcesclicked():
            guiHandler = GUIHandler.getInstance()
            guiHandler.setWindow("LimitResourcesWin")
            
        #setup GUI elements

        #window size
        minWidth = 284
        minHeight = 124
        self.columnconfigure(0, weight = 1, minsize = minWidth)
        self.columnconfigure(1, weight = 1, minsize = minWidth)
        self.columnconfigure(2, weight = 1, minsize = minWidth)
        self.rowconfigure(0, weight = 1, minsize = minHeight)

        #create frames
        inputSelectFrame = tk.Canvas(self, width = minWidth, height = minHeight, bd = 0, highlightthickness = 2, relief = 'sunken')
        inputSelectFrame.grid(row=0, column=0, sticky="nsew")
        flagFrame = tk.Canvas(self, width = minWidth, height = minHeight, bd = 0, highlightthickness = 2, relief = 'sunken')
        flagFrame.grid(row=0, column=1, sticky="nsew")
        runFrame=tk.Canvas(self, width = minWidth, height = minHeight, bd = 0, highlightthickness = 2, relief = 'sunken')
        runFrame.grid(row=0, column=2, sticky="nsew")

        #input selection section
        #frame size
        elementMinWidth = 30
        elementMinHeight = 5
        inputSelectFrame.columnconfigure(0, weight = 1, minsize = elementMinWidth)
        inputSelectFrame.columnconfigure(1, weight = 1, minsize = elementMinWidth)
        inputSelectFrame.columnconfigure(2, weight = 1, minsize = elementMinWidth)
        inputSelectFrame.columnconfigure(3, weight = 1, minsize = elementMinWidth)
        inputSelectFrame.rowconfigure(0, weight = 1, minsize = elementMinHeight)
        inputSelectFrame.rowconfigure(1, weight = 1, minsize = elementMinHeight)
        inputSelectFrame.rowconfigure(2, weight = 1, minsize = elementMinHeight)
        inputSelectFrame.rowconfigure(3, weight = 1, minsize = elementMinHeight)
        #widgets
        fileHeading = tk.Label(master=inputSelectFrame, text = "Select inputs")
        fileHeading.grid(row=0, column=2) # heading
        fitlabel = tk.Label(master=inputSelectFrame, text="Image Location:")
        fitlabel.grid(row=1, column=0)
        fittooltip = tk.Button(master=inputSelectFrame, text="?", command=fittooltipclicked) #Displays message giving tooltip info
        fittooltip.grid(row=1, column=1)
        fitfile = tk.Entry(master=inputSelectFrame)
        fitfile.grid(row=1, column=2)
        fitbrowse = tk.Button(master=inputSelectFrame, text="Browse...", command=fitbrowseclicked) # Browses files
        fitbrowse.grid(row=1, column=3)
        snrlabel = tk.Label(master=inputSelectFrame, text="Signal-Noise Ratio:")
        snrlabel.grid(row=2, column=0)
        snrtooltip = tk.Button(master=inputSelectFrame, text="?", command=snrtooltipclicked)
        snrtooltip.grid(row=2, column=1)
        snrentry = tk.Entry(master=inputSelectFrame)
        snrentry.insert(tk.END, "10") #Sets default SNR to 10
        snrentry.grid(row=2, column=2)
        viewImageButton = tk.Button(master=inputSelectFrame, text="View Image", command=viewimageclicked) #Views given image
        viewImageButton.grid(row=3, column=2)

        #flag selection section
        #inner frames to separate header from flags
        flagHeadingFrame=tk.Frame(master=flagFrame)
        flagHeadingFrame.pack(fill = tk.BOTH)
        flagSelectFrame=tk.Frame(master=flagFrame)
        flagSelectFrame.pack(fill = tk.BOTH)

        checkheading = tk.Label(master=flagHeadingFrame, text = "Select Tests to Run") #heading
        checkheading.pack(fill = tk.BOTH)

        #framesize
        flagMinSize = 30
        flagMinHeight = 5
        flagSelectFrame.columnconfigure(0, weight = 1, minsize = flagMinSize)
        flagSelectFrame.columnconfigure(1, weight = 1, minsize = flagMinSize)
        flagSelectFrame.rowconfigure(0, weight = 1, minsize = flagMinHeight)
        flagSelectFrame.rowconfigure(1, weight = 1, minsize = flagMinHeight)
        flagSelectFrame.rowconfigure(2, weight = 1, minsize = flagMinHeight)
        #widgets
        flag = tk.StringVar(master=self)
        photoplot = tk.Radiobutton(master=flagSelectFrame, text='Photoplot', variable=flag, value='Photoplot')
        photoplot.grid(row=0, column=0, sticky="nsw", padx=10) #sticky causes element to align left, padx causes it to not go all the way left
        publication = tk.Radiobutton(master=flagSelectFrame, text ='Publication', variable=flag, value='Publication')
        publication.grid(row=1, column=0, sticky="nsw", padx=10)
        checkpixels = tk.Radiobutton(master=flagSelectFrame, text='Check Pixels', variable=flag, value='CheckPixels')
        checkpixels.grid(row=2, column=0, sticky="nsw", padx=10)
        simulate = tk.Radiobutton(master=flagSelectFrame, text='Simulate', variable=flag, value='Simulate')
        simulate.grid(row=0, column=1, sticky="nsw", padx=10)
        zoomed = tk.Radiobutton(master=flagSelectFrame, text='Create Zoomed Image', variable=flag, value='Zoomed')
        zoomed.grid(row=1, column=1, sticky="nsw", padx=10)
        orbit = tk.Radiobutton(master=flagSelectFrame, text='Orbiting Objects', variable=flag, value='Orbits')
        orbit.grid(row=2, column=1, sticky="nsw", padx=10)
        flag.set('Photoplot') #Sets the initial radiobutton selection

        #Run section
        runButton = tk.Button(master=runFrame, text="Run", command=runclicked) #The 'Run' button
        runButton.place(relx=0.5, rely=0.5, anchor = tk.CENTER)
        
        #Resource allocation
        if(hasResource): #Only sets up if import was successful
            resButton = tk.Button(master=runFrame, text="Limit Use of Computer Resources", command=limitresourcesclicked)
            resButton.place(relx=0.5, rely=0, anchor = tk.N)