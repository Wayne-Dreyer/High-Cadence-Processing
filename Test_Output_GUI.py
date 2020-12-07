#Author: Josh Renshaw
#Date: 19/08/2020
#Purpose: This file creates a GUI which will display any given matplotlib.pyplot
#         plot within a tkinter window, the GUI also implements the inbuilt
#         navigation functions (pan/zoom/etc.) of matplotlib as a navigation toobar
import tkinter as tk #used for the tkinter GUI window
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) #used to implement the default matplotlib key bindings
from matplotlib.backend_bases import key_press_handler #required to use the default navigation toolbar
from matplotlib.figure import Figure #required to display the figure in the GUI canvas
import matplotlib.pyplot as plt #used to create a plot as a PLACEHOLDER
import numpy as np #used to do math to create a PLACEHOLDER plot
from tempDataOutput import *
#from FOB import *
#import sys
#np.set_printoptions(threshold=sys.maxsize)

#Create the tkinter main window
#dataObject = DataObject()
class OutputGUI:
    def __init__(self):
        global root, mainCanvas
        root = tk.Tk()
        mainCanvas = tk.Canvas(root)

    def outputGUI(self, fig, dataObject):
        dataObject.changeSelectedGUI(root)
        #Give the main windows a title
        root.minsize(1600, 900)
        root.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Output")
        #Create the standard size canvas
        mainCanvas.pack(fill="both", expand=True)
        #Create the FigCanvas on which the plot will display, anchor to TOP,
        #fill to parent canvas
        figCanvas = FigureCanvasTkAgg(fig, master=mainCanvas)
        figCanvas.draw()
        figCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Create the toolbar element, and attach it to the FigCanvas to display it
        #in the GUI, anchor to TOP, fill parent canvas
        toolbar = NavigationToolbar2Tk(figCanvas, root)
        toolbar.update()
        figCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Call to the on click event
        #canvas.mpl_connect("key_press_event", on_key_press)
        # On click event for the exit button
         # stops mainloop
        #    root.destroy() This is required on Windows OS
        # Create the exit button and pack it to the bottom of the GUI window, linked to the _quit on click event
        def cLimEvent():
            filterInputWin = tk.Toplevel()
            filterInputWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Filter Input")
            filterInputWin.wm_geometry("250x125")

            minFilterEntryLabel = tk.Label(filterInputWin, text="Enter min filter value: ")
            minFilterEntryLabel.pack()
            minFilterEntry = tk.Entry(filterInputWin)
            minFilterEntry.pack()
            minFilterEntry.focus_set()

            maxFilterEntryLabel = tk.Label(filterInputWin, text="Enter max filter value: ")
            maxFilterEntryLabel.pack()
            maxFilterEntry = tk.Entry(filterInputWin)
            maxFilterEntry.pack()

            filterEntryBtn = tk.Button(filterInputWin, text="Submit Filter Limits", command= lambda: filterPlot(minFilterEntry.get(), maxFilterEntry.get()))
            filterEntryBtn.pack()
            filterInputWin.bind('<Return>', (lambda event: filterPlot(minFilterEntry.get(), maxFilterEntry.get())))

            def filterPlot(cmin, cmax):
                try:
                    if (cmin == '') or (cmax == ''):
                        raise ValueError('no input')
                    minResult = float(cmin)
                    maxResult = float(cmax)


                    filterInputWin.destroy()
                    filterWin = tk.Toplevel()
                    filterWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Filtered Output")
                    filterWin.wm_geometry("1600x800")

                    filteredFig = getFilteredPlot(cmin, cmax)

                    filterCanvas = FigureCanvasTkAgg(filteredFig, master=filterWin)
                    filterCanvas.draw()
                    filterCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                    filterToolbar = NavigationToolbar2Tk(filterCanvas, filterWin)
                    filterToolbar.update()
                    filterCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                    #filterWinFormattingCanvas = tk.Canvas(master=filterToolbar, width=1175, height=25)
                    #filterWinFormattingCanvas.pack(side=tk.LEFT)

                    filterQuitBtn = tk.Button(master=filterToolbar, text="Quit", command=lambda: filterWinQuit(), background="white", borderwidth=2)
                    filterQuitBtn.pack(side=tk.LEFT)#side = tk.RIGHT)

                    def filterWinQuit():
                        filterWin.destroy()

                except ValueError:
                    print("not a valid cmin/cmax")

        sliceButton = tk.Button(master=toolbar, text="Select Colour Limits", command=lambda: cLimEvent(), background="white", borderwidth=2)
        sliceButton.pack(side=tk.LEFT)

        #formattingCanvas = tk.Canvas(master=toolbar, width=1025, height=25)
        #formattingCanvas.pack(side=tk.LEFT)
                    #onClick for quit button
        def _quit():
            #Stops mainloop/exits the program
            root.quit()
        # Create the exit button and pack it to the bottom of the GUI window, linked to the _quit on click event
        quitButton = tk.Button(master=toolbar, text="Quit", command=_quit, background="white", borderwidth=2)
        quitButton.pack(side=tk.LEFT)

        #print(low)

        # Run the GUI
        tk.mainloop()





        #formattingCanvas = tk.Canvas(master=filterToolbar, width=1000, height=25)
        #formattingCanvas.pack(side=tk.LEFT)
        # Create the exit button and pack it to the bottom of the GUI window, linked to the _quit on click event
        #quitButton = tk.Button(master=filterToolbar, text="Quit", command=_quitFilter(), background="white", borderwidth=2)
        #quitButton.pack(tk.LEFT)

        #def _quitFilter():
            #Stops mainloop/exits the program
            #filterWin.destroy()

#data = tempDataOutput()
#fig = data.getPlot()

#outputGUI(fig)
