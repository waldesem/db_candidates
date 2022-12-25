from tkinter import *
from tkinter import ttk

from backend import *


class ChildWin:
    """Class gui elements"""

    def __init__(self, window):  # create window
        self.root = window
        self.root.title('Изменить базу данных')
        self.root.geometry('760x580')
        self.root.resizable(False, False)

    def create_frame(self, **kwargs):  # create frame
        self.frame = Frame(self.root)
        self.frame.grid(kwargs)
        return self.frame

    def create_yscrollbar (self, frame, ont, com, **kwargs):
        self.scroll = Scrollbar(frame, orient=ont, command=com)
        self.scroll.grid(kwargs)
        return self.scroll

    def sroll_text_edit(self, frame, **kwargs):
        self.txt = Text(frame)
        self.txt.grid(kwargs)
        return self.txt

    def child_app(self):    # secondary window
        events_cld = Development() # exemplar of class Development from events_app module
        # создаем фреймы
        frame_cdb = self.create_frame(row=0, column=0, columnspan=2, rowspan=1, pady=10, padx=10)
        frame_set = self.create_frame(row=1, column=0, columnspan=2, rowspan=1, pady=10, padx=10)
        # виджеты-кнопки
        Button(frame_set, text="Обновить", command=lambda: events_cld.change(self.root, txt_chd)).grid(row=0, column=0)
        # создаем комбобокс
        cbox = ttk.Combobox(frame_cdb, values=COLS, state="readonly")
        cbox.grid(row=1, column=0, pady=10, padx=10) # команда ниже выбирает из меню cbox и создает текст
        cbox.bind("<<ComboboxSelected>>", lambda event:
        Development.text_edit(txt_chd, events_cld.select[events_cld.combo_select(cbox)]))
        # создаем текстовое поле
        txt_chd = self.sroll_text_edit(frame_cdb, column=0, row=2, sticky='N' + 'S' + 'E' + 'W')
        scrollbar = self.create_yscrollbar(frame_cdb, "vertical", txt_chd.yview, column=1, row=2, sticky='ns')
        txt_chd["yscrollcommand"] = scrollbar.set

def change_app ():
    window = Toplevel()
    child = ChildWin(window)
    child.child_app()
