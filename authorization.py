from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,messagebox
import tkinter as tk
import sqlite3
import hashlib
from db_create import *
from gui_user import create_window_user
from gui_admin import create_window_admin
from register_app import *
ASSETS_PATH = Path(r"assets/frame0")

user_id = None

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
    
def check_credentials_in_db(username):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT Password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result

def get_user_id_from_db(username):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT usersID FROM users WHERE Username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def check_credentials():
    global user_id
    username  = username_entry.get()
    password = password_entry.get()
    credentials = check_credentials_in_db(username)
    if credentials:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == credentials[0]:
            messagebox.showinfo("Успех", "Авторизация успешна!")
            user_id = get_user_id_from_db(username)
            window.destroy()
            if username == "admin":
                create_window_admin()
            else:
                create_window_user(user_id)  
        else:
            messagebox.showerror("Ошибка", "Неверный пароль")
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден")


def main():
    global window
    window = tk.Tk()
    window.title("Авторизация")
    
    window.geometry("700x375")
    window.configure(bg = "#F0CEFF")
    global canvas
    
    canvas = Canvas(
    window,
    bg = "#F0CEFF",
    height = 375,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    
    global username_entry, password_entry, login_button
    canvas.create_text(
    374.0,
    43.0,
    anchor="nw",
    text="Логин",
    fill="#83338F",
    font=("Inter Italic", 21 * -1)
    )

    canvas.create_text(
        382.0,
        122.0,
        anchor="nw",
        text="Пароль",
        fill="#83338F",
        font=("Inter Italic", 21 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_log.png"))
    entry_bg_1 = canvas.create_image(
        532.5,
        90.0,
        image=entry_image_1
    )
    username_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    username_entry.place(
        x=413.0,
        y=70.0,
        width=239.0,
        height=38.0
    )

    password_label = PhotoImage(
        file=relative_to_assets("entry_pass.png"))
    password_label = canvas.create_image(
        532.5,
        169.0,
        image=password_label
    )
    password_entry= Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        show = "*"
    )
    password_entry.place(
        x=413.0,
        y=149.0,
        width=239.0,
        height=38.0
    )

    canvas.create_rectangle(
        0.0,
        11.0,
        355.0,
        397.0,
        fill="#FFFCA8",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        175.0,
        176.0,
        image=image_image_1
    )

    login_button_image = PhotoImage(
    file=relative_to_assets("button_log.png"))
    login_button = Button(
    image=login_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=check_credentials,
    relief="flat"
    )  
    login_button.place(
        x=413.0,
        y=237.0,
        width=239.0,
        height=34.0
    )

    button_image_reg = PhotoImage(
    file=relative_to_assets("button_reg.png"))
    button_reg = Button(
        image=button_image_reg,
        borderwidth=0,
        highlightthickness=0,
        command=on_login,
        relief="flat"
    )
    button_reg.place(
        x=411.0,
        y=286.0,
        width=241.0,
        height=34.0
    )
    create_tables()

    window.resizable(False, False)
    window.mainloop()
    
if __name__ == "__main__":
    main()
