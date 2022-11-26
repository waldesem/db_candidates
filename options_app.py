from tkinter import *
from tkinter import ttk


class TopWindow(Toplevel):
    """Объявляем класс Window для работы с окном"""

    def __init__(self) -> None:
        super().__init__()
        self.title('Настройки')
        self.geometry('480x120')
        self.columnconfigure(0, weight=1)
        self.option_add('*Dialog.msg.font', 'Arial 10')


class WinFrame(Frame):
    """Объявляем класс WinFrame для работы с фреймами"""

    def __init__(self, parent) -> None:
        super().__init__(parent)


def settings():
    
    selector = ['Таблица кандидатов', 'Таблица обратной связи']
    
    
    # выбор таблицы БД из выпадающего списка
    def select_item(event):
        # получаем выбранный элемент
        selection = combobox.get()
        return selection


    # старт окна изменения базы данных
    master = TopWindow()
    # создаем фрейм для размещения элементов
    frame_opt = WinFrame(master)
    frame_opt.grid(row=0, column=0, columnspan=3, rowspan=1, pady=10, padx=10)

    # комбобокс выбора таблицы с данными
    Label(frame_opt, text='Выбор таблицы', font=('Arial', 10), anchor='w', padx=10, pady=10).grid(row=0, column=0)
    combobox = ttk.Combobox(frame_opt, values=selector, state="readonly", width=37)
    combobox.current(0)
    combobox.grid(row=0, column=1, pady=10, padx=10)
    combobox.bind("<<ComboboxSelected>>", select_item)
    Button(frame_opt, text="Применить", command='command').grid(row=0, column=2)

    