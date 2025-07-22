import sqlite3

def init_db():
    conn = sqlite3.connect("messenger.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    try:
        conn = sqlite3.connect("messenger.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("messenger.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

def save_message(sender, content):
    conn = sqlite3.connect("messenger.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, content) VALUES (?, ?)", (sender, content))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect("messenger.db")
    c = conn.cursor()
    c.execute("SELECT sender, content FROM messages")
    messages = c.fetchall()
    conn.close()
    return messages
