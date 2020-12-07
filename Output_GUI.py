#Author: Josh Renshaw
#Date: 19/10/2020
#Purpose: This file creates a GUI which will display any given matplotlib.pyplot
#         plot within a tkinter window, the GUI also implements the inbuilt
#         navigation functions (pan/zoom/etc.) of matplotlib as a navigation toobar
from os import name
import tkinter as tk #used for the tkinter GUI window
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib.pyplot import (fill, close) #used to implement the default matplotlib key bindings
from GUIHandler import GUIHandler #connects GUI to the handler

import numpy as np

#defines the OutputGUI class to be used in the GUIHandler as a frame to display
class OutputGUI(tk.Frame):
    #initialize the frame
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        #defines parent elements as global such that other elements can see them
        global mainCanvas
        global frame
        frame = self

    #sets up and displays data from dataObject/fig/outputString when called from other components
    def outputGUI(self, fig, dataObject, outputString):
        #creates a new window to browse where to save file
        def browseFiles():
            #get the file path
            filename = str(tk.filedialog.asksaveasfilename(initialdir = "/", title = "Save File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*"))))
            str1 = ''
            #try save the file
            try:
                names = filename.split("/")

                file = names[len(names) - 1]

                for ele in names:  
                    str1 += ele + '/'
                path = str1.replace(file + "/", "")
                
                tk.messagebox.showinfo("File Saved Successfully", "File saved to: " + filename)

                from DataOutput import outputDataToFile
                outputDataToFile(dataObject, file, path)
            #notify user if saving failed
            except FileNotFoundError:
                tk.messagebox.showerror("Invalid File Path", "The file path was invalid and the file was unable to be saved.")
        #creates a window to display the outputString
        def outputEvent():
            outputWin = tk.Toplevel()
            outputWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Calculated Output")
            outputWin.wm_geometry("1000x600")

            #format the string and insert the string into the window as read-only
            text = tk.Text(outputWin)

            text.insert(tk.INSERT, outputString)
            text.config(state = tk.DISABLED)
            text.pack(fill=tk.BOTH, expand=1)
            browseBtn = tk.Button(outputWin, text="Save file...", command= lambda:browseFiles())
            browseBtn.pack(side = tk.BOTTOM)

        #creates a window to get filter values
        def cLimEvent():
            #format the main window
            filterInputWin = tk.Toplevel()
            filterInputWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Filter Input")
            filterInputWin.wm_geometry("250x125")

            #create the min value entry elements
            minFilterEntryLabel = tk.Label(filterInputWin, text="Enter min filter value: ")
            minFilterEntryLabel.pack()
            minFilterEntry = tk.Entry(filterInputWin)
            minFilterEntry.pack()
            minFilterEntry.focus_set()

            #create the max value entry elements
            maxFilterEntryLabel = tk.Label(filterInputWin, text="Enter max filter value: ")
            maxFilterEntryLabel.pack()
            maxFilterEntry = tk.Entry(filterInputWin)
            maxFilterEntry.pack()

            #create the submit button element
            filterEntryBtn = tk.Button(filterInputWin, text="Submit Filter Limits", command= lambda: filterPlot(minFilterEntry.get(), maxFilterEntry.get()))
            filterEntryBtn.pack()
            filterInputWin.bind('<Return>', (lambda event: filterPlot(minFilterEntry.get(), maxFilterEntry.get())))

            #creates the filtered plot in a new window
            def filterPlot(cmin, cmax):

                #validate the min/max values, order of them doesnt matter just need to be valid numbers
                try:
                    if (cmin == '') or (cmax == ''):
                        raise ValueError('no input')

                    #convert to floats
                    minResult = float(cmin)
                    maxResult = float(cmax)

                    #destroy the input windows
                    filterInputWin.destroy()

                    #create/format the new window
                    filterWin = tk.Toplevel()
                    filterWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Filtered Output")
                    filterWin.wm_geometry("1600x800")

                    #make call to DataOutput to get new figure to display
                    from DataOutput import getFilteredPlot
                    filteredFig = getFilteredPlot(cmin, cmax, fig)

                    #put the figure in a matplotlib figure canvas
                    filterCanvas = FigureCanvasTkAgg(filteredFig, master=filterWin)
                    filterCanvas.draw()
                    filterCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                    #make the toolbar for the figure canavas
                    filterToolbar = NavigationToolbar2Tk(filterCanvas, filterWin)
                    filterToolbar.update()
                    filterCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                    #make the quit button
                    filterQuitBtn = tk.Button(master=filterToolbar, text="Quit", command=lambda: filterWinQuit(), background="white", borderwidth=2)
                    filterQuitBtn.pack(side=tk.LEFT)

                    #exits the window
                    def filterWinQuit():
                        filterWin.destroy()

                except ValueError:
                    tk.messagebox.showerror("Invalid Filter Inputs", "The input filters are invalid, please enter a valid input.")

        #onClick for quit button, makes call to GUIHandler in order to quit window safely
        def _quit():
            handler = GUIHandler.getInstance()
            handler.setWindow("InputGUI")
            #close all figures to conserve memory
            close('all')
            #clear the frame so that the program can be run again
            for widget in frame.winfo_children():   
                widget.destroy()

        if(dataObject.getFlag() == 'CheckPixels'):
            #get the zoom factor
            zoomFactor = dataObject.getCheckFactor()
            #get the dimensions of the zoomed image
            realHeight = dataObject.getHeight()/2
            realWidth = dataObject.getWidth()/2

            #get axes data from the figure
            ax = fig.gca()

            ax.set_ybound(lower=realWidth*2, upper=0) 
            ax.set_xbound(lower=0, upper=realHeight*2)

        #Create the standard size canvas
        mainCanvas = tk.Canvas(frame, width=1600, height=900)
        mainCanvas.pack(fill="both", expand=True)

        #Create the FigCanvas on which the plot will display, anchor to TOP, fill to parent canvas
        figCanvas = FigureCanvasTkAgg(fig, master=mainCanvas)
        figCanvas.draw()
        figCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create the toolbar element, and attach it to the FigCanvas to display it in the GUI, anchor to TOP, fill parent canvas
        toolbar = NavigationToolbar2Tk(figCanvas, frame)
        toolbar.update()
        figCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        #create the select limits button element
        limitsButton = tk.Button(master=toolbar, text="Select Colour Limits", command=lambda: cLimEvent(), background="white", borderwidth=2)
        limitsButton.pack(side=tk.LEFT)

        #check if there is an outputString to display, if so make the outputButton
        if(outputString != None):
            #make the button to show the outputString
            outputButton = tk.Button(master=toolbar, text="Show Calculated Output", command=lambda: outputEvent(), background="white", borderwidth=2)
            outputButton.pack(side=tk.LEFT)
        else:
            #make the button to show the outputString
            outputButton = tk.Button(master=toolbar, text="Save File...", command=lambda: browseFiles(), background="white", borderwidth=2)
            outputButton.pack(side=tk.LEFT)
            
        # Create the exit button and pack it to the bottom of the GUI window, linked to the _quit on click event
        quitButton = tk.Button(master=toolbar, text="Return to Input GUI", command=_quit, background="white", borderwidth=2)
        quitButton.pack(side=tk.LEFT)

    def multipleOutputGUI(self, figs, dataObject, outputString):
        #creates a new window to browse where to save file
        def browseFiles():
            #get the file path
            filename = str(tk.filedialog.asksaveasfilename(initialdir = "/", title = "Save File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*"))))
            str1 = ''
            #try save the file
            try:
                names = filename.split("/")

                file = names[len(names) - 1]

                for ele in names:  
                    str1 += ele + '/'
                path = str1.replace(file + "/", "")
                
                tk.messagebox.showinfo("File Saved Successfully", "File saved to: " + filename)

                from DataOutput import outputDataToFile
                outputDataToFile(dataObject, file, path)
            #notify user if saving failed
            except FileNotFoundError:
                tk.messagebox.showerror("Invalid File Path", "The file path was invalid and the file was unable to be saved.")
        #creates a window to display the outputString
        def outputEvent():
            outputWin = tk.Toplevel()
            outputWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Calculated Output")
            outputWin.wm_geometry("1000x600")

            #format the string and insert the string into the window as read-only
            text = tk.Text(outputWin)

            text.insert(tk.INSERT, outputString)
            text.config(state = tk.DISABLED)
            text.pack(fill=tk.BOTH, expand=1)
            browseBtn = tk.Button(outputWin, text="Save file...", command= lambda:browseFiles())
            browseBtn.pack(side = tk.BOTTOM)

        #creates a window to get filter values
        def cLimEvent(fig):
            #format the main window
            filterInputWin = tk.Toplevel()
            filterInputWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Filter Input")
            filterInputWin.wm_geometry("250x125")

            #create the min value entry elements
            minFilterEntryLabel = tk.Label(filterInputWin, text="Enter min filter value: ")
            minFilterEntryLabel.pack()
            minFilterEntry = tk.Entry(filterInputWin)
            minFilterEntry.pack()
            minFilterEntry.focus_set()

            #create the max value entry elements
            maxFilterEntryLabel = tk.Label(filterInputWin, text="Enter max filter value: ")
            maxFilterEntryLabel.pack()
            maxFilterEntry = tk.Entry(filterInputWin)
            maxFilterEntry.pack()

            #create the submit button element
            filterEntryBtn = tk.Button(filterInputWin, text="Submit Filter Limits", command= lambda: filterPlot(minFilterEntry.get(), maxFilterEntry.get()))
            filterEntryBtn.pack()
            filterInputWin.bind('<Return>', (lambda event: filterPlot(minFilterEntry.get(), maxFilterEntry.get())))

            #creates the filtered plot in a new window
            def filterPlot(cmin, cmax):

                #validate the min/max values, order of them doesnt matter just need to be valid numbers
                try:
                    if (cmin == '') or (cmax == ''):
                        raise ValueError('no input')

                    #convert to floats
                    minResult = float(cmin)
                    maxResult = float(cmax)

                    #destroy the input windows
                    filterInputWin.destroy()

                    #create/format the new window
                    filterWin = tk.Toplevel()
                    filterWin.wm_title("High Cadence Optical Transient Searches using Drift Scan Imaging - Filtered Output")
                    filterWin.wm_geometry("1600x800")

                    #make call to DataOutput to get new figure to display
                    from DataOutput import getFilteredPlot
                    filteredFig = getFilteredPlot(cmin, cmax, fig)

                    #put the figure in a matplotlib figure canvas
                    filterCanvas = FigureCanvasTkAgg(filteredFig, master=filterWin)
                    filterCanvas.draw()
                    filterCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                    #make the toolbar for the figure canavas
                    filterToolbar = NavigationToolbar2Tk(filterCanvas, filterWin)
                    filterToolbar.update()
                    filterCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                    #make the quit button
                    filterQuitBtn = tk.Button(master=filterToolbar, text="Quit", command=lambda: filterWinQuit(), background="white", borderwidth=2)
                    filterQuitBtn.pack(side=tk.LEFT)

                    #exits the window
                    def filterWinQuit():
                        filterWin.destroy()

                except ValueError:
                    tk.messagebox.showerror("Invalid Filter Inputs", "The input filters are invalid, please enter a valid input.")

        #onClick for quit button, makes call to GUIHandler in order to quit window safely
        def _quit():
            #switch the frame
            handler = GUIHandler.getInstance()
            handler.setWindow("InputGUI")
            #close all figures to conserve memory
            close('all')
            #clear the frame so that the program can be run again
            for widget in frame.winfo_children():   
                widget.destroy()

        def logicFunc(figs):
            tooManyFigsWin.destroy()
            #get the zoomed images list from dataobject
            zoomedImages = []
            zoomedImages = dataObject.getZoomedImages()

            #get the zoom factor
            zoomFactor = dataObject.getZoomFactor()

            #create tabs for multiple figure display
            tabControl = ttk.Notebook(frame)

            tabs = []
            mainCs = []
            figCs = []
            toolBs = []
            lBtns = []
            outBtns = []
            qBtns = []

            for n in range(0, int(len(figs))):
                tabName = str(n + 1)
                
                tabs.append(tk.Frame(tabControl, width=1700, height=1000))
                tabControl.add(tabs[n], text=tabName)
                
                
                #Create the standard size canvas
                mainCs.append(tk.Canvas(tabs[n], width=1550, height=850))
                mainCs[n].pack(fill="both", expand=True)

                #Create the FigCanvas on which the plot will display, anchor to TOP, fill to parent canvas
                figCs.append(FigureCanvasTkAgg(figs[n], master=mainCs[n]))
                figCs[n].draw()
                figCs[n].get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                # Create the toolbar element, and attach it to the FigCanvas to display it in the GUI, anchor to TOP, fill parent canvas
                toolBs.append(NavigationToolbar2Tk(figCs[n], tabs[n]))
                toolBs[n].update()
                figCs[n].get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                #create the select limits button element
                lBtns.append(tk.Button(master=toolBs[n], text="Select Colour Limits", command=lambda: cLimEvent(figs[tabControl.index(tabControl.select())]), background="white", borderwidth=2))
                lBtns[n].pack(side=tk.LEFT)

                #check if there is an outputString to display, if so make the outputButton
                if(outputString != None):
                #make the button to show the outputString
                    outBtns.append(tk.Button(master=toolBs[n], text="Show Calculated Output", command=lambda: outputEvent(), background="white", borderwidth=2))
                    outBtns[n].pack(side=tk.LEFT)
                else:
                    outBtns.append(tk.Button(master=toolBs[n], text="Save File...", command=lambda: browseFiles(), background="white", borderwidth=2))
                    outBtns[n].pack(side=tk.LEFT)
                    
                # Create the exit button and pack it to the bottom of the GUI window, linked to the _quit on click event
                qBtns.append(tk.Button(master=toolBs[n], text="Return to Input GUI", command=_quit, background="white", borderwidth=2))
                qBtns[n].pack(side=tk.LEFT)

                #get the dimensions of the zoomed image
                realHeight = zoomedImages[n].getHeight()/2
                realWidth = zoomedImages[n].getWidth()/2

                #get axes data from the figure
                ax = figs[n].gca()

                ax.set_ybound(lower=realWidth*2, upper=0) 
                ax.set_xbound(lower=0, upper=realHeight*2)
                tabControl.pack()

        def yesFunc(figs):
            figs = figs[:50]
            logicFunc(figs)

        def noFunc(figs):
            logicFunc(figs)

        if(len(figs) <= 0):
            tk.messagebox.showinfo("Warning - No detections found", "There are 0 detections found, returning to the Input GUI.")
            _quit()

        if(len(figs) >= 50):
            #tk.messagebox.showinfo("Warning - Too many figures", "There are " + str(len(figs)) + " figures, only the first 50 figures will be displayed. Please lower the detection threshold and run again.")
            tooManyFigsWin = tk.Toplevel()
            tooManyFigsWin.wm_title("Warning - Too many figures")
            tooManyFigsWin.wm_geometry("300x125")

            
            #create the max value entry elements
            tooManyFigsEntry = tk.Label(tooManyFigsWin, text="There are " + str(len(figs)) + " figures, \nonly the first 50 figures will be displayed. \nDo you want to load all the figures?")
            tooManyFigsEntry.pack()

            #create the submit button element
            tooManyFigsBtnY = tk.Button(tooManyFigsWin, text="No", command= lambda: yesFunc(figs))
            tooManyFigsBtnN = tk.Button(tooManyFigsWin, text="Yes", command= lambda: noFunc(figs))

            tooManyFigsBtnY.pack()
            tooManyFigsBtnN.pack()