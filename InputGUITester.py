#This file was created by Tate Hagan
import tkinter as tk
from InputGUISoloDebug import InputGUI

root = tk.Tk()

container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)
frames = {}
F = InputGUI
page_name = F.__name__
frame = F(parent=container)
frames[page_name] = frame
frame.grid(row=0, column=0, sticky="nsew")
showframe = frames[page_name]
showframe.tkraise()

root.mainloop()