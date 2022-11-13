import subprocess
from tkinter import *
from tkinter import messagebox, ttk

from docx import Document

from about_app import about_db_pro
from login_app import user_login
from change_db import response_db, update_db, CONNECT, COLS


# клик по кнопке поиск в БД записей по ФИО и дате рождения
def db_search():
    query = "SELECT * FROM candidates WHERE full_name like ? and birthday like ?"
    value = tuple([str(j) for j in [fio_search.get(), dr_search.get()]])
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


# клик по кнопке поиск в БД записей по SQL-запросу
def db_search_where():
    query = (str(sql_search.get()))
    try:
        search = [h for h in response_db(CONNECT, query, value='')]
        # удаляем старые записи в окне таблицы
        for j in tree.get_children():
            tree.delete(j)
        # записываем найденные записи
        for k in range(len(search)):
            tree.insert('', 'end', values=search[k])
    except IndexError:
        messagebox.showinfo(title="Результат проверки", message="Запись в БД не найдена")


# общий запрос в БД перед стартом программы
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
    table = document.add_table(rows=len(COLS), cols=2)
    table.style = 'Table Grid'
    for j in range(len(COLS)):
        table.rows[j].cells[0].text = COLS[j]
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
    command_lst = [user_login, 'settings', about_db_pro]
    for n in range(len(command_lst)):
        main_menu.add_command(label=menu_label_lst[n], command=command_lst[n], font=('Arial', 10))
        master.config(menu=main_menu)

    # фрейм виджетов базы данных
    db_frame = Frame(master)
    db_frame.grid(row=0, column=0, columnspan=4, rowspan=1, pady=10, padx=10)
    for i in range(3):
        db_frame.columnconfigure(i, weight=1)

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
    Label(db_frame, text='Найти по условию', font=('Arial', 10),
          width=40, anchor='center', padx=10, pady=10).grid(row=0, column=2)
    Button(db_frame, text="Поиск", command=db_search).grid(row=1, column=2)
    # поиск по sql запросу
    Label(db_frame, text='Запрос в формате SQL', font=('Arial', 10),
          width=30, anchor='w', padx=10, pady=10).grid(row=2, column=0)
    sql_search = StringVar()
    sql_search.set("Select * from candidates where...")
    Entry(db_frame, textvariable=sql_search, width=40).grid(row=2, column=1)
    Button(db_frame, text="SQL запрос", command=db_search_where).grid(row=2, column=2)
    Label(db_frame, text='Результаты поиска', font=('Arial', 10),
          width=30, anchor='w', padx=10, pady=10).grid(row=3, column=1)
    Button(db_frame, text="Выгрузить данные", command=take_info).grid(row=0, column=3)
    Button(db_frame, text="Изменить данные", command=change_db).grid(row=1, column=3)
    Button(db_frame, text="Обновить данные", command=start_query).grid(row=2, column=3)

    # фрейм и таблица записей из БД
    frame_table = Frame(master)
    frame_table.grid(row=4, column=0, columnspan=4, rowspan=1, pady=10, padx=20)
    for col in range(len(COLS)):
        frame_table.columnconfigure(col, weight=1)

    # настройки скролбаров
    x_scrollbar = Scrollbar(frame_table, orient='horizontal')
    x_scrollbar.grid(row=1, column=0, columnspan=3, sticky='E' + 'W')
    y_scrollbar = Scrollbar(frame_table, orient='vertical')
    y_scrollbar.grid(row=0, column=3, sticky='N' + 'S')

    # размещение столбцов, строк  и др.
    tree = ttk.Treeview(frame_table, columns=COLS, height=5, show="headings",
                        displaycolumns=[COLS[1]] + [COLS[3]] + [COLS[5]] + [COLS[-3]] + [COLS[-2]],
                        xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
    tree.grid(row=0, column=0, columnspan=3, sticky='E' + 'W')
    x_scrollbar['command'] = tree.xview
    y_scrollbar['command'] = tree.yview

    # настройка заголовков
    for col in tree['columns']:
        tree.heading(col, text=f"{col}", anchor='center')
        tree.column(col, anchor='center', width=160)

    # загрузка записей по умолчанию на старте программы
    # search_query = start_query()
    # for i in range(len(search_query)):
    #     tree.insert('', 'end', values=search_query[i])

    # выбор строки в таблице результатов
    tree.bind("<<TreeviewSelect>>", item_selected)

    # фрейм и текстовое поле для выбранной записи из таблицы БД
    frame_select = Frame(master)
    frame_select.grid(row=5, column=0, columnspan=4, rowspan=1, pady=10, padx=20)

    # параметры текстового поля
    editor = Text(frame_select, height=24, wrap="word")
    editor.grid(column=0, row=0, sticky='E' + 'W')

    #  скроллбары текстового поля
    ys = ttk.Scrollbar(frame_select, orient="vertical", command=editor.yview)
    ys.grid(column=3, row=0, sticky='N' + 'S')
    xs = ttk.Scrollbar(frame_select, orient="horizontal", command=editor.xview)
    xs.grid(column=0, row=1, sticky='E' + 'W')
    editor["yscrollcommand"] = ys.set
    editor["xscrollcommand"] = xs.set

    # запуск главного окна
    master.mainloop()
