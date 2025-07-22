from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'messenger.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')  # отдаем HTML из templates/index.html

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'error': 'Username taken'}), 400
    conn.close()
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT sender, content FROM messages ORDER BY id")
    msgs = c.fetchall()
    conn.close()
    messages = [{'sender': row['sender'], 'content': row['content']} for row in msgs]
    return jsonify(messages)

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.json
    sender = data.get('sender')
    content = data.get('content')
    if not sender or not content:
        return jsonify({'success': False, 'error': 'Missing sender or content'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, content) VALUES (?, ?)", (sender, content))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
