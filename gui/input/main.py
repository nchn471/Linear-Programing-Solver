
from tkinter import Frame, Canvas, Entry, Text, Button, PhotoImage, messagebox

from .create_input.main import CreateInput
from .view_input.main import ViewInput
from gui.config import *
import pandas as pd




def input():
    Input()


class Input(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selected_rid = None
        self.configure(bg="#FFFFFF")

        # Loop through windows and place them
        self.windows = {
            "add": CreateInput(self),
            "view": ViewInput(self),
        }

        self.current_window = self.windows["add"]
        self.current_window.place(x=0, y=0, width=1013.0, height=506.0)

        self.current_window.tkraise()

    def navigate(self, name):
        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Show the screen of the button pressed
        self.windows[name].place(x=0, y=0, width=1013.0, height=506.0)
    
    def refresh_view(self, df):
        self.windows["view"].insert_input(df)    

