import sqlite3
from tkinter import messagebox as mb

from docx import Document

# CONNECT = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\candidates.db' # база данных
CONNECT = '/home/semenenko/MyProjects/Python/Share_db_files/candidates.db'
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

class Development:
    """Class backend operations"""
    
    select = ''
    index : int

    def __init__(self):
        self.tree = None
        self.combobox = None

    def tree_select(self, tree):  # получение списка по нажатию строки в таблице базы данных
        self.tree = tree
        Development.select = self.tree.item(self.tree.selection())["values"]
        return Development.select

    def combo_select(self, combobox): # получение данных из combobox
        self.combobox = combobox
        Development.index = COLS.index(self.combobox.get())
        return Development.index

    @classmethod
    def tree_view_db(cls, function, tree):   # удаление записи из таблицы treeview, вставляет новые данные
        [tree.delete(m) for m in tree.get_children()]  # удаляем старые записи в окне таблицы
        response = [h for h in function]    # получаем данные в виде списка через SQL запрос 
        [tree.insert('', 'end', values=response[k]) for k in range(len(response))]  # вставляем записи в таблицу

    @staticmethod
    def db_search(tree, fio, bth, check):    # событие по нажатию кнопки  "Поиск" в БД
        if check.get():
            query = "SELECT "f'{", ".join(SQL)}' " FROM candidates WHERE full_name like ? and birthday like ?"
            value = tuple(map(str, [fio.get(), bth.get()]))
        else:
            query = "SELECT "f'{", ".join(SQL)}' " FROM candidates WHERE full_name like ?"
            value = tuple(map(str, [fio.get()]))
        Development.tree_view_db(Development.response_db(CONNECT, query, value), tree)
    
    @staticmethod
    def change(master, editor): # событие по нажатию кнопки "Изменить данные" в дочернем окне
        change_query = f"UPDATE candidates SET '{SQL[Development.index]}' = ? where id = ?"
        value = tuple(map(str, [editor.get("1.0", "end").strip(), Development.select[0]]))
        resp = Development.response_db(CONNECT, change_query, value)
        if len(resp):
            mb.showinfo(title="Ошибка", message="Проверьте данные", parent=master)
        else:
            mb.showinfo(title="Успех", message="Запись обновлена", parent=master)

    @staticmethod
    def download():    # событие по нажатию кнопки "Выгрузить данные" из БД
        file_query = '/home/semenenko/Загрузки/yourfile.docx'
        document = Document()    # создаем таблицу Word
        table = document.add_table(rows=len(COLS), cols=2)
        table.style = 'Table Grid'
        for j in range(len(COLS)):
            table.rows[j].cells[0].text = COLS[j]
            table.rows[j].cells[1].text = str(Development.select[j])
        document.save(file_query)

    @classmethod
    def response_db(cls, database, query, value):    # функция для передачи запроса в БД
        try:
            with sqlite3.connect(database, timeout=5.0) as con:
                cur = con.cursor()
                cur.execute(query, value)
                record_db = cur.fetchall()
        except sqlite3.Error:
                mb.showinfo(title='Ошибка', message='Ошибка БД')
        return record_db

    @staticmethod
    def text_edit(editor, text): # показ в виджете "Текст"
        editor.delete("1.0", 'end')
        editor.insert("1.0", text)
