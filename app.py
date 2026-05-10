import os
import sqlite3
import secrets
import traceback
from flask import Flask, render_template_string, request, redirect, url_for, session
from urllib.parse import quote as url_quote

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.jinja_env.filters['urlencode'] = lambda s: url_quote(str(s))

DB_FILE = os.path.join(os.path.dirname(__file__), 'exam_system.db')
web_conn = None
web_cursor = None

def get_db_connection():
    global web_conn, web_cursor
    if web_conn is None:
        web_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        web_cursor = web_conn.cursor()
    return web_conn, web_cursor

def ensure_tables():
    try:
        conn, cursor = get_db_connection()
        cursor.execute("""CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            teacher_name TEXT,
            mobile_number TEXT
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admission_number TEXT UNIQUE,
            student_name TEXT,
            grade INTEGER
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            exam_id INTEGER,
            marks INTEGER
        )""")
        conn.commit()
        print("? Database ready")
    except Exception as e:
        print(f"DB Error: {e}")

def hash_password(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return '''<html><head><title>EDUSMART</title><style>
    body{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);margin:0;padding:20px;min-height:100vh}
    .container{max-width:800px;margin:0 auto;background:white;padding:40px;border-radius:10px}
    h1{color:#667eea;text-align:center}
    .content{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:30px}
    .card{padding:20px;text-align:center}
    .btn{background:#667eea;color:white;padding:12px 20px;border:none;border-radius:5px;cursor:pointer;text-decoration:none;display:inline-block;margin-top:15px}
    .btn:hover{background:#764ba2}</style></head><body>
    <div class="container"><h1>?? EDUSMART</h1><p style="text-align:center">Online Results Management System</p>
    <div class="content">
    <div class="card"><h3>?? Students</h3><a href="/check_results" class="btn">Check Results</a></div>
    <div class="card"><h3>????? Teachers</h3><a href="/login" class="btn">Login</a></div>
    </div></div></body></html>'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            if username and password:
                conn, cursor = get_db_connection()
                cursor.execute("SELECT teacher_name FROM teachers WHERE username = ? AND password_hash = ?", (username, hash_password(password)))
                row = cursor.fetchone()
                if row:
                    session['username'] = username
                    session['teacher_name'] = row[0]
                    return redirect(url_for('dashboard'))
                else:
                    error = "Invalid credentials"
            else:
                error = "Please fill all fields"
        except Exception as e:
            error = f"Error: {str(e)}"
            traceback.print_exc()
    
    return f'''<html><head><title>Login</title><style>
    body{{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}}
    .form{{background:white;padding:40px;border-radius:10px;width:100%;max-width:400px}}
    h1{{color:#667eea;text-align:center;margin-top:0}}
    .form-group{{margin-bottom:20px}}
    label{{display:block;margin-bottom:8px;font-weight:bold}}
    input{{width:100%;padding:10px;border:1px solid #ddd;border-radius:5px}}
    button{{width:100%;padding:12px;background:#667eea;color:white;border:none;border-radius:5px;cursor:pointer;font-weight:bold}}
    button:hover{{background:#764ba2}}
    .error{{color:#e74c3c;background:#ffe0e0;padding:12px;border-radius:5px;margin-bottom:20px}}
    .links{{text-align:center;margin-top:20px}}
    .links a{{color:#667eea;text-decoration:none;margin:0 10px}}
    </style></head><body>
    <div class="form"><h1>????? Teacher Login</h1>
    {"<div class=\"error\">" + error + "</div>" if error else ""}
    <form method="POST">
    <div class="form-group"><label>Username:</label><input type="text" name="username" required></div>
    <div class="form-group"><label>Password:</label><input type="password" name="password" required></div>
    <button type="submit">Login</button></form>
    <div class="links"><a href="/">Home</a><a href="/register">Sign Up</a></div>
    </div></body></html>'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        try:
            name = request.form.get('teacher_name', '').strip()
            phone = request.form.get('mobile', '').strip()
            pwd = request.form.get('password', '').strip()
            confirm = request.form.get('confirm', '').strip()
            
            if not name or not phone or not pwd:
                message = "Fill all fields"
            elif pwd != confirm:
                message = "Passwords don't match"
            elif len(pwd) < 6:
                message = "Password too short"
            else:
                conn, cursor = get_db_connection()
                username = f"teacher_{secrets.token_hex(4)}"
                cursor.execute("INSERT INTO teachers (username, password_hash, teacher_name, mobile_number) VALUES (?, ?, ?, ?)",
                    (username, hash_password(pwd), name, phone))
                conn.commit()
                message = f"? Account created! Username: {username}"
        except Exception as e:
            message = f"Error: {str(e)}"
            traceback.print_exc()
    
    return f'''<html><head><title>Register</title><style>
    body{{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}}
    .form{{background:white;padding:40px;border-radius:10px;width:100%;max-width:400px}}
    h1{{color:#667eea;text-align:center;margin-top:0}}
    .form-group{{margin-bottom:20px}}
    label{{display:block;margin-bottom:8px;font-weight:bold}}
    input{{width:100%;padding:10px;border:1px solid #ddd;border-radius:5px}}
    button{{width:100%;padding:12px;background:#667eea;color:white;border:none;border-radius:5px;cursor:pointer}}
    button:hover{{background:#764ba2}}
    .msg{{padding:12px;border-radius:5px;margin-bottom:20px;background:#e0ffe0;color:#27ae60}}
    .links{{text-align:center;margin-top:20px}}
    .links a{{color:#667eea;text-decoration:none;margin:0 10px}}
    </style></head><body>
    <div class="form"><h1>?? Register</h1>
    {"<div class=\"msg\">" + message + "</div>" if message else ""}
    <form method="POST">
    <div class="form-group"><label>Teacher Name:</label><input type="text" name="teacher_name" required></div>
    <div class="form-group"><label>Mobile:</label><input type="tel" name="mobile" required></div>
    <div class="form-group"><label>Password:</label><input type="password" name="password" required></div>
    <div class="form-group"><label>Confirm:</label><input type="password" name="confirm" required></div>
    <button type="submit">Create Account</button></form>
    <div class="links"><a href="/">Home</a><a href="/login">Login</a></div>
    </div></body></html>'''

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f'''<html><head><title>Dashboard</title><style>
    body{{font-family:Arial;margin:30px;background:#f5f5f5}}
    .container{{max-width:1000px;margin:0 auto}}
    .header{{background:white;padding:20px;border-radius:8px;display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}}
    .logout{{background:#e74c3c;color:white;padding:10px 20px;border-radius:5px;text-decoration:none}}
    </style></head><body>
    <div class="container">
    <div class="header">
    <div><h1>?? Dashboard</h1><p>Welcome, {session.get('teacher_name', session.get('username'))}</p></div>
    <a href="/logout" class="logout">Logout</a>
    </div>
    <div style="background:white;padding:20px;border-radius:8px">
    <h2>? Logged In Successfully</h2>
    <p>Welcome to EDUSMART Online Results Management System.</p>
    </div>
    </div></body></html>'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/check_results')
def check_results():
    return '''<html><head><title>Results</title><style>
    body{{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);margin:0;padding:20px;min-height:100vh}}
    .container{{max-width:600px;margin:0 auto;background:white;padding:40px;border-radius:10px}}
    h1{{color:#667eea;text-align:center}}
    input{{width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;margin-bottom:15px}}
    button{{width:100%;padding:12px;background:#667eea;color:white;border:none;border-radius:5px;cursor:pointer}}
    button:hover{{background:#764ba2}}
    </style></head><body>
    <div class="container"><h1>?? Check Results</h1>
    <form method="POST">
    <input type="text" name="admission" placeholder="Admission Number" required>
    <input type="text" name="name" placeholder="Student Name" required>
    <button>Search</button>
    </form>
    <div style="text-align:center;margin-top:20px"><a href="/" style="color:#667eea">? Home</a></div>
    </div></body></html>'''

@app.errorhandler(500)
def error(e):
    print(f"Error: {e}")
    traceback.print_exc()
    return "Internal Server Error", 500

try:
    ensure_tables()
    print("? EDUSMART app initialized")
except Exception as e:
    print(f"Init error: {e}")
    traceback.print_exc()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
