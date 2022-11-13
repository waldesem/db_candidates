from tkinter import Toplevel, Label, Button, Frame, Text, ttk, messagebox
import sqlite3

# CONNECT = '/home/semenenko/MyProjects/Python/Share_db_files/candidates.db'
CONNECT = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\candidates.db'

COLS = ['id', 'Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Предыдущее ФИО', 'Дата рождения',
        'Место рождения', 'Гражданство', 'Серия паспорта', 'Номер паспорта', 'Дата выдачи', 'СНИЛС', 'ИНН',
        'Адрес регистрации', 'Адрес проживания', 'Телефон', 'Электронная  почта', 'Образование',
        'Проверка по местам работы', 'Проверка паспорта', 'Проверка долгов', 'Проверка банкротства',
        'Проверка по БКИ', 'Проверка аффилированности', 'Проверка Internet', 'Проверка Сronos', 'Проверка Cros',
        'Доп. информация', 'Результат', 'Дата проверки', 'Сотрудник']

# название столбцов базы данных
SQL = ['id', 'staff', 'department', 'full_name', 'last_name', 'birthday', 'birth_place', 'country', 'series_passport',
       'number_passport', 'date_given', 'snils', 'inn', 'reg_address', 'live_address', 'phone', 'email', 'education',
       'check_work_place', 'check_passport', 'check_debt', 'check_bankruptcy', 'check_bki', 'check_affiliation',
       'check_internet', 'check_cronos', 'check_cross', 'check_rand_info', 'resume', 'date_check', 'officer']


# запрос в базу данных
def response_db(db, query, value):
    try:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query, value)
            if 'INSERT' in query:
                con.commit()
            record_db = cur.fetchall()
    except sqlite3.Error as error:
        print('Ошибка', error)
    return record_db


# запустить окно редактирования базы данных
def update_db(selected_people):
    # связываем данные колонок SQl БД с их русским названием и данными, которые передаются из выделенной строки таблицы
    sql_col_dict = dict(zip(COLS, SQL))
    col_select = dict(zip(COLS, selected_people))

    # изменение записей в БД
    def change_value():
        query = f"UPDATE candidates SET '{sql_col_dict[idx]}' = ? where id = ?"
        value = tuple([str(i) for i in [editor.get("1.0", "end").strip(), selected_people[0]]])
        resp = response_db(CONNECT, query, value)
        if len(resp):
            messagebox.showinfo(title="Ошибка", message="Проверьте данные", parent=master)
        else:
            messagebox.showinfo(title="Успех", message="Запись обновлена", parent=master)

    # получение данных из combobox
    def selected(event):
        global idx
        # получаем выбранный элемент в лейбле показываем его SQl поле, в текстовом - содержание строки.
        selection = combobox.get()
        for key in sql_col_dict:
            if key == selection:
                label["text"] = f"Вы выбрали изменить запись в колонке: {sql_col_dict[key]}"
                editor.delete("1.0", 'end')
                editor.insert("1.0", col_select[key])
                idx = key  # индекс для передачи в SQL запрос на изменение значения.
        return idx

    # старт окна базы данных
    master = Toplevel()
    master.title('База данных')
    master.geometry('760x640')
    master.columnconfigure(0, weight=1)

    # создаем фрейм для размещения элементов
    frame_db = Frame(master)
    frame_db.grid(row=0, column=0, columnspan=2, rowspan=1, pady=10, padx=10)

    # создаем динамический лейбл для информации
    label = Label(frame_db)
    label.grid(row=0, column=0, pady=10, padx=10)

    # создаем комбобокс
    combobox = ttk.Combobox(frame_db, values=COLS, state="readonly")
    combobox.grid(row=1, column=0, pady=10, padx=10)
    combobox.bind("<<ComboboxSelected>>", selected)

    # создаем текстовое поле
    editor = Text(frame_db, wrap="word")
    editor.grid(column=0, row=2, sticky='N' + 'S' + 'E' + 'W')

    # создаем  скроллбар
    ys = ttk.Scrollbar(frame_db, orient="vertical", command=editor.yview)
    ys.grid(column=1, row=2, sticky='N' + 'S')
    xs = ttk.Scrollbar(frame_db, orient="horizontal", command=editor.xview)
    xs.grid(column=0, row=3, sticky='E' + 'W')
    editor["yscrollcommand"] = ys.set
    editor["xscrollcommand"] = xs.set

    # создаем кнопку для обновления  информации в БД
    Button(frame_db, text="Обновить данные", command=change_value).grid(row=4, column=0)
