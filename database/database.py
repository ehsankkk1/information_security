import sqlite3


def initalizeDataBaseTables():
    create_user_table()
    create_students_marks_table()


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
            user_type TEXT NOT NULL,
            csr TEXT NULL,
            private_key TEXT NULL,
            public_key TEXT NULL
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
        return "User added successfully."
    except sqlite3.IntegrityError:
        return "Error: Username must be unique. User not added."
    finally:
        conn.close()


def login_user_db(username, password):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


def edit_user_info_db(username, new_city, new_phone_number):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET city=?, phone_number=? WHERE username=?',
                   (new_city, new_phone_number, username))
    conn.commit()
    conn.close()
    return "User information updated successfully."


def create_teacher_private_key_db(username, privatekey):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET private_key=? WHERE username=?',
                   (privatekey, username))
    conn.commit()
    conn.close()
    return "Teacher private key created successfully."


def create_teacher_csr_db(username, csr):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET csr=? WHERE username=?',
                   (csr, username))
    conn.commit()
    conn.close()
    return "Teacher certificate created successfully."


def insert_client_pub_key(username, public_key):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET public_key=? WHERE username=?', (public_key, username))
    conn.commit()
    conn.close()


def get_client_pub_key(username):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT public_key FROM users WHERE username=?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0]


def create_students_marks_table():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT UNIQUE NOT NULL,
            subject_name TEXT NOT NULL,
            mark TEXT NOT NULL
                    )
    ''')
    conn.commit()
    conn.close()


def add_student_mark(student_name, subject_name, mark):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO students_marks (student_name,subject_name, mark) VALUES (?, ?,?)',
                       (student_name, subject_name, mark))
        conn.commit()
        return "mark added successfully."
    except sqlite3.IntegrityError:
        return "Error: mark not valid"
    finally:
        conn.close()


def get_marks():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students_marks')
    user = cursor.fetchone()
    conn.close()
    return user
