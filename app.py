#!/usr/bin/env python
"""
EDUSMART - Online Exam Results Management System
Deployment wrapper that runs the Flask web server with templates from main exam system code.
"""

import os
import sys
import sqlite3
import secrets
import re

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
        staff_number TEXT,
        admission_num TEXT,
        first_school TEXT,
        village TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS subject_levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        level TEXT,
        grade INTEGER,
        FOREIGN KEY(subject_id) REFERENCES subjects(id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        exam_id INTEGER,
        marks INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(subject_id) REFERENCES subjects(id),
        FOREIGN KEY(exam_id) REFERENCES exams(id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidate_targets (
        student_id INTEGER,
        subject_id INTEGER,
        target INTEGER,
        PRIMARY KEY(student_id, subject_id),
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(subject_id) REFERENCES subjects(id)
    )''')
    
    conn.commit()
    print("✓ Database tables ready")

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
            return {'id': row[0], 'mobile': row[1], 'staff_number': row[2]}
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

# ==================== LOAD TEMPLATES FROM MAIN FILE ====================

TEMPLATES = {}

def load_templates_from_main_file():
    """Extract all HTML templates from the main exam_system.py file."""
    global TEMPLATES
    try:
        main_file = os.path.join(os.path.dirname(__file__), 'exam_system.py')
        if not os.path.exists(main_file):
            print("⚠ Main file (exam_system.py) not found - using placeholder templates")
            return
        
        with open(main_file, 'r', encoding='utf-8', errors='ignore') as f:
            main_code = f.read()
        
        # Extract all _TEMPLATE = """ ... """ assignments
        pattern = r'(\w+_TEMPLATE) = """((?:[^"\\]|\\.)*?)"""'
        
        for match in re.finditer(pattern, main_code, re.DOTALL):
            template_name = match.group(1)
            template_content = match.group(2)
            TEMPLATES[template_name] = template_content
            print(f"✓ Loaded: {template_name}")
            
    except Exception as e:
        print(f"⚠ Error loading templates: {e}")

# Create Flask app
app = Flask(__name__, static_folder='.')
app.secret_key = secrets.token_hex(16)

# Add URL encoding filter
from urllib.parse import quote as url_quote
app.jinja_env.filters['urlencode'] = lambda s: url_quote(str(s))

# Initialize on startup
print("Starting EDUSMART Web Server...")
try:
    ensure_tables()
    load_templates_from_main_file()
    print("✓ EDUSMART Web Server initialized")
except Exception as e:
    print(f"✗ Initialization error: {e}")
    import traceback
    traceback.print_exc()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page."""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    template = TEMPLATES.get('WELCOME_TEMPLATE', '''
    <html><head><title>EDUSMART</title></head><body>
    <h1>Welcome to EDUSMART</h1>
    <p><a href="/login">Teacher Login</a> | <a href="/check_results">Check Results</a></p>
    </body></html>''')
    
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
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid username or password"
        else:
            error = "Please enter username and password"
    
    template = TEMPLATES.get('LOGIN_TEMPLATE', '''
    <html><head><title>Login</title></head><body>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button>Login</button>
    </form>
    </body></html>''')
    
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
                message = '❌ Mobile number too short'
            elif password != confirm_password:
                message = '❌ Passwords do not match'
            elif len(password) < 6:
                message = '❌ Password too short (min 6 chars)'
            else:
                generated_username = generate_teacher_username()
                if save_teacher_credentials(generated_username, password, teacher_name, mobile_number, staff_number or None):
                    success = True
                    message = f'✓ Success! Your username: {generated_username}'
                else:
                    message = '❌ Failed to create account'
        except Exception as e:
            message = f'❌ Error: {str(e)}'
            import traceback
            traceback.print_exc()
    
    template = TEMPLATES.get('REGISTER_TEMPLATE', '''
    <html><head><title>Register</title></head><body>
    {% if message %}<p>{{ message }}</p>{% endif %}
    <form method="POST">
        <input type="text" name="teacher_name" placeholder="Teacher Name" required>
        <input type="tel" name="mobile_number" placeholder="Mobile Number" required>
        <input type="text" name="staff_number" placeholder="Staff Number (optional)">
        <input type="password" name="password" placeholder="Password" required>
        <input type="password" name="confirm_password" placeholder="Confirm Password" required>
        <button>Register</button>
    </form>
    </body></html>''')
    
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
        cursor.execute("SELECT COUNT(DISTINCT grade) FROM students")
        stats['total_classes'] = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error loading stats: {e}")
    
    teacher_name = session.get('teacher_name', session.get('username', 'Teacher'))
    
    template = TEMPLATES.get('DASHBOARD_TEMPLATE', '''
    <html><head><title>Dashboard</title></head><body>
    <h1>Dashboard</h1>
    <p>Welcome, {{ teacher_name }}!</p>
    <p>Students: {{ total_students }} | Exams: {{ total_exams }} | Subjects: {{ total_subjects }} | Classes: {{ total_classes }}</p>
    <a href="/logout">Logout</a>
    </body></html>''')
    
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
    session.clear()
    return redirect(url_for('login'))

@app.route('/check_results', methods=['GET', 'POST'])
def check_results():
    """Public page for checking exam results."""
    template = TEMPLATES.get('CHECK_RESULTS_TEMPLATE', '''
    <html><head><title>Check Results</title></head><body>
    <h1>Check Your Results</h1>
    <form method="POST">
        <input type="text" name="admission_number" placeholder="Admission Number" required>
        <input type="text" name="student_name" placeholder="Student Name" required>
        <button>Search</button>
    </form>
    </body></html>''')
    
    return render_template_string(template)

@app.route('/students')
def students_page():
    """Students management page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    grades = list(range(1, 10))
    template = TEMPLATES.get('STUDENTS_TEMPLATE', '''
    <html><head><title>Students</title></head><body>
    <h1>Students Management</h1>
    <p>Available grades: {{ grades }}</p>
    </body></html>''')
    
    return render_template_string(template, grades=grades)

@app.route('/teachers')
def teachers_page():
    """Teachers management page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    teachers = []
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT id, username, teacher_name, mobile_number, staff_number FROM teachers ORDER BY created_at DESC")
        teachers = [{'id': row[0], 'username': row[1], 'name': row[2], 'mobile': row[3], 'staff': row[4]} for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error loading teachers: {e}")
    
    template = TEMPLATES.get('TEACHERS_TEMPLATE', '''
    <html><head><title>Teachers</title></head><body>
    <h1>Teachers Management</h1>
    <p>Total: {{ total_teachers }}</p>
    </body></html>''')
    
    return render_template_string(template, teachers=teachers, total_teachers=len(teachers))

@app.errorhandler(500)
def error_500(e):
    """Handle 500 errors."""
    print(f"Error 500: {e}")
    import traceback
    traceback.print_exc()
    return "Server Error", 500

@app.errorhandler(404)
def error_404(e):
    """Handle 404 errors."""
    return "Page Not Found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
