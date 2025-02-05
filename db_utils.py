import sqlite3

def init_db():
    conn = sqlite3.connect('health_app.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT,
        age INTEGER,
        gender TEXT,
        phone TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        medicine_name TEXT,
        dose TEXT,
        reminder_time TEXT,
        FOREIGN KEY (user_id) REFERENCES Users (id)
    )
    """)
    conn.commit()
    conn.close()

def add_user(username, email, password_hash, age, gender, phone):
    conn = sqlite3.connect('health_app.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO Users (username, email, password_hash, age, gender, phone)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (username, email, password_hash, age, gender, phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect('health_app.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM Users WHERE email = ?
    """, (email,))
    user = cursor.fetchone()
    conn.close()
    return user
