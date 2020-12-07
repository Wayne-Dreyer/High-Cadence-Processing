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
#from tempDataOutput import * #Get plot data from DataObject
#from tkinter import *
from matplotlib.widgets import Cursor
#from tempDataObject import *

#dataObject = DataObject()
class PhotometryGUI:
    def __init__(self):
        global root
        root = tk.Tk()

    def photoGUI(self, fig, dataObject):
        dataObject.changeSelectedGUI(root)
        global btn
        # Create the tkinter window and give it a title
        root.minsize(1600, 900)
        root.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Photometry")
        w = tk.Canvas(root)
        w.pack(fill="both", expand=True)
        # Create the canvas/tk.DrawingArea on which the plot will display

        canvas = FigureCanvasTkAgg(fig, master=w)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Create the toolbar element, and attach it to the canvas to display it in the GUI
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    #    canvas.mpl_connect("key_press_event", on_key_press)
        def sendSlice(sliceWin, starName):
            print(starName, ix, iy)#send to other component here, just print to screen for now
            #root.grab_release()
            btn['state'] = tk.NORMAL
            sliceWin.destroy()
        def starSliceWindow(ix, iy):
            #root.grab_set()
            canvas1.mpl_disconnect(cid)
            sliceWin = tk.Toplevel()
            sliceWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Star Slice Selector")
            sliceWin.wm_geometry("500x100")
            starEntryLabel = tk.Label(sliceWin, text="Enter name of star: ")
            starEntryLabel.pack()
            starEntry = tk.Entry(sliceWin)
            starEntry.pack()
            starEntry.focus_set()

            intX = int(ix)
            intY = int(iy)

            lb = tk.Label(sliceWin, text="Coordinatess: {}, {}".format(intX, intY))
            lb.pack()
            starEntryBtn = tk.Button(sliceWin, text="Submit Star Slice", command= lambda: sendSlice(sliceWin, starEntry.get()))
            starEntryBtn.pack()
            sliceWin.bind('<Return>', (lambda event: sendSlice(sliceWin, starEntry.get())))
        def onclick(event):
            global ix, iy
            ix, iy = event.xdata, event.ydata
            #print(ix, iy)
            if (ix is None) and (iy is None):
                print("no window made")
            else:
                starSliceWindow(ix, iy)
        def sliceEvent(canvas):
            global cid, canvas1
            btn['state'] = tk.DISABLED
            canvas1 = canvas
            cid = canvas.mpl_connect('button_press_event', onclick)
        sliceButton = tk.Button(master=toolbar, text="Select Slice", command= lambda: sliceEvent(canvas), background="white", borderwidth=2)
        sliceButton.pack(side=tk.LEFT)
        btn = sliceButton
        #c = tk.Canvas(master=toolbar, width=1075, height=25)
        #c.pack(side=tk.LEFT)
            # On click event for the exit button
        def _quit():
            root.quit()     # stops mainloop
        # Create the exit button and pack it to the bottom of the GUI window, linked to the _quit on click event
        button = tk.Button(master=toolbar, text="Quit", command=_quit, background="white", borderwidth=2)
        button.pack(side=tk.LEFT)
        # Run the GUI
        root.mainloop()


    # On Click event for the inbuilt toolbar
    #def on_key_press(event):
    #    print("you pressed {}".format(event.key))
    #    key_press_handler(event, canvas, toolbar)
    # Call to the on click event

    #    root.destroy() This is required on Windows OS


    #def func(event):
    #    print('hit return')




        #win = tk.Tk()
        #win.geometry("200x200+200+100")
        #button = tk.Button(win, text="Open new Window")
        #button['command'] = new_window1
        #button.pack()
        #win.mainloop()

        #app = tk.Tk()
        #app.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Star Slice")

        #appW = tk.Canvas(root, width=800, height=400)
        #appW.pack()

        #app.mainloop()

    #data = tempDataOutput()
    #fig = data.getPlot()

    #photoGUI(fig)
