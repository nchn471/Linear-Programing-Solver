from tkinter import Frame, Canvas, Scrollbar, Text, LEFT, BOTH, Y, PhotoImage, Button, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from gui.config import *
from algo.graph import GraphLinearProgram

from pathlib import Path
OUTPUT_PATH = Path(__file__).parent
DATA_PATH = OUTPUT_PATH.parent.parent / "algo" / "input.csv"
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Graph(Frame):
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
            40.0, 420.0, 742.0, 422.0, fill="#EFEFEF", outline=""
        )

        self.scrolled_frame = Frame(self)
        self.scrolled_frame.place(x=40, y=18, width=702, height=400)

        # Create vertical scrollbar
        self.y_scrollbar = Scrollbar(self.scrolled_frame)
        self.y_scrollbar.pack(side="right", fill="y")

        self.input_canvas = Canvas(
            self.scrolled_frame,
            bg="#EFEFEF",
            width=702,
            height=650,
            yscrollcommand=self.y_scrollbar.set
        )
        
        self.input_canvas.pack(side="left", fill="both", expand=True)
        self.y_scrollbar.config(command=self.input_canvas.yview)



    def on_frame_configure(self, event):
        # Update the scroll region to match the size of the content frame
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.input_canvas.yview_scroll(int(-1*(event.delta/120)), "units")



    def show_graph_frame(self,df):
        # df = pd.read_csv(DATA_PATH)
        self.graph = GraphLinearProgram(df)
        self.fig = self.graph.plot_graph()


        self.plot_frame = Frame(self.input_canvas, bg="#FFFFFF")
        self.plot_frame.bind("<Configure>", self.on_frame_configure)
        self.input_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        self.fig.tight_layout(pad=0.5)
        self.fig.set_size_inches(6, 4) 

        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().pack(fill='both', expand=True)
        self.input_canvas.create_window((0, 0), window=self.plot_frame, anchor="nw", width=682, height=600)

        # Create a new frame to contain the text elements
        self.text_frame = Frame(self.input_canvas, bg="#FFFFFF")
        self.text_widget = Text(self.text_frame, bg="#FFFFFF", font=(FONT, 16), wrap="word")
        self.text_widget.pack(fill="both", expand=False)

        self.input_canvas.create_window((0, 600), window=self.text_frame, anchor="nw", width=682, height=200)
        if self.graph.is_valid():
            self.show_result()


    
    def show_result(self):
        # Cài đặt các tags cho text_widget
        self.text_widget.tag_configure("subscript", offset=-4, font=(FONT, 8))
        self.text_widget.tag_configure("red", foreground="#ff505f", font=(FONT_BOLD, 16))
        self.text_widget.tag_configure("blue", foreground="#5E95FF", font=(FONT_BOLD, 14))
        
        # Xóa nội dung hiện tại của text_widget
        self.text_widget.delete("1.0", "end")
        
        # Xác định tối ưu hóa là Minimize hay Maximize
        optimize = "min" if self.graph.minimize else "max"
        
        # Hiển thị hàm mục tiêu Z
        self.text_widget.insert("end", f"The {optimize} value of the function:\n", "blue")
        self.text_widget.insert("end", f"Z = {self.graph.c[0]}")
        self.text_widget.insert("end", "x", "red")
        self.text_widget.insert("end", "1", ("red", "subscript"))
        self.text_widget.insert("end", f" + {self.graph.c[1]}")
        self.text_widget.insert("end", "x", "red")
        self.text_widget.insert("end", "2\n", ("red", "subscript"))

        # Hiển thị vấn đề tối ưu hóa
        self.text_widget.insert("end", "Output Problems:\n", "blue")
        
        # Xác định kết quả của vấn đề tối ưu hóa
        flag = self.graph.status
        if flag == 0:
            self.text_widget.insert("end", "The problem has no solutions:\n", "red")
            self.text_widget.insert("end", f"Optimal Value = {self.graph.optimal_value}\n")
        elif flag == 1:
            self.text_widget.insert("end", "The problem has unique solutions:\n", "blue")
            self.text_widget.insert("end", f"Optimal Point = ({self.graph.solutions[0][0]},{self.graph.solutions[0][1]})\n")
            self.text_widget.insert("end", f"Optimal Value = {self.graph.optimal_value}\n")
        elif flag == 2:
            self.text_widget.insert("end", "The problem has infinity solutions:\n", "blue")
            self.text_widget.insert("end", f"Optimal line between Point = ({self.graph.solutions[0][0]},{self.graph.solutions[0][1]}) and ({self.graph.solutions[1][0]},{self.graph.solutions[1][1]})\n")
            self.text_widget.insert("end", f"Optimal Value = {self.graph.optimal_value}\n")
        else:
            self.text_widget.insert("end", "The problem appears unbounded:\n", "red")
            self.text_widget.insert("end", f"Optimal Value = {self.graph.optimal_value}\n")

        self.text_widget.config(state="disabled")  # Disable editing


