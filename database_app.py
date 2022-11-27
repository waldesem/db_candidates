import sqlite3
import subprocess
from tkinter import *
from tkinter import messagebox, ttk

from docx import Document

from change_db import update_db, CONNECT, COLS


class Window(Tk):
    """Объявляем класс Window для работы с окном"""

    def __init__(self) -> None:
        super().__init__()
        self.title('База данных')
        self.geometry('1020x840')
        self.columnconfigure(0, weight=1)
        self.option_add('*Dialog.msg.font', 'Arial 10')


class MainMenu:
    """Объявляем класс MainMenu для меню приложения"""

    def __init__(self, parent) -> None:
        self.parent = parent
        self.menu = Menu()
        self.menu.add_command(label='Настройки', command='settings', font=('Arial', 10))
        self.parent.config(menu=self.menu)


class WinFrame(Frame):
    """Объявляем класс WinFrame для работы с фреймами"""

    def __init__(self, parent) -> None:
        super().__init__(parent)


class ButtonActions:
    """Объявляем класс ButtonActions для событий кнопок"""

    @staticmethod
    # событие по нажатию кнопки  "Поиск" в БД записей по ФИО и дате рождения
    def db_search():
        # формируем запрос на поиск данных в БД
        db_search_query = "SELECT * FROM candidates WHERE full_name like ? and birthday like ?"
        db_search_value = tuple(map(str, [fio_search.get(), dr_search.get()]))
        # создаем экземпляр класса БД и передаем запрос
        search_db = Database(CONNECT, db_search_query, db_search_value)
        # удаляем записи из таблицы, получаем и вставляем новые через функци класса Database
        treeviewdb(search_db.response_db(), "Результат проверки", "Запись в БД не найдена")

    @staticmethod
    # событие по нажатию кнопки "Обновить данные" в окне таблицы
    def start_query():
        # формируем запрос на поиск данных в БД
        start_query_query = "SELECT * FROM candidates ORDER BY date_check DESC LIMIT 5"
        # создаем экземпляр класса БД
        query_db = Database(CONNECT, start_query_query, value='')
        # удаляем записи из таблицы, получаем и вставляем новые
        treeviewdb(query_db.response_db(), "Ошибка", "БД не подключена")

    @staticmethod
    # событие по нажатию кнопки "Выгрузить данные" из БД
    def take_info():
        file_query = '/home/semenenko/Загрузки/yourfile.docx'
        document = Document()
        # создаем таблицу Word
        table = document.add_table(rows=len(COLS), cols=2)
        table.style = 'Table Grid'
        for j in range(len(COLS)):
            table.rows[j].cells[0].text = COLS[j]
            table.rows[j].cells[1].text = selected_people.split('\n')[j]
        document.save(file_query)
        subprocess.call(["xdg-open", file_query])

    @staticmethod
    # событие по нажатию кнопки "Изменить данные" запись в БД
    def change_db():
        # вызов дочернего окна и передача переменной с выбранными данными
        update_db(selected_people.split('\n'))

    @staticmethod
    # событие по нажатию чекбокса "Включить ДР в поиск" запись в БД (не работает)
    def change_check_button():
        pass


class Database:
    """Объявляем класс Database для работы с базой данных"""

    def __init__(self, database, query, value):
        self.database = database
        self.query = query
        self.value = value

    # функция для передачи запроса в БД
    def response_db(self):
        try:
            with sqlite3.connect(self.database, timeout=5.0) as con:
                cur = con.cursor()
                cur.execute(self.query, self.value)
                record_db = cur.fetchall()
        except sqlite3.Error as error:
            print('Ошибка', error)
        return record_db


# функция удаления записи из таблицы treeview, получает и вставляет новые данные
def treeviewdb(function, title, message):
    try:
        # удаляем старые записи в окне таблицы
        for m in tree.get_children():
            tree.delete(m)
        # получаем данные в виде списка через SQL запрос 
        response = [h for h in function]
        # записываем найденные записи в окно
        for k in range(len(response)):
            tree.insert('', 'end', values=response[k])
    except IndexError:
        messagebox.showinfo(title=title, message=message)


# событие по нажатию строки в таблице базы данных и показ в виджете "Текст"
selected_people = ""


def item_selected(event):
    global selected_people
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        selected_people = '\n'.join(map(str, item["values"]))
    editor.delete("1.0", 'end')
    editor.insert("1.0", selected_people)
    return selected_people


