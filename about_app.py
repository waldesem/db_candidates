from tkinter import Toplevel, Label


def about_db_pro():
    master = Toplevel()
    master.title('О программе')
    master.geometry('360x240')
    about_txt = ['Программа "БД - Кадровая безопасность"', 'Разработка: wsemenenko@gmail.com',
                 'https://github.com/waldesem', 'GNU General Public License, version 3', '2022 г.']
    for i in range(len(about_txt)):
        Label(master, text=f"{about_txt[i]}", font=('Arial', 10),
              width=45, anchor='center', padx=5, pady=5).grid(row=i, column=0)
