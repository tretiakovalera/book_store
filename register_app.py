import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


def add_employee(FirstName,LastName,username,password,Phone,Email):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute("SELECT * FROM users WHERE Username=?", (username,))
    if c.fetchone():
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
        conn.close()
        return False

    c.execute("INSERT INTO users (FirstName,LastName,Username,Password,Phone,Email) VALUES (?,?,?,?,?,?)", 
              (FirstName,LastName,username,hashed_password,Phone,Email ))
    conn.commit()
    conn.close()
    messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован.")
    return True

def on_register( entry_first_name,entry_last_name, entry_username,entry_password,entry_phone,entry_email):
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    username = entry_username.get()
    password = entry_password.get()
    phone = entry_phone.get()
    email = entry_email.get()
    add_employee(first_name, last_name, username, password, phone, email)

def on_login():
    root = tk.Tk()
    root.title("Регистрация сотрудника")
    root.geometry("400x400")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    label_first_name = tk.Label(main_frame, text="Имя:")
    label_first_name.grid(row=0, column=0, padx=5, pady=5)
    entry_first_name = tk.Entry(main_frame)
    entry_first_name.grid(row=0, column=1, padx=5, pady=5)

    label_last_name = tk.Label(main_frame, text="Фамилия:")
    label_last_name.grid(row=1, column=0, padx=5, pady=5)
    entry_last_name = tk.Entry(main_frame)
    entry_last_name.grid(row=1, column=1, padx=5, pady=5)

    label_username = tk.Label(main_frame, text="Имя пользователя:")
    label_username.grid(row=2, column=0, padx=5, pady=5)
    entry_username = tk.Entry(main_frame)
    entry_username.grid(row=2, column=1, padx=5, pady=5)

    label_password = tk.Label(main_frame, text="Пароль:")
    label_password.grid(row=3, column=0, padx=5, pady=5)
    entry_password = tk.Entry(main_frame, show="*")
    entry_password.grid(row=3, column=1, padx=5, pady=5)

    label_phone = tk.Label(main_frame, text="Телефон:")
    label_phone.grid(row=4, column=0, padx=5, pady=5)
    entry_phone = tk.Entry(main_frame)
    entry_phone.grid(row=4, column=1, padx=5, pady=5)

    label_email = tk.Label(main_frame, text="Email:")
    label_email.grid(row=5, column=0, padx=5, pady=5)
    entry_email = tk.Entry(main_frame)
    entry_email.grid(row=5, column=1, padx=5, pady=5)

    button_register = tk.Button(main_frame, text="Зарегистрировать", command=lambda: on_register(
    entry_first_name,
    entry_last_name,
    entry_username,
    entry_password,
    entry_phone,
    entry_email
    ))
    button_register.grid(row=6, column=0, columnspan=2, padx=5, pady=20)

    root.mainloop()