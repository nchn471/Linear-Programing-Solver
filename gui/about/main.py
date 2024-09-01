
from tkinter import Frame, Canvas, Entry, Text, Button, PhotoImage, messagebox
from gui.config import *

from pathlib import Path
OUTPUT_PATH = Path(__file__).parent
DATA_PATH = OUTPUT_PATH.parent.parent / "algo" / "input.csv"
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
def relative_to_assets(path: str) -> Path:

    return ASSETS_PATH / Path(path)

def about():
    About()


class About(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=432,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            36.0,
            43.0,
            anchor="nw",
            text="Linear Programing Solver",
            fill="#5E95FF",
            font=(FONT_BOLD, 26 * -1),
        )

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(191.0, 26.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(203.0, 205.0, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        image_3 = self.canvas.create_image(565.0, 205.0, image=self.image_image_3)

        self.canvas.create_rectangle(
            65.0, 174.0, 178.0, 176.0, fill="#FFFFFF", outline=""
        )

        self.canvas.create_rectangle(
            430.0, 174.0, 543.0, 176.0, fill="#FFFFFF", outline=""
        )



        self.canvas.create_text(
            197.0,
            352.0,
            anchor="nw",
            text="© 2023-2024, Ho Chi Minh University of Science",
            fill="#5E95FF",
            font=(FONT, 16 * -1),
        )

        self.canvas.create_text(
            237.0,
            372.0,
            anchor="nw",
            text="Linear Programing Courses’s Project",
            fill="#5E95FF",
            font=(FONT, 16 * -1),
        )

        self.canvas.create_text(
            65.0,
            135.0,
            anchor="nw",
            text="Created by",
            fill="#5E95FF",
            font=(FONT_BOLD, 26 * -1),
        )

        self.canvas.create_text(
            430.0,
            135.0,
            anchor="nw",
            text="About",
            fill="#5E95FF",
            font=(FONT_BOLD, 26 * -1),
        )
        self.canvas.create_text(
            65.0,
            188.0,
            anchor="nw",
            text="Nguyễn Công Hoài Nam - 21280099",
            fill="#777777",
            font=(FONT, 15 * -1),
        )
        self.canvas.create_text(
            65.0,
            217.0,
            anchor="nw",
            text="Nguyễn Công Hoài Nam - 21280099",
            fill="#777777",
            font=(FONT, 15 * -1),
        )
        self.canvas.create_text(
            65.0,
            246.0,
            anchor="nw",
            text="Nguyễn Công Hoài Nam - 21280099",
            fill="#777777",
            font=(FONT, 15 * -1),
        )

        self.canvas.create_text(
            430.0,
            188.0,
            anchor="nw",
            text="This program belongs to:",
            fill="#777777",
            font=(FONT_BOLD, 15 * -1),
        )
        self.canvas.create_text(
            430.0,
            211.0,
            anchor="nw",
            text="Ho Chi Minh University of Science",
            fill="#777777",
            font=(FONT, 15 * -1),
        )
        self.canvas.create_text(
            430.0,
            229.0,
            anchor="nw",
            text="Courses: Linear Programing",
            fill="#777777",
            font=(FONT, 15 * -1),
        )
        self.canvas.create_text(
            430.0,
            247.0,
            anchor="nw",
            text="Class Code: 22TTH_KDL ",
            fill="#777777",
            font=(FONT, 15 * -1),
        )
