import tkinter as tk #imports the GUI framework
class ProcessingWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        processingLabel = tk.Label(master=self, text = "Processing...")
        processingLabel.pack()