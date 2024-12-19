from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from buttons_adm import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_window_admin():
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
        562.0,
        19.0,
        anchor="nw",
        text="Администратор",
        fill="#643881",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        16.999999999999943,
        14.0,
        anchor="nw",
        text="Личный кабинет",
        fill="#643881",
        font=("Inter", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1_adm.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=create_order_window,
        relief="flat"
    )
    button_1.place(
    x=379.99999999999994,
    y=220.0,
    width=207.0,
    height=68.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2_adm.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=show_all_customers,
        relief="flat"
    )
    button_2.place(
    x=120.99999999999994,
    y=220.0,
    width=207.0,
    height=68.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3_adm.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=delete_book,
        relief="flat"
    )
    button_3.place(
    x=482.99999999999994,
    y=125.0,
    width=207.0,
    height=68.0
    )
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4_adm.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=open_add_book_window,
        relief="flat"
    )
    button_4.place(
    x=16.999999999999943,
    y=125.0,
    width=207.0,
    height=68.0
    )
    
    button_image_5 = PhotoImage(
    file=relative_to_assets("button_5_adm.png"))
    button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=display_book_catalog,
    relief="flat"
    )
    button_5.place(
    x=249.99999999999994,
    y=125.0,
    width=207.0,
    height=68.0
    )
    window.resizable(False, False)
    window.mainloop()
    
    
def main():
    create_window_admin()

if __name__ == "__main__":
    main()