from tkinter import Toplevel, Frame, Text, Scrollbar, Button
from tkinter import ttk

from backend import *


class ChildWin:
    """Class gui elements"""

    def __init__(self):  # create window
        self.root = Toplevel()
        self.root.title('Изменить базу данных')
        self.root.geometry('760x580')
        self.root.resizable(False, False)
        self.child_win()

    def create_frame(self, **kwargs):  # create frame
        self.frame = Frame(self.root)
        self.frame.grid(kwargs)
        return self.frame

    def child_win(self):
        self.combo_frame = self.create_frame(row=0, column=0, columnspan=2, rowspan=1, pady=10, padx=10)
        self.txt = Text(self.combo_frame)
        self.txt.grid(column=0, row=1, sticky='nsew')
        self.combobox = ttk.Combobox(self.combo_frame, values=COLS, state="readonly")
        self.combobox.grid(row=0, column=0, pady=10, padx=10)
        self.combobox.bind("<<ComboboxSelected>>", lambda event: text_edit(self.txt, Selection.selected[Selection.index]))
        self.scroll = Scrollbar(self.combo_frame, orient="vertical", command=self.txt.yview)
        self.scroll.grid(column=1, row=1, sticky='ns')
        self.txt["yscrollcommand"] = self.scroll.set
        self.button_frame = self.create_frame(row=1, column=0, columnspan=2, rowspan=1, pady=10, padx=10)
        Button(self.button_frame, text="Обновить", command=lambda: change(self.root, self.txt)).grid(row=0, column=0)


def child_app():   
    ChildWin() # secondary window


