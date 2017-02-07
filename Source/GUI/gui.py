from tkinter import *
from tkinter import ttk

class Gui:

    def __init__(self,parent):
        self.parent = parent # a Tk() object
        parent.title("Gui")
        self.initialize()
        parent.mainloop() # this is the method that runs a Tk() object

    def initialize(self):
        # make the frame that is shown on startup
        initframe = ttk.Frame(self.parent, padding="3 3 12 12")
        initframe.grid(column=0, row=0, sticky=(N, W, E, S))
        initframe.columnconfigure(0, weight=1)
        initframe.rowconfigure(0, weight=1)
        self.parent.resizable(False, False)
        
        # make the buttons
        ttk.Button(initframe, text="Build a Neural Net", command=self.build).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(initframe, text="Train a Neural Net", command=self.train).grid(column=4, row=2, sticky=(W, E))
        ttk.Button(initframe, text="Train a Neural Net", command=self.test).grid(column=6,row=2,sticky=(W,E))

        # sets a pad for all children, not necessary
        for child in initframe.winfo_children():
            child.grid_configure(padx=20, pady=20)

    # function called when "Return Home" is clicked, deletes the overlaying frame
    def goback(self):
        self.info_frame.destroy()

    # functions called when buttons are clicked, seems like it builds a frame "on top of" of the parent frame
    def build(self):
        self.info_frame = ttk.Frame(self.parent, padding="3 3 12 12")
        self.info_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.rowconfigure(0, weight=1)

        ttk.Button(self.info_frame, text="Return Home", command=self.goback).grid(column=2, row=2, sticky=(W, E))

    
    def train(self):
        self.info_frame = ttk.Frame(self.parent, padding="3 3 12 12")
        self.info_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.rowconfigure(0, weight=1)

        ttk.Button(self.info_frame, text="Return Home", command=self.goback).grid(column=2, row=2, sticky=(W, E))

    def test(self):
        self.info_frame = ttk.Frame(self.parent, padding="3 3 12 12")
        self.info_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.rowconfigure(0, weight=1)

        ttk.Button(self.info_frame, text="Return Home", command=self.goback).grid(column=2, row=2, sticky=(W, E))


if __name__ == "__main__":
    root = Tk()
    window = Gui(root)
    
