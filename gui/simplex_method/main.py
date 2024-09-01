import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame, Canvas, Scrollbar, Button, Tk, Text, HORIZONTAL
from algo.simplex import SimplexLinearProgram  # Ensure this import matches your file structure
from gui.config import *
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
DATA_PATH = OUTPUT_PATH.parent.parent / "algo" / "input.csv"
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Simplex(Frame):
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
        self.canvas.create_rectangle(
            40.0, 14.0, 742.0, 16.0, fill="#EFEFEF", outline=""
        )

        self.canvas.create_rectangle(
            40.0, 420.0, 742.0, 422.0, fill="#EFEFEF", outline=""
        )

        self.scrolled_frame = Frame(self)
        self.scrolled_frame.place(x=40, y=18, width=702, height=400)

        self.y_scrollbar = Scrollbar(self.scrolled_frame)
        self.y_scrollbar.pack(side="right", fill="y")

        self.x_scrollbar = Scrollbar(self.scrolled_frame, orient=HORIZONTAL)
        self.x_scrollbar.pack(side="bottom", fill="x")

        self.input_canvas = Canvas(
            self.scrolled_frame,
            bg="#EFEFEF",
            width=702,
            height=650,
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set
        )
        
        self.input_canvas.pack(side="left", fill="both", expand=True)
        self.y_scrollbar.config(command=self.input_canvas.yview)
        self.x_scrollbar.config(command=self.input_canvas.xview)

        # Update scrollregion when the size of the text frame changes
        self.text_frame = Frame(self.input_canvas, bg="#FFFFFF")

        self.text_frame.bind("<Configure>", self.on_frame_configure)
        self.text_widget = Text(self.text_frame, bg="#FFFFFF", font=("Helvetica", 16), wrap="none")
        self.text_widget.pack(fill="both", expand=True)
        self.input_canvas.create_window((0, 0), window=self.text_frame, anchor="nw", width=982, height=1000)
        self.text_widget.config(yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)
        # Tag configurations for styling
        self.text_widget.tag_configure("subscript", offset=-4, font=("Helvetica", 8))
        self.text_widget.tag_configure("red", foreground="#ff505f", font=("Helvetica", 16, "bold"))
        self.text_widget.tag_configure("blue", foreground="#5E95FF", font=("Helvetica", 14, "bold"))


        # Liên kết sự kiện cuộn chuột với thanh cuộn


    def on_frame_configure(self, event):
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.input_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shiftmouse(self, event):
        self.input_canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def show_results(self, df):
        lp = SimplexLinearProgram(df)
        lp.run_program()
        print(df)
        self.text_widget.delete("1.0","end")

        # Adding formatted text to the text widget
        def insert_text(text, tag=None):
            if tag:
                self.text_widget.insert("end", text, tag)
            else:
                self.text_widget.insert("end", text)

        def format_tableau(tableau):
            formatted = ""
            for row in tableau:
                formatted += "\t".join([f"{val:.2f}" for val in row]) + "\n"
            return formatted

        if lp.method != 2:
            if lp.method == 0:
                insert_text("Dantzig method\n", "blue")
            else:
                insert_text("Bland method\n", "blue")


            insert_text("Number of Iterations: ", "blue")
            insert_text(f"{len(lp.iterations)}\n", "blue")
            
            for i, iteration in enumerate(lp.iterations):
                insert_text(f"Iteration {i+1}:\n", "blue")
                insert_text(format_tableau(iteration) + "\n")

                if i < len(lp.pivot_indices):
                    pivot_row, pivot_col = lp.pivot_indices[i]
                    insert_text(f"Pivot Element at row {pivot_row + 1}, column {pivot_col + 1}\n", "red")

            if lp.check == 0:
                insert_text("The problem appears to be unbounded\n", "red")
            elif lp.check == 2:
                insert_text("The problem has no solutions\n", "red")
            else:
                insert_text("The problem has solutions\n", "blue")
                if lp.optimal_point is not None:
                    insert_text("Optimal Point: ", "blue")
                    insert_text(f"{lp.optimal_point}\n", "blue")

            insert_text("Optimal Value: ", "blue")
            insert_text(f"{lp.optimal_value}\n", "blue")

        else:
            insert_text("Two-phase method\n", "blue")
            insert_text("Phase 1 Iterations: ", "blue")
            insert_text(f"{len(lp.iterations_p1)}\n", "blue")
            
            for i, iteration in enumerate(lp.iterations_p1):
                insert_text(f"Phase 1 - Iteration {i+1}:\n", "blue")
                insert_text(format_tableau(iteration) + "\n")

                if i < len(lp.pivot_indices_p1):
                    pivot_row, pivot_col = lp.pivot_indices_p1[i]
                    insert_text(f"Pivot Element at row {pivot_row + 1}, column {pivot_col + 1}\n", "red")

            if lp.check == 0:
                insert_text("The problem appears to be unbounded\n", "red")
            elif lp.check == 2:
                insert_text("The problem has no solutions\n", "red")
            else:
                insert_text("Phase 2 Iterations: ", "blue")
                insert_text(f"{len(lp.iterations_p2)}\n", "blue")

                for i, iteration in enumerate(lp.iterations_p2):
                    insert_text(f"Phase 2 - Iteration {i+1}:\n", "blue")
                    insert_text(format_tableau(iteration) + "\n")

                    if i < len(lp.pivot_indices_p2):
                        pivot_row, pivot_col = lp.pivot_indices_p2[i]
                        insert_text(f"Pivot Element at row {pivot_row + 1}, column {pivot_col + 1}\n", "red")

                insert_text("The problem has solutions\n", "blue")
                insert_text("Optimal Value: ", "blue")
                insert_text(f"{lp.optimal_value}\n", "blue")

            if lp.optimal_point is not None:
                insert_text("Optimal Point: ", "blue")
                insert_text(f"{lp.optimal_point}\n", "blue")

        self.input_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.input_canvas.bind_all("<Shift-MouseWheel>", self._on_shiftmouse)

 