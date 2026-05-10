#!/usr/bin/env python
"""
EDUSMART - Online Exam Results Management System
Deployment wrapper that runs the Flask web server with templates from main exam system code.
"""

import os
import sys
import sqlite3
import secrets
import traceback

# Ensure main module is importable
sys.path.insert(0, os.path.dirname(__file__))

# Import Flask requirements
try:
    from flask import Flask, render_template_string, request, redirect, url_for, session
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("ERROR: Flask not installed")
    sys.exit(1)

# Database configuration
DB_FILE = os.path.join(os.path.dirname(__file__), 'exam_system.db')

# Global database connection
web_conn = None
web_cursor = None

def get_db_connection():
    """Get or create database connection."""
    global web_conn, web_cursor
    if web_conn is None:
        web_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        web_cursor = web_conn.cursor()
    return web_conn, web_cursor

def hash_password(password):
    """Hash a password for secure storage."""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def ensure_tables():
    """Create database tables if they don't exist."""
    conn, cursor = get_db_connection()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        teacher_name TEXT,
        mobile_number TEXT,
        staff_number TEXT
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admission_number TEXT UNIQUE,
        student_name TEXT,
        grade INTEGER,
        stream TEXT,
        level TEXT,
        parent_phone TEXT,
        parent_id TEXT
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        exam_id INTEGER,
        marks INTEGER
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidate_targets (
        student_id INTEGER,
        subject_id INTEGER,
        target INTEGER,
        PRIMARY KEY(student_id, subject_id)
    )''')
    
    conn.commit()

def verify_teacher_credentials(username, password):
    """Verify teacher login credentials."""
    try:
        conn, cursor = get_db_connection()
        password_hash = hash_password(password)
        cursor.execute("SELECT teacher_name FROM teachers WHERE username = ? AND password_hash = ?", (username, password_hash))
        row = cursor.fetchone()
        if row:
            return True, row[0]
        return False, None
    except Exception as e:
        print(f"Error verifying credentials: {e}")
        return False, None

def save_teacher_credentials(username, password, teacher_name, mobile_number, staff_number=None):
    """Save new teacher credentials."""
    try:
        conn, cursor = get_db_connection()
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO teachers (username, password_hash, teacher_name, mobile_number, staff_number) VALUES (?, ?, ?, ?, ?)",
            (username, password_hash, teacher_name, mobile_number, staff_number)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving teacher: {e}")
        return False

def get_teacher_info(username):
    """Get teacher information."""
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT id, mobile_number, staff_number FROM teachers WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return {'id': row[0], 'mobile': row[1], 'staff_number': row[2] or 'N/A'}
        return None
    except Exception as e:
        print(f"Error getting teacher info: {e}")
        return None

def generate_teacher_username():
    """Generate unique teacher username."""
    while True:
        username = f"teacher_{secrets.token_hex(4)}"
        conn, cursor = get_db_connection()
        cursor.execute("SELECT id FROM teachers WHERE username = ?", (username,))
        if not cursor.fetchone():
            return username

# ==================== LOAD TEMPLATES ====================

TEMPLATES = {}

def load_templates():
    """Try to load templates from exam_system module."""
    global TEMPLATES
    try:
        # Try direct import first
        import exam_system as exam_mod
        
        # List of template names to try loading
        template_names = [
            'LOGIN_TEMPLATE', 'REGISTER_TEMPLATE', 'DASHBOARD_TEMPLATE',
            'WELCOME_TEMPLATE', 'CHECK_RESULTS_TEMPLATE', 'STUDENTS_TEMPLATE',
            'TEACHERS_TEMPLATE', 'FORGOT_PASSWORD_TEMPLATE', 'CANDIDATE_LOGIN_TEMPLATE',
            'CANDIDATE_DASHBOARD_TEMPLATE', 'SIDEBAR_PAGE_TEMPLATE'
        ]
        
        for template_name in template_names:
            if hasattr(exam_mod, template_name):
                TEMPLATES[template_name] = getattr(exam_mod, template_name)
                print(f"✓ Loaded: {template_name}")
        
        if TEMPLATES:
            print(f"✓ Loaded {len(TEMPLATES)} templates from exam_system module")
            return True
    except Exception as e:
        print(f"⚠ Could not import exam_system module: {e}")
    
    return False

# Create Flask app
app = Flask(__name__, static_folder='.')
app.secret_key = secrets.token_hex(16)

# Add URL encoding filter
from urllib.parse import quote as url_quote
app.jinja_env.filters['urlencode'] = lambda s: url_quote(str(s))

# Initialize on startup
print("=" * 60)
print("Starting EDUSMART Web Server...")
print("=" * 60)
try:
    ensure_tables()
    print("✓ Database tables ready")
    
    if load_templates():
        print("✓ Templates loaded successfully")
    else:
        print("⚠ Templates not found - will use built-in fallbacks")
    
    print("✓ EDUSMART Web Server initialized")
except Exception as e:
    print(f"✗ Initialization error: {e}")
    traceback.print_exc()

# ==================== FALLBACK TEMPLATES ====================

FALLBACK_LOGIN = '''
<html>
<head><title>Login - EDUSMART</title>
<style>
body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
.container { background: white; padding: 50px; border-radius: 10px; width: 100%; max-width: 400px; }
h1 { text-align: center; color: #667eea; }
input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
button { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
button:hover { opacity: 0.9; }
.error { color: red; background: #ffe0e0; padding: 10px; border-radius: 5px; }
.links { text-align: center; margin-top: 15px; }
.links a { margin: 0 10px; color: #667eea; text-decoration: none; }
</style>
</head>
<body>
<div class="container">
<h1>🎓 Teacher Login</h1>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
<form method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button>Login</button>
</form>
<div class="links">
<a href="/">Home</a> | <a href="/register">Register</a>
</div>
</div>
</body>
</html>
'''

FALLBACK_HOME = '''
<html>
<head><title>EDUSMART - Home</title>
<style>
body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; min-height: 100vh; }
.container { max-width: 1000px; margin: 0 auto; background: white; padding: 50px; border-radius: 15px; text-align: center; }
h1 { color: #667eea; font-size: 2.5em; margin: 0; }
p { color: #666; font-size: 1.2em; }
.buttons { margin: 30px 0; }
.btn { display: inline-block; padding: 15px 30px; margin: 10px; border-radius: 5px; text-decoration: none; font-weight: bold; cursor: pointer; }
.btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.btn-primary:hover { opacity: 0.9; }
</style>
</head>
<body>
<div class="container">
<h1>🎓 EDUSMART SOLUTIONS</h1>
<p>Online Exam Results Management System</p>
<div class="buttons">
<a href="/login" class="btn btn-primary">👨‍🏫 Teacher Login</a>
<a href="/register" class="btn btn-primary">📝 Register</a>
<a href="/check_results" class="btn btn-primary">📊 Check Results</a>
</div>
</div>
</body>
</html>
'''

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page."""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    template = TEMPLATES.get('WELCOME_TEMPLATE', FALLBACK_HOME)
    return render_template_string(template, request=request)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Teacher login."""
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if username and password:
            success, teacher_name = verify_teacher_credentials(username, password)
            if success:
                session['username'] = username
                session['teacher_name'] = teacher_name
                teacher_info = get_teacher_info(username)
                if teacher_info:
                    session['teacher_id'] = teacher_info['id']
                    session['mobile_number'] = teacher_info['mobile']
                    session['staff_number'] = teacher_info['staff_number']
                print(f"✓ Teacher {username} logged in")
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid username or password"
        else:
            error = "Please enter username and password"
    
    template = TEMPLATES.get('LOGIN_TEMPLATE', FALLBACK_LOGIN)
    return render_template_string(template, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Teacher registration."""
    message = None
    success = False
    generated_username = None
    
    if request.method == 'POST':
        try:
            teacher_name = request.form.get('teacher_name', '').strip()
            mobile_number = request.form.get('mobile_number', '').strip()
            staff_number = request.form.get('staff_number', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if not teacher_name or not mobile_number or not password or not confirm_password:
                message = '❌ Please fill all required fields'
            elif len(mobile_number) < 10:
                message = '❌ Mobile number too short (min 10 digits)'
            elif password != confirm_password:
                message = '❌ Passwords do not match'
            elif len(password) < 6:
                message = '❌ Password too short (min 6 chars)'
            else:
                generated_username = generate_teacher_username()
                if save_teacher_credentials(generated_username, password, teacher_name, mobile_number, staff_number or None):
                    success = True
                    message = f'✓ Account created! Username: <b>{generated_username}</b>'
                    print(f"✓ New teacher registered: {generated_username}")
                else:
                    message = '❌ Failed to create account - username may exist'
        except Exception as e:
            message = f'❌ Error: {str(e)}'
            traceback.print_exc()
    
    template = TEMPLATES.get('REGISTER_TEMPLATE', '''
    <html>
    <head><title>Register - EDUSMART</title>
    <style>
    body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
    .container { background: white; padding: 50px; border-radius: 10px; width: 100%; max-width: 400px; }
    h1 { text-align: center; color: #667eea; }
    input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
    button { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    .msg { padding: 15px; border-radius: 5px; margin: 10px 0; background: #e0ffe0; color: #27ae60; }
    </style>
    </head>
    <body>
    <div class="container">
    <h1>📝 Register</h1>
    {% if message %}<div class="msg">{{ message|safe }}</div>{% endif %}
    <form method="POST">
    <input type="text" name="teacher_name" placeholder="Teacher Name" required>
    <input type="tel" name="mobile_number" placeholder="Mobile Number" required>
    <input type="text" name="staff_number" placeholder="Staff Number (optional)">
    <input type="password" name="password" placeholder="Password" required>
    <input type="password" name="confirm_password" placeholder="Confirm Password" required>
    <button>Create Account</button>
    </form>
    </div>
    </body>
    </html>
    ''')
    
    return render_template_string(template, message=message, success=success, generated_username=generated_username)

@app.route('/dashboard')
def dashboard():
    """Teacher dashboard."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    stats = {'total_students': 0, 'total_exams': 0, 'total_subjects': 0, 'total_classes': 0}
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT COUNT(*) FROM students")
        stats['total_students'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM exams")
        stats['total_exams'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM subjects")
        stats['total_subjects'] = cursor.fetchone()[0]
    except:
        pass
    
    teacher_name = session.get('teacher_name', session.get('username', 'Teacher'))
    
    template = TEMPLATES.get('DASHBOARD_TEMPLATE', '''
    <html>
    <head><title>Dashboard - EDUSMART</title>
    <style>
    body { font-family: Arial; background: #f5f5f5; margin: 0; padding: 20px; }
    .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
    .header { display: flex; justify-content: space-between; align-items: center; }
    h1 { color: #667eea; margin: 0; }
    .logout { background: #e74c3c; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; }
    .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
    .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
    .stat-card h3 { margin: 0 0 10px 0; font-size: 1.2em; }
    .stat-card .number { font-size: 2em; font-weight: bold; }
    </style>
    </head>
    <body>
    <div class="container">
    <div class="header">
    <div><h1>📊 Dashboard</h1><p>Welcome, {{ teacher_name }}!</p></div>
    <a href="/logout" class="logout">Logout</a>
    </div>
    <div class="stats">
    <div class="stat-card"><h3>Students</h3><div class="number">{{ total_students }}</div></div>
    <div class="stat-card"><h3>Exams</h3><div class="number">{{ total_exams }}</div></div>
    <div class="stat-card"><h3>Subjects</h3><div class="number">{{ total_subjects }}</div></div>
    <div class="stat-card"><h3>Classes</h3><div class="number">{{ total_classes }}</div></div>
    </div>
    </div>
    </body>
    </html>
    ''')
    
    return render_template_string(template, 
        username=session['username'],
        teacher_name=teacher_name,
        total_students=stats['total_students'],
        total_exams=stats['total_exams'],
        total_subjects=stats['total_subjects'],
        total_classes=stats['total_classes'])

@app.route('/logout')
def logout():
    """Logout."""
    print(f"✓ User {session.get('username')} logged out")
    session.clear()
    return redirect(url_for('login'))

@app.route('/check_results', methods=['GET', 'POST'])
def check_results():
    """Public page for checking exam results."""
    template = TEMPLATES.get('CHECK_RESULTS_TEMPLATE', '''
    <html>
    <head><title>Check Results - EDUSMART</title>
    <style>
    body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
    .container { background: white; padding: 40px; border-radius: 10px; width: 100%; max-width: 500px; }
    h1 { text-align: center; color: #667eea; }
    input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
    button { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    .home-link { text-align: center; margin-top: 20px; }
    .home-link a { color: #667eea; text-decoration: none; }
    </style>
    </head>
    <body>
    <div class="container">
    <h1>📊 Check Results</h1>
    <p style="text-align: center;">Enter your details to view exam results</p>
    <form method="POST">
    <input type="text" name="admission_number" placeholder="Admission Number" required>
    <input type="text" name="student_name" placeholder="Student Name" required>
    <button>Search Results</button>
    </form>
    <div class="home-link"><a href="/">← Back Home</a></div>
    </div>
    </body>
    </html>
    ''')
    
    return render_template_string(template)

@app.route('/students')
def students_page():
    """Students management page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    grades = list(range(1, 10))
    return render_template_string('<h1>Students Management</h1><p>Grades: ' + str(grades) + '</p>')

@app.route('/teachers')
def teachers_page():
    """Teachers management page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    teachers = []
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT id, username, teacher_name, mobile_number FROM teachers ORDER BY id DESC")
        teachers = [{'id': r[0], 'username': r[1], 'name': r[2], 'mobile': r[3]} for r in cursor.fetchall()]
    except:
        pass
    
    return render_template_string('<h1>Teachers (' + str(len(teachers)) + ')</h1>')

@app.errorhandler(500)
def error_500(e):
    """Handle 500 errors."""
    print(f"500 Error: {e}")
    traceback.print_exc()
    return '''<html><body style="font-family:Arial; padding:20px;">
    <h1>❌ Server Error</h1>
    <p>Something went wrong. Please try again.</p>
    <a href="/">← Home</a>
    </body></html>''', 500

@app.errorhandler(404)
def error_404(e):
    """Handle 404 errors."""
    return '''<html><body style="font-family:Arial; padding:20px;">
    <h1>❌ Page Not Found</h1>
    <a href="/">← Home</a>
    </body></html>''', 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting web server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)

