from pathlib import Path

from tkinter import Frame, Canvas, Button, PhotoImage, ttk, StringVar, messagebox, Entry, END
from pandastable import Table, TableModel
import pandas as pd

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
DATA_PATH = OUTPUT_PATH.parent.parent.parent / Path("./algo")
from gui.config import *


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

df = pd.DataFrame({
    "x1": ["","",""],
    "x2": ["","",""],
    "operator": ["||","",""],
    "rhs": ["min","",""]
})

class CustomTable(Table):
    """Custom table class inherits from Table. You can then override required methods"""
    def __init__(self, parent=None, **kwargs):
        Table.__init__(self, parent, **kwargs)
        self.bind("<ButtonRelease-1>", self.drop_operator_menu)  # Bind left click release event

    def drop_operator_menu(self, event):
        self.endrow = self.get_row_clicked(event)
        self.endcol = self.get_col_clicked(event)
        df = self.model.df
        operators = ["=", "<=", ">="]
        finds = ["min", "max"]
        if (self.endrow == 0 and self.endcol == len(df.columns) - 1):
            x1, y1, x2, y2 = self.getCellCoords(self.endrow, len(df.columns) - 1)
            self.dropvar = StringVar()
            self.dropvar.set('')
            combobox = ttk.Combobox(self, textvariable=self.dropvar, values=finds)
            combobox.bind("<<ComboboxSelected>>", self.handleEntryMenu)
            col_width = self.cellwidth
            row_height = self.rowheight
            self.create_window(x1, y1,
                               width=col_width, height=row_height,
                               window=combobox, anchor='nw',
                               tag='entry')

        elif (self.endrow == len(df) - 1 and self.endcol < len(df.columns) - 2):
            col = self.endcol
            x1, y1, x2, y2 = self.getCellCoords(self.endrow, col)
            self.dropvar = StringVar()
            self.dropvar.set('')
            combobox = ttk.Combobox(self, textvariable=self.dropvar, values=[">=", "<=", "free"])
            combobox.bind("<<ComboboxSelected>>", self.handleEntryMenu)
            col_width = self.cellwidth
            row_height = self.rowheight
            self.create_window(x1, y1,
                                width=col_width, height=row_height,
                                window=combobox, anchor='nw',
                                tag='entry')

        elif (0 < self.endrow < len(df)-1 and self.endcol == len(df.columns) - 2):
            row = self.get_row_clicked(event)
            col = len(df.columns) - 2
            x1, y1, x2, y2 = self.getCellCoords(row, col)
            self.dropvar = StringVar()
            self.dropvar.set('')
            # Get options
            combobox = ttk.Combobox(self, textvariable=self.dropvar, values=operators)
            combobox.bind("<<ComboboxSelected>>", self.handleEntryMenu)
            col_width = self.cellwidth
            row_height = self.rowheight
            self.create_window(x1, y1,
                               width=col_width, height=row_height,
                               window=combobox, anchor='nw',
                               tag='entry')
        else:
            self.drawCellEntry(self.endrow, self.endcol)
            
    def drawCellEntry(self, row, col, text=None):

        h = self.rowheight
        model = self.model
        if row < 0 or row >= len(model.df) or col < 0 or col >= len(model.df.columns):
            return  # Kiểm tra xem có nằm ngoài DataFrame không

        text = model.getValueAt(row, col)

        if pd.isnull(text):
            text = ''

        x1, y1, x2, y2 = self.getCellCoords(row, col)
        w = x2 - x1
        self.cellentryvar = txtvar = StringVar()
        txtvar.set(text)

        self.cellentry = Entry(self.parentframe, width=20,
                            textvariable=txtvar,
                            takefocus=1,
                            font=self.thefont)
        self.cellentry.icursor(END)

        self.cellentry.bind('<Leave>', lambda x: self.handleCellEntry(row, col))
        self.cellentry.focus_set()
        self.entrywin = self.create_window(x1, y1,
                                            width=w, height=h,
                                            window=self.cellentry, anchor='nw',
                                            tag='entry')

    def handleEntryMenu(self, event):
        value = self.dropvar.get()
        self.delete('entry')
        row = self.endrow
        col = self.endcol
        self.model.setValueAt(value, row, col)
        self.redraw()
    
    def add_row(self):
        df = self.model.df
        new_row = pd.Series({col: "" for col in df.columns})
        df.loc[len(df)] = new_row
        self.updateModel(TableModel(df))  # Update the table model with the new DataFrame
        self.redraw()  # Redraw the table

    def add_column(self):
        df = self.model.df
        # Determine the index where to insert the new column
        col_index = len(df.columns) - 2
        new_col_name = f"x{col_index + 1}"
        df.insert(col_index, new_col_name, "")
        self.updateModel(TableModel(df))  # Update the table model with the new DataFrame
        self.redraw()  # Redraw the table

    def remove_row(self):
        df = self.model.df
        if len(df) > 3:
            df = df.drop(df.index[-1])  # Remove the last row
            self.updateModel(TableModel(df))
            self.redraw()

    def remove_column(self):
        df = self.model.df
        if len(df.columns) > 4:  # Ensure there are at least two columns
            df = df.drop(df.columns[-3], axis=1)  # Remove the second-to-last column
            self.updateModel(TableModel(df))
            self.redraw()
    def refresh(self):
        df = self.model.df
        last_row_index = len(df) - 1
        last_col_index = len(df.columns) - 1
        
        # Update specific cells
        df.iat[0, last_col_index - 1] = "||"
        df.iat[last_row_index, last_col_index] = None
        df.iat[last_row_index, last_col_index - 1] = None
    
        # Update the TableModel
        self.updateModel(TableModel(df))

    def get_dataframe(self):
        return self.model.df



