#Author: Josh Renshaw
#Date: 19/10/2020
#Purpose: This file creates a GUI which will display any given matplotlib.pyplot
#         plot within a tkinter window, the GUI also implements the inbuilt
#         navigation functions (pan/zoom/etc.) of matplotlib as a navigation toobar
import tkinter as tk #imports GUI elements from tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) #imports the element to hold the figure/the matplotlib toobar
from DataOutput import outputDataToGUI #connects the GUI to the DataOutput component to get data from

#defines the PhotometryGUI class to be used in the GUIHandler as a frame to display
class PhotometryGUI(tk.Frame):
    #initialize the frame
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        #defines parent elements as global such that other elements can see them
        global mainCanvas
        global frame
        frame = self

    #sets up and displays data from dataObject/fig when called from other components
    def photoGUI(self, fig, dataObject):
        #creates a slice on screen and sends slice info to the dataObject
        def sendSlice(sliceWin, starName, brightness, strWidth):
            #checks the input values for validity, displays error window if ANY value is incorrect
            try:
                width = int(strWidth)
                if(starName == ''):
                    raise ValueError('invalid star name')
                if((float(brightness) > 10.0) or (float(brightness) < -2.0)):
                    raise ValueError('invalid brightness')
                if(width <= 0):
                    raise ValueError('invalid width')

                #send the slice to the dataObject
                dataObject.setSlice(int(ix), int(iy), starName, width, float(brightness))

                #set slice button back to normal
                btn['state'] = tk.NORMAL

                #add the slice to the screen using axes information
                ax.text(ix, iy-50, starName)
                ax.text(ix, iy, 'x', color='red')
                ax.text(ix+width/2, iy, '|', color='red')
                ax.text(ix-width/2, iy, '|', color='red')

                #update the canvas to show new axes info
                canvas.draw()

                #enable the undo button as there is now a slice to undo
                undoButton['state'] = tk.NORMAL

                #kill the sliceWin as we are done with this slice
                sliceWin.destroy()

            except ValueError:
                tk.messagebox.showerror("Invalid Slice Inputs", "The input slice is invalid, please enter a valid input.")

        #creates the star slice window when the star slice button is pressed
        def starSliceWindow(ix, iy):
            #ensures user does not use the default 'X' button to exit the window unsafely
            def disable_event():
                tk.messagebox.showerror("Invalid Button Press", "Please use the Cancel button to exit safely")

            #allows the window to be exited safely
            def cancelSlice():
                btn['state'] = tk.NORMAL
                sliceWin.destroy()

            #stops looking for a click on the figure canvas
            canvas1.mpl_disconnect(cid)

            #create and format the slice window
            sliceWin = tk.Toplevel(pady=10)
            sliceWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Star Slice Selector")
            sliceWin.wm_geometry("200x250")

            #create the star name entry elements
            starEntryLabel = tk.Label(sliceWin, text="Enter name of star: ")
            starEntryLabel.pack()
            starEntry = tk.Entry(sliceWin)
            starEntry.pack()
            starEntry.focus_set()

            #create the brighness entry elements
            brightnessEntryLabel = tk.Label(sliceWin, text="Enter brightness of star: ")
            brightnessEntryLabel.pack()
            brightnessEntry = tk.Entry(sliceWin)
            brightnessEntry.pack()

            #create the width entry elements
            widthEntryLabel = tk.Label(sliceWin, text="Enter slice width: ")
            widthEntryLabel.pack()
            widthEntry = tk.Entry(sliceWin)

            #use the default width
            widthEntry.insert(tk.END, "50")
            widthEntry.pack()

            #convert coords from figure to ints to display
            intX = int(ix)
            intY = int(iy)

            #show the coords in a label
            lb = tk.Label(sliceWin, text="Coordinatess: {}, {}".format(intX, intY))
            lb.pack()

            #create the cancel button, link it to the cancelSlice function
            cancelBtn = tk.Button(sliceWin, text="Cancel Star Slice", command= lambda: cancelSlice())
            cancelBtn.pack(side=tk.BOTTOM)
            cancelBtn.bind('<Return>', (lambda event: cancelSlice()))

            #create the submit star slice button, link it to the sendSlice function
            #sends data to sendSlice using lamda expressions
            starEntryBtn = tk.Button(sliceWin, text="Submit Star Slice", command= lambda: sendSlice(sliceWin, starEntry.get(), brightnessEntry.get(), widthEntry.get()))
            starEntryBtn.pack(side=tk.BOTTOM)
            sliceWin.bind('<Return>', (lambda event: sendSlice(sliceWin, starEntry.get(), brightnessEntry.get(), widthEntry.get())))

            #disables the 'X' quit button to ensure window is exited safely
            sliceWin.protocol("WM_DELETE_WINDOW", disable_event)
        #called when user clicks on the figure to create a slice
        def figClick(event):
            #gets the coord data from the figure
            global ix, iy
            ix, iy = event.xdata, event.ydata

            if (ix is None) and (iy is None):
                tk.messagebox.showerror("Invalid Slice Location", "The slice loaction is invalid, slice must be located within the bounds of the figure.")
            else:
                #open the star slice win and send the coord data
                starSliceWindow(ix, iy)

        #called when sliceButton is pressed, starts checking for any clicks on the figure
        def sliceEvent(canvas):
            global cid, canvas1

            #disbale the button so only 1 slice can occur at a time
            btn['state'] = tk.DISABLED
            canvas1 = canvas

            #call figClick when there is a click on the canvas
            cid = canvas.mpl_connect('button_press_event', figClick)

        #sends data to Photometry then exits the window and switches the frame to the OutputGUI
        def _quit():
            from Photometry import performPhotometry
            performPhotometry(dataObject)
            
            dataObject.setPhotoplotImage(fig)

            outputDataToGUI(dataObject)

            #clear the frame so that the program can be run again
            for widget in frame.winfo_children():
                widget.destroy()

        #removes the last slice from the slice list, and from the axes information to remove it from the screen
        def undo():
            #remove the last slice from the slice list
            list = dataObject.getSliceList()
            list.pop()

            #disable the undo button if there are no more slices to undo
            if(len(list) == 0):
                undoButton['state'] = tk.DISABLED

            #iterate through the last 4 elements of the axes data to remove the slice from screen
            i = len(ax.texts)
            for t in ax.texts[i-4:i]:
                t.set_visible(False)
                ax.texts.pop()

            #update the canvas to show these changes
            canvas.draw()

        #build the main canvas with a dedicated size
        mainCanvas = tk.Canvas(frame, width=1600, height=900)
        mainCanvas.pack(fill="both", expand=True)

        #define global vars to give access across the functions
        global btn
        global ax

        #get axes data from the figure
        ax = fig.gca()

        #create the matplotlib figure canvas to display fig
        canvas = FigureCanvasTkAgg(fig, master=mainCanvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create the toolbar element, and attach it to the canvas to display it in the GUI
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        #create the sliceButton, call sliceEvent when clicked
        sliceButton = tk.Button(master=toolbar, text="Select Slice", command= lambda: sliceEvent(canvas), background="white", borderwidth=2)
        sliceButton.pack(side=tk.LEFT)
        btn = sliceButton

        # Create the exit button and pack it to the bottom of the GUI window, linked to the _quit on click event
        continueButton = tk.Button(master=toolbar, text="Continue", command=_quit, background="white", borderwidth=2)
        continueButton.pack(side=tk.LEFT)
        
        #create the undo button, start with the button disabled as there is not slice to undo
        undoButton = tk.Button(master=toolbar, text="Undo Last Slice", command=undo, background="white", borderwidth=2)
        undoButton.pack(side=tk.LEFT)
        undoButton['state'] = tk.DISABLED
