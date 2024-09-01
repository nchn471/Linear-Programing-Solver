from tkinter import (
    Toplevel,
    Frame,
    Canvas,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
from gui.about.main import About
from gui.graphical_method.main import Graph
from gui.input.main import Input
from gui.simplex_method.main import Simplex
from gui.config import *

from pathlib import Path
OUTPUT_PATH = Path(__file__).parent
DATA_PATH = OUTPUT_PATH.parent.parent / "algo" / "input.csv"
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
def relative_to_assets(path: str) -> Path:

    return ASSETS_PATH / Path(path)
def mainWindow():
    MainWindow()


class MainWindow(Toplevel):
    # global user

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.title("Solving Linear Programing Problems")

        icon = PhotoImage(file=relative_to_assets("logo2.png"))

        self.iconphoto(True, icon)

        self.geometry("1012x506")
        self.configure(bg="#5E95FF")

        self.current_window = None
        self.current_window_label = StringVar()

        self.canvas = Canvas(
            self,
            bg="#5E95FF",
            height=506,
            width=1012,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            215, 0.0, 1012.0, 506.0, fill="#FFFFFF", outline=""
        )

        # Add a frame rectangle
        self.sidebar_indicator = Frame(self, background="#FFFFFF")

        self.sidebar_indicator.place(x=0, y=133, height=47, width=7)

        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.input_btn = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.input_btn, "input"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.input_btn.place(x=7.0, y=133.0, width=208.0, height=47.0)

        button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.simplex_btn = Button(
            self.canvas,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.simplex_btn, "simplex"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.simplex_btn.place(x=7.0, y=183.0, width=208.0, height=47.0)

        button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.graph_btn = Button(
            self.canvas,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.graph_btn, "graph"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.graph_btn.place(x=7.0, y=233.0, width=208.0, height=47.0)

        button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.about_btn = Button(
            self.canvas,
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.about_btn, "about"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.about_btn.place(x=7.0, y=283.0, width=208.0, height=47.0)

        self.heading = self.canvas.create_text(
            255.0,
            33.0,
            anchor="nw",
            text="Hello",
            fill="#5E95FF",
            font=(FONT_BOLD, 26 * -1),
        )

        self.canvas.create_text(
            28.0,
            21.0,
            anchor="nw",
            text="HCMUS",
            fill="#FFFFFF",
            font=(FONT_BOLD, 36 * -1),
        )

        self.canvas.create_text(
            844.0,
            43.0,
            anchor="nw",
            text="NCHN",
            fill="#808080",
            font=(FONT_BOLD, 16 * -1),
        )

        self.canvas.create_text(
            341.0,
            213.0,
            anchor="nw",
            text="(The screens below",
            fill="#5E95FF",
            font=(FONT_BOLD, 48 * -1),
        )

        self.canvas.create_text(
            420.0,
            272.0,
            anchor="nw",
            text="will come here)",
            fill="#5E95FF",
            font=(FONT_BOLD, 48 * -1),
        )

        # Loop through windows and place them
        self.windows = {
            "about": About(self),
            "input" : Input(self),
            "simplex" : Simplex(self),
            "graph" : Graph(self)
        }

        self.handle_btn_press(self.input_btn, "input")
        self.sidebar_indicator.place(x=0, y=133)

        self.current_window.place(x=215, y=72, width=1013.0, height=506.0)

        self.current_window.tkraise()
        self.resizable(False, False)
        self.mainloop()
        
    def handle_btn_press(self, caller, name):
        # Place the sidebar on respective button
        self.sidebar_indicator.place(x=0, y=caller.winfo_y())

        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Set ucrrent Window
        self.current_window = self.windows.get(name)

        # Show the screen of the button pressed
        self.windows[name].place(x=215, y=72, width=1013.0, height=506.0)

        # Handle label change
        current_name = self.windows.get(name)._name.split("!")[-1].capitalize()
        self.canvas.itemconfigure(self.heading, text=current_name)

    def linear_programing_solver(self,df):
        self.windows["graph"].show_graph_frame(df)
        self.windows["simplex"].show_results(df)