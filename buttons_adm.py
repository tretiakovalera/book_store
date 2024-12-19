import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from db_create import *
def open_add_book_window():
    # Создаем новое окно для добавления книги
    add_book_window = tk.Toplevel()
    add_book_window.title("Добавить книгу")

    # Создаем поля ввода
    tk.Label(add_book_window, text="Название книги:").grid(row=0, column=0)
    title_entry = tk.Entry(add_book_window)
    title_entry.grid(row=0, column=1)

    tk.Label(add_book_window, text="Автор:").grid(row=1, column=0)
    author_entry = tk.Entry(add_book_window)
    author_entry.grid(row=1, column=1)

    tk.Label(add_book_window, text="Цена:").grid(row=2, column=0)
    price_entry = tk.Entry(add_book_window)
    price_entry.grid(row=2, column=1)

    tk.Label(add_book_window, text="Количество на складе:").grid(row=3, column=0)
    stock_entry = tk.Entry(add_book_window)
    stock_entry.grid(row=3, column=1)

    tk.Label(add_book_window, text="Описание:").grid(row=4, column=0)
    description_entry = tk.Entry(add_book_window)
    description_entry.grid(row=4, column=1)

    # Функция для обработки добавления книги
    def submit_book():
        title = title_entry.get()
        author = author_entry.get()
        try:
            price = float(price_entry.get())
            stock = int(stock_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения для цены и количества.")
            return
        description = description_entry.get()

        add_book(title, author, price, stock, description)
        add_book_window.destroy()  # Закрываем окно после добавления книги

    # Кнопка для добавления книги
    submit_button = tk.Button(add_book_window, text="Добавить книгу", command=submit_book)
    submit_button.grid(row=6, columnspan=2)

def delete_book():
    # Получаем список всех книг из ассортимента
    conn = sqlite3.connect('book_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM books")
    books = cursor.fetchall()
    conn.close()

    if not books:
        messagebox.showinfo("Ассортимент пуст", "В ассортименте нет книг.")
        return

    # Формируем список названий книг
    book_titles = [book[0] for book in books]
    book_list = "\n".join(book_titles)

    # Запрашиваем у пользователя название книги для удаления
    book_to_delete = simpledialog.askstring("Удаление книги", f"Выберите книгу для удаления:\n{book_list}")

    if book_to_delete:
        try:
            conn = sqlite3.connect('book_store.db')
            cursor = conn.cursor()
            # Удаляем книгу из ассортимента по названию
            cursor.execute("DELETE FROM books WHERE title = ?", (book_to_delete,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Успех", "Книга успешно удалена из ассортимента.")
            else:
                messagebox.showinfo("Информация", "Книга с таким названием не найдена в ассортименте.")
        
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        
        finally:
            conn.close()  # Закрываем соединение с базой данных

def show_all_customers():
    # Получаем список всех пользователей из таблицы users
    conn = sqlite3.connect('book_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    customers = cursor.fetchall()
    conn.close()

    if not customers:
        messagebox.showinfo("Покупатели", "В базе данных нет покупателей.")
        return

    # Создаем новое окно для отображения информации о покупателях
    window = tk.Toplevel()
    window.title("Информация о покупателях")
    window.geometry("400x400")
    window.configure(bg="#F0CEFF")

    # Создаем заголовки
    header_frame = tk.Frame(window, bg="#643881")
    header_frame.pack(fill=tk.X)

    tk.Label(header_frame, text="ID", bg="#643881", fg="white", font=("Inter", 8, "bold")).grid(row=0, column=0, padx=4, pady=5)
    tk.Label(header_frame, text="Имя", bg="#643881", fg="white", font=("Inter", 8, "bold")).grid(row=0, column=1, padx=8, pady=5)
    tk.Label(header_frame, text="Фамилия", bg="#643881", fg="white", font=("Inter", 8, "bold")).grid(row=0, column=2, padx=8, pady=5)
    tk.Label(header_frame, text="Имя пользователя", bg="#643881", fg="white", font=("Inter", 8, "bold")).grid(row=0, column=3, padx=8, pady=5)
    tk.Label(header_frame, text="Телефон", bg="#643881", fg="white", font=("Inter", 8, "bold")).grid(row=0, column=4, padx=4, pady=8)
    tk.Label(header_frame, text="Email", bg="#643881", fg="white", font=("Inter", 8, "bold")).grid(row=0, column=5, padx=4, pady=8)

    # Создаем фрейм для прокрутки
    scroll_frame = tk.Frame(window)
    scroll_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(scroll_frame, bg="#F0CEFF")
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#F0CEFF")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Заполняем данными
    for index, customer in enumerate(customers):
        row_index = index + 1
        tk.Label(scrollable_frame, text=customer[0], bg="#F0CEFF", font=("Inter", 10)).grid(row=index, column=0, padx=10, pady=5)
        tk.Label(scrollable_frame, text=customer[1], bg="#F0CEFF", font=("Inter", 10)).grid(row=index, column=1, padx=10, pady=5)
        tk.Label(scrollable_frame, text=customer[2], bg="#F0CEFF", font=("Inter", 10)).grid(row=index, column=2, padx=10, pady=5)
        tk.Label(scrollable_frame, text=customer[3], bg="#F0CEFF", font=("Inter", 10)).grid(row=index, column=3, padx=10, pady=5)
        tk.Label(scrollable_frame, text=customer[5], bg="#F0CEFF", font=("Inter", 10)).grid(row=index, column=4, padx=10, pady=5)
        tk.Label(scrollable_frame, text=customer[6], bg="#F0CEFF", font=("Inter", 10)).grid(row=index, column=5, padx=10, pady=5)

    # Упаковываем элементы
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    

def fetch_orders():
    try:
        conn = sqlite3.connect('book_store.db')
        cursor = conn.cursor()
        
        # Запрос для получения информации о заказах
        query = '''
        SELECT o.order_id, u.FirstName, u.LastName, o.order_date, o.total_amount, o.status
        FROM orders o
        JOIN users u ON o.user_id = u.usersID
        '''
        
        cursor.execute(query)
        orders = cursor.fetchall()
        if not orders:
            messagebox.showinfo("Информация", "Нет заказов для отображения.")
        
        return orders
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    finally:
        conn.close()

def show_orders(tree):
    # Очистка предыдущих данных в таблице заказов
    for row in tree.get_children():
        tree.delete(row)
    
    # Получение заказов из базы данных
    orders = fetch_orders()
    
    # Заполнение таблицы заказов
    for order in orders:
        tree.insert("", "end", values=order)
def fetch_order_items(order_id):
    try:
        conn = sqlite3.connect('book_store.db')
        cursor = conn.cursor()
        
        # Запрос для получения информации о книгах в заказе
        query = '''
        SELECT b.title, b.author, oi.quantity, oi.price
        FROM order_items oi
        JOIN books b ON oi.book_id = b.book_id
        WHERE oi.order_id = ?
        '''
        
        cursor.execute(query, (order_id,))
        order_items = cursor.fetchall()
        
        return order_items
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    finally:
        conn.close()
        
def show_order_details(order_id):
    order_items = fetch_order_items(order_id)
    
    # Создаем новое окно для отображения деталей заказа
    details_window = tk.Toplevel()
    details_window.title(f"Детали заказа {order_id}")

    # Создание таблицы для книг в заказе
    tree = ttk.Treeview(details_window, columns=("Название", "Автор", "Количество", "Цена"), show="headings")
    tree.heading("Название", text="Название")
    tree.heading("Автор", text="Автор")
    tree.heading("Количество", text="Количество")
    tree.heading("Цена", text="Цена")
    tree.pack(side="left")
    # Создание прокрутки для таблицы книг
    scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscroll=scrollbar.set)

    # Заполнение таблицы книг в заказе
    for item in order_items:
        tree.insert("", "end", values=item)

    # Проверка, если нет книг в заказе
    if not order_items:
        messagebox.showinfo("Информация", "Нет книг в этом заказе.")
        
def create_order_window():
    # Создание основного окна
    root = tk.Tk()
    root.title("Информация о заказах")

    # Создание фрейма для таблицы заказов
    frame = ttk.Frame(root)
    frame.pack(pady=10)

    # Создание таблицы для заказов
    tree = ttk.Treeview(frame, columns=("ID заказа", "Имя", "Фамилия", "Дата заказа", "Сумма", "Статус"), show="headings")
    tree.heading("ID заказа", text="ID заказа")
    tree.heading("Имя", text="Имя")
    tree.heading("Фамилия", text="Фамилия")
    tree.heading("Дата заказа", text="Дата заказа")
    tree.heading("Сумма", text="Сумма")
    tree.heading("Статус", text="Статус")
    tree.pack(side="left")

    # Создание прокрутки для таблицы заказов
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscroll=scrollbar.set)
    
    show_orders(tree)
    def on_double_click(event):
        selected_item = tree.selection()
        if selected_item:
            order_id = tree.item(selected_item, 'values')[0]
            print(f"Выбран заказ ID: {order_id}")  # Отладочное сообщение
            show_order_details(order_id)

    tree.bind("<Double-1>", on_double_click)

    # # Запуск основного цикла
    root.mainloop()
    
def display_book_catalog():
    # Создаем новое окно для отображения каталога книг
    catalog_window = tk.Toplevel()
    catalog_window.title("Каталог книг")
    
    # Создаем таблицу для отображения книг
    tree = ttk.Treeview(catalog_window, columns=("ID", "Название", "Автор", "Цена", "Остаток", "Описание"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Название", text="Название")
    tree.heading("Автор", text="Автор")
    tree.heading("Цена", text="Цена")
    tree.heading("Остаток", text="Остаток")
    tree.heading("Описание", text="Описание")
    
    tree.pack(fill=tk.BOTH, expand=True)

    # Подключаемся к базе данных
    conn = sqlite3.connect('book_store.db')
    cursor = conn.cursor()
    
    # Запрос для получения всех книг
    cursor.execute('SELECT book_id, title, author, price, stock, description FROM books')
    books = cursor.fetchall()
    
    # Проверяем, есть ли книги в каталоге
    if not books:
        messagebox.showinfo("Информация", "Каталог книг пуст.")
    else:
        for book in books:
            tree.insert("", tk.END, values=book)
    
    conn.close()
