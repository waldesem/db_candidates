from tkinter import Toplevel, Label, Button, Frame, Text, ttk, messagebox
import sqlite3

# местонахождение базы данных
CONNECT = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\candidates.db'

# название столбцов таблицы кандидатов базы данных
SQL = ['id', 'staff', 'department', 'full_name', 'last_name', 'birthday', 'birth_place', 'country', 'series_passport',
       'number_passport', 'date_given', 'snils', 'inn', 'reg_address', 'live_address', 'phone', 'email', 'education',
       'check_work_place', 'check_passport', 'check_debt', 'check_bankruptcy', 'check_bki', 'check_affiliation',
       'check_internet', 'check_cronos', 'check_cross', 'resume', 'date_check', 'officer']

# русские названия столбцов таблицы кандидатов базы данных
COLS = ['id', 'Должность', 'Подразделение', 'Фамилия Имя Отчество', 'Предыдущее ФИО', 'Дата рождения',
        'Место рождения', 'Гражданство', 'Серия паспорта', 'Номер паспорта', 'Дата выдачи', 'СНИЛС', 'ИНН',
        'Адрес регистрации', 'Адрес проживания', 'Телефон', 'Электронная  почта', 'Образование',
        'Проверка по местам работы', 'Проверка паспорта', 'Проверка долгов', 'Проверка банкротства',
        'Проверка по БКИ', 'Проверка аффилированности', 'Проверка Internet', 'Проверка Сronos', 'Проверка Cros',
        'Результат', 'Дата проверки', 'Сотрудник']


class TopWindow(Toplevel):
    """Объявляем класс Window для работы с окном"""

    def __init__(self) -> None:
        super().__init__()
        self.title('База данных')
        self.geometry('640x560')
        self.columnconfigure(0, weight=1)
        self.option_add('*Dialog.msg.font', 'Arial 10')


class WinFrame(Frame):
    """Объявляем класс WinFrame для работы с фреймами"""

    def __init__(self, parent) -> None:
        super().__init__(parent)


class Database:
    """Объявляем класс Database для работы с базой данных"""

    def __init__(self, database, query, value):
        self.database = database
        self.query = query
        self.value = value

    # функция для передачи запроса в БД
    def insert_db(self):
        try:
            with sqlite3.connect(self.database, timeout=5.0) as con:
                cur = con.cursor()
                cur.execute(self.query, self.value)
                record_db = cur.fetchall()
        except sqlite3.Error as error:
            print('Ошибка', error)
        return record_db


# запустить окно редактирования базы данных
def update_db(selected_people):
    # связываем данные колонок SQl БД с их русским названием и данными, которые передаются из строки таблицы
    sql_col_dict = dict(zip(COLS, SQL))
    col_select = dict(zip(COLS, selected_people))

    # изменение записей в БД
    def change_value():
        query = f"UPDATE candidates SET '{sql_col_dict[idx]}' = ? where id = ?"
        value = tuple(map(str, [editor.get("1.0", "end").strip(), selected_people[0]]))
        response = Database(CONNECT, query, value)
        resp = response.insert_db()
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

    # старт окна изменения базы данных
    master = TopWindow()
    # создаем фрейм для размещения элементов
    frame_db = WinFrame(master)
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
    editor["yscrollcommand"] = ys.set

    # создаем кнопку для обновления  информации в БД
    frame_button = WinFrame(master)
    frame_button.grid(row=1, column=0, columnspan=2, rowspan=1, pady=10, padx=10)
    Button(frame_button, text="Обновить данные", command=change_value).grid(row=0, column=0)
