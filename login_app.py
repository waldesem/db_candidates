from tkinter import Toplevel, StringVar, Label, Entry, Button


# login button check
def check_login():
    pass


# login window
def user_login():
    master = Toplevel()
    master.title('Вход в базу данных')
    master.geometry('360x120')
    # #username label and text entry box
    Label(master, text="Пользователь", font=('Arial', 10),
          width=15, anchor='w', padx=10, pady=10).grid(row=0, column=0)
    username = StringVar()
    Entry(master, textvariable=username, width=20).grid(row=0, column=1)
    # password label and password entry box
    Label(master, text="Пароль", font=('Arial', 10),
          width=15, anchor='w', padx=10, pady=10).grid(row=1, column=0)
    password = StringVar()
    Entry(master, textvariable=password, width=20, show='*').grid(row=1, column=1)
    # login/cancel button
    Button(master, text="Вход", command=check_login).grid(row=2, column=0)
    Button(master, text="Отмена", command=master.destroy).grid(row=2, column=1)
