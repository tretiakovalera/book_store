import sqlite3

# Создание таблиц
def create_tables():
    conn = sqlite3.connect('book_store.db')

    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            usersID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            Phone TEXT,
            Email TEXT
        )
        ''')
    
    # Таблица книг
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        author TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT,
        image_url TEXT
    )
    ''')
    
    # Таблица корзины
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
    ''')
    
    # Таблица заказов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        order_date TEXT NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT CHECK(status IN ('pending', 'completed', 'canceled')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    # Таблица товаров в заказе
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        book_id INTEGER,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
    ''')
    
    conn.commit()
    
def add_book(title, author, price, stock, description=None, image_url=None):
    try:
        conn = sqlite3.connect('book_store.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, price, stock, description, image_url) VALUES (?, ?, ?, ?, ?, ?)",
                       (title, author, price, stock, description, image_url))
        conn.commit()
        print("Книга успешно добавлена.")
    except sqlite3.IntegrityError:
        print("Ошибка: Книга с таким названием уже существует.")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        conn.close()