# главное окно приложения
if __name__ == '__main__':
    # окно сообщений   
    master = Window()
    # меню приложения
    main_menu = MainMenu(master)

    # фрейм виджетов базы данных
    db_frame = WinFrame(master)
    db_frame.grid(row=0, column=0, columnspan=4, rowspan=1, pady=10, padx=10)
    for i in range(3):
        db_frame.columnconfigure(i, weight=1)

    # название видежетов на вкладке База данных
    txt_search = ['Фамилия Имя Отчество', 'Дата рождения']
    for i in range(len(txt_search)):
        Label(db_frame, text=f"{txt_search[i]}", font=('Arial', 10),
              width=30, anchor='w', padx=10, pady=10).grid(row=i, column=0)
    fio_search = StringVar()
    fio_search.set("Фамилия Имя Отчество")
    Entry(db_frame, textvariable=fio_search, width=40).grid(row=0, column=1)
    dr_search = StringVar()
    dr_search.set("ДД.ММ.ГГГГ")
    Entry(db_frame, textvariable=dr_search, width=40).grid(row=1, column=1)
    # чекбокс для включения в запрос даты рождения
    check_button = IntVar()
    enabled_check_button = ttk.Checkbutton(db_frame, text='Вкл.', variable=check_button,
                                           command='change_check_button')
    enabled_check_button.grid(padx=10, pady=10, row=1, column=2)
    # кнопки обновления информации в таблице и поиска в БД (в зависимости от чекбокса по ФИО или +ДР)
    Button(db_frame, text="Обновить данные", command=ButtonActions.start_query, width=20).grid(row=0, column=3)
    Button(db_frame, text="Поиск данных", command=ButtonActions.db_search, width=20).grid(row=1, column=3)

    # фрейм и таблица записей из БД
    frame_table = WinFrame(master)
    frame_table.grid(row=1, column=0, columnspan=4, rowspan=1, padx=10, pady=0, sticky="nsew")
    for i in range(3):
        frame_table.columnconfigure(i, weight=1)

    Label(frame_table, text='Результаты поиска:', font=('Arial', 11, 'bold'),
          width=30, anchor='center', padx=10, pady=10).grid(columnspan=3, row=0, column=0)
    # кнопки выгрузки информации в таблицу WORD и изменения в БД (окткрываетя отдельное окно)
    Button(frame_table, text="Выгрузить данные", command=ButtonActions.take_info).grid(row=3, column=0)
    Button(frame_table, text="Изменить данные", command=ButtonActions.change_db).grid(row=3, column=2)

    # настройки скролбаров
    x_scrollbar = Scrollbar(frame_table, orient='horizontal')
    x_scrollbar.grid(row=2, column=0, columnspan=3, sticky='E' + 'W')
    y_scrollbar = Scrollbar(frame_table, orient='vertical')
    y_scrollbar.grid(row=1, column=4, sticky='N' + 'S')

    # размещение столбцов, строк  и др.
    displaycolumns = [COLS[1]] + [COLS[3]] + [COLS[5]] + [COLS[-3]] + [COLS[-2]]
    tree = ttk.Treeview(frame_table, columns=COLS, height=5, show="headings",
                        displaycolumns=displaycolumns,
                        xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
    tree.grid(row=1, column=0, columnspan=3, sticky='E' + 'W')
    x_scrollbar['command'] = tree.xview
    y_scrollbar['command'] = tree.yview

    # настройка заголовков
    for col in tree['columns']:
        tree.heading(col, text=f"{col}", anchor='center')
        tree.column(col, anchor='center', width=160)

    # выбор строки в таблице результатов
    tree.bind("<<TreeviewSelect>>", item_selected)

    # фрейм и текстовое поле для выбранной записи из таблицы БД
    frame_select = WinFrame(master)
    frame_select.grid(row=2, column=0, columnspan=4, rowspan=1, pady=10, padx=20, sticky="nsew")
    for i in range(3):
        frame_select.columnconfigure(i, weight=1)

    Label(frame_select, text='Просмотр информации:', font=('Arial', 11, 'bold'),
          width=30, anchor='center', padx=10, pady=10).grid(columnspan=3, row=0, column=0)

    # параметры текстового поля
    editor = Text(frame_select, wrap="word")
    editor.grid(columnspan=3, column=0, row=1, sticky='nsew')

    #  скроллбары текстового поля
    ys = ttk.Scrollbar(frame_select, orient="vertical", command=editor.yview)
    ys.grid(column=4, row=1, sticky='ns')
    editor["yscrollcommand"] = ys.set

    # запуск главного окна
    master.mainloop()
