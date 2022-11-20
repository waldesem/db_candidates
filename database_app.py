import subprocess
from tkinter import *
from tkinter import messagebox, ttk

from docx import Document

from about_app import about_db_pro
from login_app import user_login
from change_db import response_db, update_db, CONNECT, COLS, REGISTRY

cols = COLS

# Список с таблицами базы данных
selector = ['Таблица кандидатов', 'Таблица обратной связи']
viewcolumns = [cols[1]] + [cols[3]] + [cols[5]] + [cols[-3]] + [cols[-2]]


# выбор таблицы БД из выпадающего списка
def select_item(event):
    global cols
    global viewcolumns
    # получаем выбранный элемент
    selection = combobox.get()
    if selection == selector[1]:
        cols = REGISTRY
        viewcolumns = [REGISTRY[1]] + [REGISTRY[2]] + [REGISTRY[3]] + [REGISTRY[4]] + [REGISTRY[9]] + [REGISTRY[10]]
    else:
        pass


# клик по кнопке поиск в БД записей по ФИО и дате рождения
def db_search():
    query = "SELECT * FROM candidates WHERE full_name like ? and birthday like ?"
    value = tuple(map(str, [fio_search.get(), dr_search.get()]))
    try:
        search = [h for h in response_db(CONNECT, query, value)]
        # удаляем старые записи в окне таблицы
        for m in tree.get_children():
            tree.delete(m)
        # записываем найденные записи
        for k in range(len(search)):
            tree.insert('', 'end', values=search[k])
    except IndexError:
        messagebox.showinfo(title="Результат проверки", message="Запись в БД не найдена")


# обновить данные в окне таблицы
def start_query():
    query = "SELECT * FROM candidates ORDER BY date_check DESC LIMIT 5"
    try:
        for h in tree.get_children():
            tree.delete(h)
        start_search = [j for j in response_db(CONNECT, query, value='')]
        for s in range(len(start_search)):
            tree.insert('', 'end', values=start_search[s])
    except IndexError:
        messagebox.showinfo(title="Ошибка", message="БД не подключена")


# выбор строки в таблице базы данных и показ в текстовом поле
selected_people = ""


def item_selected(event):
    global selected_people
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        selected_people = '\n'.join(map(str, item["values"]))
    editor.delete("1.0", 'end')
    editor.insert("1.0", selected_people)
    return selected_people


# клик по кнопке Выгрузка информации из БД
def take_info():
    file_query = '/home/semenenko/Загрузки/yourfile.docx'
    document = Document()
    # создаем таблицу Word
    table = document.add_table(rows=len(cols), cols=2)
    table.style = 'Table Grid'
    for j in range(len(cols)):
        table.rows[j].cells[0].text = cols[j]
        table.rows[j].cells[1].text = selected_people.split('\n')[j]
    document.save(file_query)
    subprocess.call(["xdg-open", file_query])


# клик по кнопке меню изменить запись в БД
def change_db():
    update_db(selected_people.split('\n'))


if __name__ == '__main__':
    master = Tk()
    master.title('База данных')
    master.geometry('1020x840')
    # окно сообщений
    master.option_add('*Dialog.msg.font', 'Arial 10')
    master.columnconfigure(0, weight=1)
    # master.rowconfigure(0, weight=1)

    main_menu = Menu()
    menu_label_lst = ['Войти в БД', 'Настройки', 'О программе']
    command_lst = [user_login, 'change_settings', about_db_pro]
    for n in range(len(command_lst)):
        main_menu.add_command(label=menu_label_lst[n], command=command_lst[n], font=('Arial', 10))
        master.config(menu=main_menu)

    # фрейм виджетов базы данных
    db_frame = Frame(master)
    db_frame.grid(row=0, column=0, columnspan=4, rowspan=1, pady=10, padx=10)
    for i in range(3):
        db_frame.columnconfigure(i, weight=1)

    # комбобокс выбора таблицы с данными
    Label(db_frame, text='Выбор таблицы', font=('Arial', 10),
          width=30, anchor='w', padx=10, pady=10).grid(row=2, column=0)
    combobox = ttk.Combobox(db_frame, values=selector, state="readonly", width=40)
    combobox.current(0)
    combobox.grid(row=2, column=1, pady=10, padx=10)
    combobox.bind("<<ComboboxSelected>>", select_item)
    Button(db_frame, text="Применить", command=lambda: master.update).grid(row=2, column=2)

    # создаем название видежетов на вкладке База данных
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
    Label(db_frame, text='Найти по условиям:', font=('Arial', 10),
          width=40, anchor='center', padx=10, pady=10).grid(row=0, column=2)
    Button(db_frame, text="Поиск", command=db_search).grid(row=1, column=2)
    Button(db_frame, text="Выгрузить данные", command=take_info).grid(row=0, column=3)
    Button(db_frame, text="Изменить данные", command=change_db).grid(row=1, column=3)
    Button(db_frame, text="Обновить данные", command=start_query).grid(row=2, column=3)

    # фрейм и таблица записей из БД
    frame_table = Frame(master)
    frame_table.grid(row=1, column=0, columnspan=4, rowspan=1, padx=10, pady=10, sticky="nsew")
    for i in range(3):
        frame_table.columnconfigure(i, weight=1)

    Label(frame_table, text='Результаты поиска:', font=('Arial', 11, 'bold'),
          width=30, anchor='center', padx=10, pady=10).grid(columnspan=3, row=0, column=0)

    # настройки скролбаров
    x_scrollbar = Scrollbar(frame_table, orient='horizontal')
    x_scrollbar.grid(row=2, column=0, columnspan=3, sticky='E' + 'W')
    y_scrollbar = Scrollbar(frame_table, orient='vertical')
    y_scrollbar.grid(row=1, column=4, sticky='N' + 'S')

    # размещение столбцов, строк  и др.
    tree = ttk.Treeview(frame_table, columns=cols, height=5, show="headings",
                        displaycolumns=viewcolumns,
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
    frame_select = Frame(master)
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
