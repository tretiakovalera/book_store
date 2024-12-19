import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
def search_book(user_id):
    book_title = simpledialog.askstring("Поиск книги", "Введите название книги:")
    if book_title:
        conn = sqlite3.connect('book_store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + book_title + '%',))
        books = cursor.fetchall()
        conn.close()
        
        if books:
            add_to_cart(books, user_id)  # Передаем список книг и user_id
        else:
            messagebox.showinfo("Результаты поиска", "Книги не найдены.")

def add_to_cart(books, user_id):
    # Извлекаем названия книг и их ID
    book_options = [(book[1], book[0]) for book in books]  # (название, ID книги)
    
    # Формируем строку для выбора книги
    book_titles = "\n".join([f"{i + 1}. {title}" for i, (title, _) in enumerate(book_options)])
    
    # Запрашиваем у пользователя выбор книги
    choice = simpledialog.askinteger("Выбор книги", f"Выберите книгу:\n{book_titles}\nВведите номер книги:")
    
    if choice is not None and 1 <= choice <= len(book_options):
        selected_book = book_options[choice - 1]  # Получаем выбранную книгу
        book_title, book_id = selected_book
        
        quantity = simpledialog.askinteger("Добавить в корзину", "Введите количество:")
        if quantity is not None:  # Проверяем, что пользователь не отменил ввод
            try:
                conn = sqlite3.connect('book_store.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cart (user_id, book_id, quantity) VALUES (?, ?, ?)", (user_id, book_id, quantity))
                conn.commit()
                messagebox.showinfo("Успех", "Книга добавлена в корзину.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            finally:
                conn.close()  # Закрываем соединение с базой данных
    else:
        messagebox.showinfo("Информация", "Неверный выбор. Пожалуйста, попробуйте снова.")

def show_cart(user_id):
    if user_id is None:
        messagebox.showerror("Ошибка", "Пожалуйста, войдите в систему.")
        return

    conn = sqlite3.connect('book_store.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT b.title, b.author, c.quantity, b.price
        FROM cart c
        JOIN books b ON c.book_id = b.book_id
        WHERE c.user_id = ?
    ''', (user_id,))
    
    cart_items = cursor.fetchall()
    conn.close()
    
    if cart_items:
        result = "\n".join([f"{item[0]} by {item[1]} - Quantity: {item[2]}, Price: ${item[3]:.2f}" for item in cart_items])
        # messagebox.showinfo("Корзина", f"Ваши товары в корзине:\n{result}")
    else:
        messagebox.showinfo("Корзина", "Ваша корзина пуста.")
        return

    # Создаем новое окно для отображения корзины
    cart_window = tk.Toplevel()
    cart_window.title("Корзина")

    # Отображаем содержимое корзины в текстовом поле
    cart_text = tk.Text(cart_window, width=50, height=10)
    cart_text.insert(tk.END, result)
    cart_text.config(state=tk.DISABLED)  # Делаем текстовое поле только для чтения
    cart_text.pack(pady=10)

    # Кнопка для оформления заказа
    button_place_order = tk.Button(
        cart_window,
        text="Оформить заказ",
        command=lambda: place_order(user_id,get_cart_items(user_id))
    )
    button_place_order.pack(pady=10)
    
def get_cart_items(user_id):
    conn = sqlite3.connect('book_store.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT b.book_id, b.title, c.quantity, b.price
        FROM cart c
        JOIN books b ON c.book_id = b.book_id
        WHERE c.user_id = ?
    ''', (user_id,))
    
    cart_items = cursor.fetchall()
    conn.close()
    
    # Преобразуем данные в удобный формат
    return [{'book_id': item[0], 'title': item[1], 'quantity': item[2], 'price': item[3]} for item in cart_items]

def place_order(user_id, cart_items):
    if user_id is None or not cart_items:
        print("Ошибка: Необходимо указать пользователя и товары для заказа.")
        return

    conn = sqlite3.connect('book_store.db')
    cursor = conn.cursor()

    try:
        total_amount = sum(item['quantity'] * item['price'] for item in cart_items)

        cursor.execute('''
            INSERT INTO orders (user_id, order_date, total_amount, status)
            VALUES (?, ?, ?, 'pending')
        ''', (user_id, datetime.now().strftime('%d-%m-%Y %H:%M'), total_amount))
        
        order_id = cursor.lastrowid

        for item in cart_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, book_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['book_id'], item['quantity'], item['price']))
              # Уменьшаем количество книг в таблице books
            cursor.execute('''
                UPDATE books
                SET stock = stock - ?
                WHERE book_id = ?
            ''', (item['quantity'], item['book_id']))
        # Удаляем товары из корзины после оформления заказа
        cursor.execute('''
            DELETE FROM cart WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
        messagebox.showinfo("Информация", "Заказ успешно оформлен!")
    except Exception as e:
        print(f"Произошла ошибка при оформлении заказа: {str(e)}")
    finally:
        conn.close()

def remove_from_cart(user_id):
    conn = None  # Инициализируем переменную conn
    try:
        # Запрашиваем у пользователя название книги для удаления
        book_title = simpledialog.askstring("Удаление товара", "Введите название книги для удаления из корзины:")
        
        if book_title is not None:  # Проверяем, что пользователь не отменил ввод
            conn = sqlite3.connect('book_store.db')  # Устанавливаем соединение
            cursor = conn.cursor()
            
            # Получаем ID книги по названию
            cursor.execute("SELECT book_id FROM books WHERE title = ?", (book_title,))
            book = cursor.fetchone()
            
            if book is not None:
                book_id = book[0]  # Извлекаем ID книги
                
                # Удаляем товар из корзины
                cursor.execute("DELETE FROM cart WHERE user_id = ? AND book_id = ?", (user_id, book_id))
                conn.commit()
                
                # Проверяем, было ли удаление успешным
                if cursor.rowcount > 0:
                    messagebox.showinfo("Успех", "Книга успешно удалена из корзины.")
                else:
                    messagebox.showinfo("Информация", "Книга не найдена в вашей корзине.")
            else:
                messagebox.showinfo("Информация", "Книга с таким названием не найдена.")
    
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    finally:
        if conn is not None:  # Проверяем, было ли соединение установлено
            conn.close() 