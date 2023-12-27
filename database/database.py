import sqlite3

def initalizeDataBaseTables():
    create_user_table()


def create_user_table():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user_db(username, city, phone_number, password, user_type):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO users (username, city, phone_number, password, user_type) VALUES (?, ?, ?, ?, ?)',
                       (username, city, phone_number, password, user_type))
        conn.commit()
        print("User added successfully.")
    except sqlite3.IntegrityError:
        print("Error: Username must be unique. User not added.")
    finally:
        conn.close()

def login_user_db(username, password):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user
