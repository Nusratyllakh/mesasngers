import json
import os

USERS_FILE = "users.json"
MESSAGES_FILE = "messages.json"

# === USERS ===
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def register_user(username, password):
    users = load_users()
    if any(u["username"] == username for u in users):
        return False  # имя занято
    users.append({"username": username, "password": password})
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    return any(u["username"] == username and u["password"] == password for u in users)

# === MESSAGES ===
def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_message(sender, content):
    messages = load_messages()
    messages.append({"sender": sender, "content": content})
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

def get_all_messages():
    return load_messages()

# === Общая инициализация ===
def init_db():
    if not os.path.exists(USERS_FILE):
        save_users([])

    if not os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

 