class CreateInput(Frame):
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
            40.0, 342.0, 742.0, 344.0, fill="#EFEFEF", outline=""
        )
        self.canvas.create_text(
            40.0,
            33.0,
            anchor="nw",
            text="Create Problem Input",
            fill="#5E95FF",
            font=(FONT_BOLD, 26 * -1),
        )

        self.canvas.create_text(
            40.0,
            367.0,
            anchor="nw",
            text="Actions:",
            fill="#5E95FF",
            font=(FONT_BOLD, 26 * -1),
        )

        self.canvas.create_text(
            40.0,
            65.0,
            anchor="nw",
            text="Type your constrains and function",
            fill="#808080",
            font=("FONT", 16 * -1),
        )

        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        button_5 = Button(
            self,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command= self.save,
            relief="flat",
        )
        button_5.place(x=532.0, y=37.0, width=100.0, height=44.0)

        self.button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
        button_6 = Button(
            self,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("view"),
            relief="flat",
        )
        button_6.place(x=642.0, y=37.0, width=100.0, height=44.0)

        self.table_frame = Frame(self)
        self.table_frame.place(x=40, y=101, width=702, height=228) 

        self.table = CustomTable(self.table_frame, dataframe=df)
        self.table.show()

        # Add Row button
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))

        self.add_col_btn = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.table.add_column,
            relief="flat",
        )
        self.add_col_btn.place(x=181, y=359, width=160, height=48)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.add_row_btn = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.table.add_row,
            relief="flat",
        )
        self.add_row_btn.place(x=348, y=359, width=110, height=48)
        # Remove Row button
        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.remove_col_btn = Button(
            self,
            image=self.button_image_3,  # You can use a different image if you want
            borderwidth=0,
            highlightthickness=0,
            command=self.table.remove_column,
            relief="flat",
        )
        self.remove_col_btn.place(x=465, y=359, width=160, height=48)

        # Remove Column button
        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.remove_row_btn = Button(
            self,
            image=self.button_image_4,  # You can use a different image if you want
            borderwidth=0,
            highlightthickness=0,
            command=self.table.remove_row,
            relief="flat",
        )
        self.remove_row_btn.place(x=632, y=359, width=110, height=48)

    def is_valid(self, df):
        n_cols = len(df.columns)
        n_rows = len(df)
        op_cols = n_cols - 2 
        op_rows = n_rows -1
        skip_cells = [(0, n_cols - 1),(op_rows,n_cols-1),(op_rows,n_cols-2)]  


        for row in range(n_rows):
            for col in range(n_cols):
                if (row, col) in skip_cells:
                    continue  
                elif row == op_rows or col == op_cols:
                    if df.iat[row,col] == "":
                        return False
                else:
                    if pd.isnull(df.iat[row, col]) or df.iat[row, col] == "":
                        return False  
                    try:
                        float(df.iat[row, col])
                    except ValueError:
                        return False 
        return True 
    
    def save(self):
        self.table.refresh()
        df = self.table.get_dataframe()

        if self.is_valid(df):
            path = DATA_PATH / "input.csv"
            path.parent.mkdir(parents=True, exist_ok=True)  
            df.to_csv(path, index=False)
            messagebox.showinfo("Success", "Saved successfully.")
        else:
            messagebox.showerror("Error", "Contains invalid values.")
        self.parent.refresh_view(df)
        self.parent.parent.linear_programing_solver(df)