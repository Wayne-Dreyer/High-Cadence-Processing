#This file was created by Tate Hagan
import tkinter as tk #imports the GUI framework
from tkinter import messagebox #messagebox is only imported if you explicitly state it, which is why this line is here
from GUIHandler import GUIHandler #Allows switching back to Input GUI window
#The resource package is OS dependent for UNIX systems. The error catching here is because an error will occur on Windows systems
hasResource = True
try:
    import resource as resource #used for limiting use of computer resources
except ImportError:
    hasResource = False

class LimitResourcesWin(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        minResWidth = 30 #cell size
        minResHeight = 5
        self.grid_columnconfigure(0, weight=1, minsize = minResWidth) #columns
        self.grid_columnconfigure(1, weight=1, minsize = minResWidth)
        self.grid_columnconfigure(2, weight=1, minsize = minResWidth)
        self.grid_rowconfigure(0, weight=1, minsize = minResHeight) #rows
        self.grid_rowconfigure(1, weight=1, minsize = minResHeight)
        self.grid_rowconfigure(2, weight=1, minsize = minResHeight)
        self.grid_rowconfigure(3, weight=1, minsize = minResHeight)
        self.grid_rowconfigure(4, weight=1, minsize = minResHeight)
        self.grid_rowconfigure(5, weight=1, minsize = minResHeight)
        self.grid_rowconfigure(6, weight=1, minsize = minResHeight)
        self.grid_rowconfigure(7, weight=1, minsize = minResHeight)
            
        #event handlers
        def setOutFileSizeLimit(): #Sets limit of output file size (in bytes). May result in creation of partial files
            try:
                outfilesizevalue = int(outfilesize.get())
                if(outfilesizevalue > 1000): #Checks that size is over a minimum value
                    limits = (outfilesizevalue, resource.RLIM_INFINITY)
                    try:
                        resource.setrlimit(resource.RLIMIT_CORE, limits) #Sets the resource limit
                    except ValueError: #Thrown if limit is too high
                        tk.messagebox.showerror("Error", "Input value too high")
                    except OSError: #Thrown if underlying system call fails
                        tk.messagebox.showerror("Error", "System call failed")
                else:
                    tk.messagebox.showinfo("Invalid Input", "Value too small")
            except ValueError:
                tk.messagebox.showinfo("Invalid Input", "File size limit must be an integer")
            
        def setMaxProcTime(): #Sets max processor time for process. If exceeded, SIGXCPU signal sent to process
            try:
                maxproctimevalue = int(maxproctime.get())
                if(maxproctimevalue > 10): #Checks that time is over a minimum value
                    limits = (maxproctimevalue, resource.RLIM_INFINITY)
                    try:
                        resource.setrlimit(resource.RLIMIT_CPU, limits)
                    except ValueError: #Thrown if limit is too high
                        tk.messagebox.showerror("Error", "Input value too high")
                    except OSError: #Thrown if underlying system call fails
                        tk.messagebox.showerror("Error", "System call failed")
                else:
                    tk.messagebox.showinfo("Invalid Input", "Value too small")
            except ValueError:
                tk.messagebox.showinfo("Invalid Input", "Max Processor time must be an integer")
            
        def setMaxHeapSize(): #Sets max heap size (bytes)
            try:
                maxheapsizevalue = int(maxheapsize.get()) * 1000000 #Convert from bytes to megabytes
                if(maxheapsizevalue > 750000000): #Checks that size is over a minimum value
                    limits = (maxheapsizevalue, resource.RLIM_INFINITY)
                    try:
                        resource.setrlimit(resource.RLIMIT_DATA, limits)
                    except ValueError: #Thrown if limit is too high
                        tk.messagebox.showerror("Error", "Input value too high")
                    except OSError: #Thrown if underlying system call fails
                        tk.messagebox.showerror("Error", "System call failed")
                else:
                    tk.messagebox.showinfo("Invalid Input", "Value too small")
            except ValueError:
                tk.messagebox.showinfo("Invalid Input", "Max Heap Size must be an integer")
            
        def setMaxStackSize(): #Sets max stack size (bytes) - only effects main thread
            try:
                maxstacksizevalue = int(maxstacksize.get()) * 1000 #Convert from bytes to kilobytes
                if(maxstacksizevalue > 750000): #Checks that size is over a minimum value
                    limits = (maxstacksizevalue, resource.RLIM_INFINITY)
                    try:
                        resource.setrlimit(resource.RLIMIT_STACK, limits)
                    except ValueError: #Thrown if limit is too high
                        tk.messagebox.showerror("Error", "Input value too high")
                    except OSError: #Thrown if underlying system call fails
                        tk.messagebox.showerror("Error", "System call failed")
                else:
                    tk.messagebox.showinfo("Invalid Input", "Value too small")
            except ValueError:
                tk.messagebox.showinfo("Invalid Input", "Max Stack Size must be an integer")
            
        def setMaxOpenFiles(): #sets max number of open files
            try:
                maxopenfilesvalue = int(maxopenfiles.get())
                if(maxopenfilesvalue > 15): #Checks that size is over a minimum value
                    hardlimit = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
                    limits = (maxopenfilesvalue, hardlimit)
                    try:
                        resource.setrlimit(resource.RLIMIT_NOFILE, limits) #BSD name for resource is RLIMIT_OFILE
                    except ValueError as eOut: #Thrown if limit is too high
                        tk.messagebox.showerror("Error", "Input value too high")
                    except OSError: #Thrown if underlying system call fails
                        tk.messagebox.showerror("Error", "System call failed")
                else:
                    tk.messagebox.showinfo("Invalid Input", "Value too small")
            except ValueError:
                tk.messagebox.showinfo("Invalid Input", "Max Stack Size must be an integer")
            
#Commented out as doesn't work at the moment, may revisit in future sprint            
#        def setMaxAddSpace():
#            try:
#                maxaddspacevalue = int(maxaddspace.get())
#                if(maxaddspacevalue > 500): #Checks that size is over a minimum value
#                    limits = (maxaddspacevalue, resource.RLIM_INFINITY)
#                    try:
#                        resource.setrlimit(resource.RLIMIT_AS, limits)
#                    except ValueError: #Thrown if limit is too high
#                        tk.messagebox.showerror("Error", "Input value too high")
#                    except OSError: #Thrown if underlying system call fails
#                        tk.messagebox.showerror("Error", "System call failed")
#                else:
#                    tk.messagebox.showinfo("Invalid Input", "Value too small")
#            except ValueError:
#                tk.messagebox.showinfo("Invalid Input", "Max Stack Size must be an integer")
                   
        def setMaxSwapSize():
            try:
                maxswapsizevalue = int(maxswapsize.get())
                if(maxswapsizevalue > 100): #Checks that size is over a minimum value
                    limits = (maxswapsizevalue, resource.RLIM_INFINITY)
                    try:
                        resource.setrlimit(resource.RLIMIT_SWAP, limits)
                    except ValueError: #Thrown if limit is too high
                        tk.messagebox.showerror("Error", "Input value too high")
                    except OSError: #Thrown if underlying system call fails
                        tk.messagebox.showerror("Error", "System call failed")
                else:
                    tk.messagebox.showinfo("Invalid Input", "Value too small")
            except ValueError:
                tk.messagebox.showinfo("Invalid Input", "Max Stack Size must be an integer")
            
        def exitClicked():
            guiHandler = GUIHandler.getInstance()
            guiHandler.setWindow("InputGUI")
                
        #widgets
        currRow = 0
        #output file size
        if(hasattr(resource, 'RLIMIT_CORE')):
            outfilesizelabel = tk.Label(master=self, text = "Maximum Output File Size (bytes):")
            outfilesizelabel.grid(row=currRow, column=0)
            outfilesize = tk.Entry(master=self)
            outfilesize.grid(row=currRow, column=1)
            outfilebutton = tk.Button(master=self, text="Set Limit", command=setOutFileSizeLimit)
            outfilebutton.grid(row=currRow, column=2)
            currRow = currRow + 1
        #maximum processor time
        if(hasattr(resource, 'RLIMIT_CPU')):
            maxproctimelabel = tk.Label(master=self, text = "Maximum Processor Time (seconds):")
            maxproctimelabel.grid(row=currRow, column=0)
            maxproctime = tk.Entry(master=self)
            maxproctime.grid(row=currRow, column=1)
            maxproctimebutton = tk.Button(master=self, text="Set Limit", command=setMaxProcTime)
            maxproctimebutton.grid(row=currRow, column=2)
            currRow = currRow + 1
        #maximum heap size
        if(hasattr(resource, 'RLIMIT_DATA')):
            maxheapsizelabel = tk.Label(master=self, text = "Maximum Heap Size (MB):")
            maxheapsizelabel.grid(row=currRow, column=0)
            maxheapsize = tk.Entry(master=self)
            maxheapsize.grid(row=currRow, column=1)
            maxheapsizebutton = tk.Button(master=self, text="Set Limit", command=setMaxHeapSize)
            maxheapsizebutton.grid(row=currRow, column=2)
            currRow = currRow + 1
        #maximum stack size
        if(hasattr(resource, 'RLIMIT_STACK')):
            maxstacksizelabel = tk.Label(master=self, text="Maximum Stack Size (kB):")
            maxstacksizelabel.grid(row=currRow, column=0)
            maxstacksize = tk.Entry(master=self)
            maxstacksize.grid(row=currRow, column=1)
            maxstacksizebutton = tk.Button(master=self, text="Set Limit", command=setMaxStackSize)
            maxstacksizebutton.grid(row=currRow,column=2)
            currRow = currRow + 1
        #maximum number of open file descriptors
        if(hasattr(resource, 'RLIMIT_NOFILE')):
            maxopenfileslabel = tk.Label(master=self, text="Maximum Open Files (number):")
            maxopenfileslabel.grid(row=currRow, column=0)
            maxopenfiles = tk.Entry(master=self)
            maxopenfiles.grid(row=currRow, column=1)
            maxopenfilesbutton = tk.Button(master=self, text="Set Limit", command=setMaxOpenFiles)
            maxopenfilesbutton.grid(row=currRow, column=2)
            currRow = currRow + 1
        #maximum address space
#        if(hasattr(resource, 'RLIMIT_AS')):
#            maxaddspacelabel = tk.Label(master=self, text="Maximum Address Space (bytes):")
#            maxaddspacelabel.grid(row=currRow, column=0)
#            maxaddspace = tk.Entry(master=self)
#            maxaddspace.grid(row=currRow, column=1)
#            maxaddspacebutton = tk.Button(master=self, text="Set Limit", command=setMaxAddSpace)
#            maxaddspacebutton.grid(row=currRow, column=2)
#            currRow = currRow + 1
#        maximum swap size
        if(hasattr(resource, 'RLIMIT_SWAP')):
            maxswapsizelabel = tk.Label(master=self, text="Maximum Swap Size (bytes):")
            maxswapsizelabel.grid(row=currRow, column=0)
            maxswapsize = tk.Entry(master=self)
            maxswapsize.grid(row=currRow, column=1)
            maxswapsizebutton = tk.Button(master=self, text="Set Limit", command=setMaxSwapSize)
            maxswapsizebutton.grid(row=currRow, column=2)
            currRow = currRow + 1
        #quit pop-up window
        quitbutton = tk.Button(master=self, text="Quit", command=exitClicked)
        quitbutton.grid(row=7, column=1)
        #Other resources below
        #resource.RLIMIT_NPROC is maximum number of processes to create (threading)
        #resource.RLIMIT_MEMLOCK is maximum address space that may be locked in memory
        #resource.RLIMIT_VMEM is maximum area of mapped memory
        #resource.RLIMIT_MSGQUEUE is for POSIX messages
        #resource.RLIMIT_NICE is ceiling for 'nice level'
        #resource.RLIMIT_RTPRIO is max realtime priority
        #resource.RLIMIT_RTTIME is time (in microsec) on CPU without making blocking syscall
        #resource.RLIMIT_SIGPENDING is max signals to queue
        #resource.RLIMIT_SWAP is max swap size (bytes)
        #resource.RLIMIT_NPTS is max no pseudo-terminals