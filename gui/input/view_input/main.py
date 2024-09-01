from tkinter import Frame, Canvas, Button, PhotoImage, ttk, StringVar, scrolledtext, Scrollbar, Text,font
from pandastable import Table, TableModel
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui.config import *
from pathlib import Path
OUTPUT_PATH = Path(__file__).parent
DATA_PATH = OUTPUT_PATH.parent.parent / "algo" / "input.csv"
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
def relative_to_assets(path: str) -> Path:

    return ASSETS_PATH / Path(path)

class ViewInput(Frame):
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
        self.canvas.place(x=0,y=0)

        self.canvas.create_rectangle(
            40.0, 14.0, 742.0, 16.0, fill="#EFEFEF", outline=""
        )

        self.canvas.create_rectangle(
            40.0, 342.0, 742.0, 344.0, fill="#EFEFEF", outline=""
        )
        self.canvas.create_text(
            116.0,
            33.0,
            anchor="nw",
            text="View Input Problem",
            fill="#5E95FF",
            font=(FONT_BOLD, 26 * -1),
        )

        # self.canvas.create_text(
        #     40.0,
        #     367.0,
        #     anchor="nw",
        #     text="Actions:",
        #     fill="#5E95FF",
        #     font=(FONT_BOLD, 26 * -1),
        # )

        self.canvas.create_text(
            116.0,
            65.0,
            anchor="nw",
            text="",
            fill="#808080",
            font=(FONT, 16 * -1),
        )
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.navigate_back_btn = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_navigate_back,
            relief="flat",
        )
        self.navigate_back_btn.place(x=40.0, y=33.0, width=53.0, height=53.0)


        self.scrolled_frame = Frame(self)
        self.scrolled_frame.place(x=40, y=101, width=702, height=228)

        # # Create horizontal scrollbar
        # self.x_scrollbar = Scrollbar(self.scrolled_frame, orient="horizontal")
        # self.x_scrollbar.pack(side="bottom", fill="x")

        # Create vertical scrollbar
        self.y_scrollbar = Scrollbar(self.scrolled_frame)
        self.y_scrollbar.pack(side="right", fill="y")

        self.input_canvas = Canvas(
            self.scrolled_frame,
            bg="#EFEFEF",
            width=702,
            height=228,
            # xscrollcommand=self.x_scrollbar.set,
            yscrollcommand=self.y_scrollbar.set
        )
        self.input_canvas.pack(side="left", fill="both", expand=True)

        # Link scrollbars with Canvas
        # self.x_scrollbar.config(command=self.input_canvas.xview)
        self.y_scrollbar.config(command=self.input_canvas.yview)

        # Create a frame inside the canvas to hold the text
        self.text_frame = Frame(self.input_canvas, bg="#EFEFEF")
        self.text_window = self.input_canvas.create_window((0, 0), window=self.text_frame, anchor="nw")

        # Add the LaTeX content to the frame
        self.text_widget = Text(self.text_frame, bg="#EFEFEF", font=(FONT, 16), wrap="none")
        self.text_widget.pack(fill="both", expand=True)

        self.text_widget.tag_configure("subscript", offset=-4, font=(FONT, 10))
        self.text_widget.tag_configure("red", foreground="#ff505f")
        self.text_widget.tag_configure("blue", foreground="#5E95FF")

        # Update scrollregion when the size of the text frame changes
        self.text_frame.bind("<Configure>", self.on_frame_configure)


        # Liên kết sự kiện cuộn chuột với thanh cuộn
        self.input_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.input_canvas.bind_all("<Shift-MouseWheel>", self._on_shiftmouse)

    def on_frame_configure(self, event):
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.input_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shiftmouse(self, event):
        self.input_canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def df_to_str(self, df):
        n_rows = len(df)
        n_cols = len(df.columns)
        lines = []
        lines.append(f"Find the {df.iat[0, -1]} value of the function")
        z_func = "Z = "
        for col in range(n_cols-2):
            z_func+= f"{df.iat[0,col]}x_{col+1}"
            if(col < n_cols-3):
                z_func+= " + "
        lines.append(z_func)
        lines.append("Constraints")
        for row in range(1,n_rows-1):
            line = ""
            for col in range(n_cols-1):
                if col < n_cols - 2:
                    digit = len(df.iat[row,col])
                    line+= f"{" "*(3-digit)}{df.iat[row,col]}x_{col+1}"
                    if col <n_cols -3:
                        line+=" + "
                else:
                    line+=f" {df.iat[row,col]} {df.iat[row,col+1]}"
            lines.append(line)
        line = "  "
        for col in range(n_cols-2):
            if df.iat[-1,col] != "free":
                line+=f"{" "*1}x_{col+1} {df.iat[-1,col]} 0"
                if col < n_cols - 3:
                    line+=", "

        lines.append(line)
        str = "\n".join(lines)
        str = self.mapping(str)
        return str
    
    def mapping(self, input_str):
        mapping_dict = {
            "!=": "≠",
            "<=": "≤",
            ">=": "≥",
        }
        
        for key, value in mapping_dict.items():
            input_str = input_str.replace(key, value)
        
        return input_str
    
    def insert_input(self, df):
        print(df)
        self.text_widget.delete("1.0","end")
        input = self.df_to_str(df)
        for index, line in enumerate(input.split("\n")):
            parts = line.split(" ")
            for part in parts:
                if "x_" in part:
                    base, subscript = part.split("_")
                    self.text_widget.insert("end", base[:-1])
                    self.text_widget.insert("end", base[-1], "red")
                    self.text_widget.insert("end", subscript, ("subscript", "red"))
                else:
                    self.text_widget.insert("end", part)
                self.text_widget.insert("end", " ")
            self.text_widget.insert("end", "\n")
            # Tô màu xanh cho dòng 1 và 3
            if index == 0 or index == 2:
                self.text_widget.tag_add("blue", f"{index+1}.0", f"{index+1}.end")
        # self.text_widget.config(state="disabled")  # Disable editing

    
    def on_frame_configure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))
                
    def handle_navigate_back(self):
        self.parent.navigate("add")