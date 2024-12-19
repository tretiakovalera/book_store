
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from buttons_users import *
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_window_user(user_id):
    window = Tk()

    window.geometry("700x375")
    window.configure(bg = "#F0CEFF")


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
    canvas.create_text(
        20.0,
        30.0,
        anchor="nw",
        text="Личный кабинет",
        fill="#643881",
        font=("Inter", 20 * -1)
    )

    canvas.create_text(
        585.0,
        35.0,
        anchor="nw",
        text="Покупатель",
        fill="#643881",
        font=("Inter", 15 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1_user.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        # command=lambda: print(user_id),
        command=lambda: show_cart(user_id),
        relief="flat"
    )
    button_1.place(
        x=246.0,
        y=277.0,
        width=207.0,
        height=68.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2_user.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:remove_from_cart(user_id),
        relief="flat"
    )
    button_2.place(
        x=393.0,
        y=179.0,
        width=207.0,
        height=68.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3_user.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: search_book(user_id),
        relief="flat"
    )
    button_3.place(
        x=97.0,
        y=179.0,
        width=207.0,
        height=68.0
    )
    window.resizable(False, False)
    window.mainloop()

def main():
    create_window_user()

if __name__ == "__main__":
    main()