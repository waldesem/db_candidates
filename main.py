from tkinter import *
from tkinter import ttk

from backend import *
from changer import change_app


class Windows:
    """Class gui elements"""
    
    selector = Development.select
 
    def __init__(self, window):    # create window
        self.root = window
        self.root.title('База данных')
        self.root.geometry('1080x860')
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.main_app()

    def create_frame(self, cols, num, **kwargs):    # create frame
        self.frame = Frame(self.root)
        self.frame.grid(kwargs)
        [self.frame.columnconfigure(col, weight=num) for col in range(cols)]
        return self.frame

    def tree_view(self, frame, scroll):   # create treeview
        self.tree = ttk.Treeview(frame, columns=COLS, height=5, show="headings",
                           displaycolumns=[COLS[1], COLS[3], COLS[5], COLS[-3], COLS[-2]], yscrollcommand=scroll)
        self.tree.grid(row=1, column=0, columnspan=3, sticky='E' + 'W')
        for col in self.tree['columns']:    # настройка заголовков
            self.tree.heading(col, text=f"{col}", anchor='center')
            self.tree.column(col, anchor='center', width=160)
        scroll['command'] = self.tree.yview
        return self.tree

    def sroll_text_edit(self, frame, **kwargs):
        self.txt = Text(frame)
        self.txt.grid(kwargs)
        self.txt["yscrollcommand"] = self.scroll.set
        return self.txt

    def create_yscrollbar (self, frame, ont, com, **kwargs):
        self.scroll = Scrollbar(frame, orient=ont, command=com)
        self.scroll.grid(kwargs)
        return self.scroll

    def create_entry(self, frame, text, wt, **kwargs): # create entries
        name = StringVar()
        name.set(text)
        self.entry = Entry(frame, textvariable=name, width=wt)
        self.entry.grid(kwargs)
        return self.entry

    def main_app(self): # main GUI
        events = Development() # exemplar of class Development from backend module
        frame_db, frame_tbl, frame_edt = [self.create_frame(3, 1, row=i, column=0, columnspan=4, rowspan=1,
                                                            pady=10, padx=10, sticky="nsew") for i in range(3)]
        lbl = ['Фамилия Имя Отчество', 'Дата рождения', 'Результаты поиска:', 'Просмотр информации:']   # надписи
        Label(frame_db, text=lbl[0], width=30, anchor='w', padx=10, pady=10).grid(row=0, column=0)
        Label(frame_db, text=lbl[1], width=30, anchor='w', padx=10, pady=10).grid(row=1, column=0)
        Label(frame_tbl,text=lbl[2], width=30, anchor='center', padx=10, pady=10).grid(row=0, column=0, columnspan=3)
        Label(frame_edt, text=lbl[3], width=30, anchor='center', padx=10,
                            pady=10).grid(row=1, column=0, columnspan=3)
        # виджеты-поля ввода
        fio_entry = self.create_entry(frame_db, "Фамилия Имя Отчество", 40, row=0, column=1)
        bth_entry = self.create_entry(frame_db, "ДД.ММ.ГГГГ", 40, row=1, column=1)
        # виджеты-кнопки
        Button(frame_db, text="Поиск", command=lambda: Development.db_search(db_tree, fio_entry, bth_entry, enabled),
               width=20).grid(row=0, column=3)
        Button(frame_db, text="Изменить", command=lambda: change_app(), width=20).grid(row=1, column=3)
        Button(frame_edt, text="Выгрузить", command=Development.download, width=20).grid(row=0, column=2)
        # чекбокс для включения в запрос даты рождения
        enabled=IntVar()
        ttk.Checkbutton(frame_db, text='Вкл.', variable=enabled).grid(padx=10, pady=10, row=1, column=2)
        # Treeview
        tvy_scroll = self.create_yscrollbar(frame_tbl, 'vertical', None, row=1, column=4, sticky='N' + 'S')
        db_tree = self.tree_view(frame_tbl, tvy_scroll)
        # выбор строки в таблице
        db_tree.bind("<<TreeviewSelect>>", lambda event:
                    Development.text_edit(txt_main, '\n'.join(map(str, events.tree_select(db_tree)))))
        # текстовое поле
        txt_main = self.sroll_text_edit(frame_edt, columnspan=3, column=0, row=2, sticky='nsew')
        self.create_yscrollbar(frame_edt, "vertical", txt_main.yview, row=2, column=4, sticky='ns')


if __name__ == '__main__':
    master = Tk()
    parent = Windows(master)
    master.mainloop()    # запуск главного окна
