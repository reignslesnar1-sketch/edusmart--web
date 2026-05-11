#!/usr/bin/env python
"""
EDUSMART - Online Exam Results Management System (Deployed)
This app imports and uses the EXACT website from the main exam_system.py
"""

import os
import sys
import sqlite3
import secrets
import traceback

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import Flask
try:
    from flask import Flask, render_template_string, request, redirect, url_for, session
except ImportError:
    print("ERROR: Flask not installed")
    sys.exit(1)

# Try to import templates - they should be in templates.py (no tkinter dependency)
print("Loading templates...")
try:
    # Import the templates file - this has ONLY HTML templates, no GUI
    import templates as template_module
    print("✓ Loaded templates module")
    HAS_TEMPLATES_MODULE = True
except ImportError as e:
    print(f"⚠ Could not import templates: {e}")
    HAS_TEMPLATES_MODULE = False

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
    """Hash password for storage."""
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
    """Verify teacher login."""
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
    """Save new teacher."""
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
    """Get teacher info."""
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
    """Generate unique username."""
    while True:
        username = f"teacher_{secrets.token_hex(4)}"
        conn, cursor = get_db_connection()
        cursor.execute("SELECT id FROM teachers WHERE username = ?", (username,))
        if not cursor.fetchone():
            return username

# ==================== GET TEMPLATES FROM EXAM_SYSTEM ====================

TEMPLATES = {}

if HAS_TEMPLATES_MODULE:
    # List of all template names from your system
    template_names = [
        'LOGIN_TEMPLATE', 'REGISTER_TEMPLATE', 'DASHBOARD_TEMPLATE',
        'WELCOME_TEMPLATE', 'CHECK_RESULTS_TEMPLATE', 'STUDENTS_TEMPLATE',
        'TEACHERS_TEMPLATE', 'FORGOT_PASSWORD_TEMPLATE', 'CANDIDATE_LOGIN_TEMPLATE',
        'CANDIDATE_DASHBOARD_TEMPLATE', 'SIDEBAR_PAGE_TEMPLATE', 'STUDENT_RESULTS_TEMPLATE',
        'CANDIDATE_PORTAL_TEMPLATE', 'SUBMIT_MARKS_TEMPLATE', 'VIEW_SUBMISSIONS_TEMPLATE'
    ]
    
    for template_name in template_names:
        try:
            if hasattr(template_module, template_name):
                template_content = getattr(template_module, template_name)
                TEMPLATES[template_name] = template_content
                print(f"  ✓ {template_name}")
        except Exception as e:
            print(f"  ⚠ Could not load {template_name}: {e}")

print(f"✓ Loaded {len(TEMPLATES)} templates")

# ==================== CREATE FLASK APP ====================

try:
    print("Creating Flask app...")
    app = Flask(__name__, static_folder='.')
    app.secret_key = secrets.token_hex(16)
    print("✓ Flask app created")

    # Add URL encoding filter
    print("Adding URL encoding filter...")
    from urllib.parse import quote as url_quote
    app.jinja_env.filters['urlencode'] = lambda s: url_quote(str(s))
    print("✓ URL filter added")

    # Initialize database
    print("Initializing database...")
    ensure_tables()
    print("✓ Database ready")
    
    print("✓ EDUSMART Web Server ready")
    print("=" * 60)

except Exception as e:
    print(f"✗ STARTUP ERROR: {e}")
    print(f"✗ Traceback: {traceback.format_exc()}")
    raise

# ==================== ROUTES ==================== 

@app.route('/')
def index():
    """Home page."""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    # Use WELCOME_TEMPLATE from exam_system
    template = TEMPLATES.get('WELCOME_TEMPLATE', '''
    <html>
    <head><title>EDUSMART</title>
    <style>
    body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; min-height: 100vh; }
    .container { max-width: 1000px; margin: 0 auto; background: white; padding: 50px; border-radius: 15px; text-align: center; }
    h1 { color: #667eea; font-size: 2.5em; }
    .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
    .btn:hover { opacity: 0.9; }
    </style>
    </head>
    <body>
    <div class="container">
    <h1>🎓 EDUSMART SOLUTIONS</h1>
    <p>Online Exam Results Management System</p>
    <div>
    <a href="/login" class="btn">👨‍🏫 Teacher Login</a>
    <a href="/register" class="btn">📝 Register Teacher</a>
    <a href="/candidate_login" class="btn">👨‍🎓 Student Portal</a>
    <a href="/check_results" class="btn">📊 Check Results</a>
    </div>
    </div>
    </body>
    </html>
    ''')
    
    return render_template_string(template, request=request)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Teacher login - EXACT from main system."""
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
    <h1>Teacher Login</h1>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <form method="POST">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button>Login</button>
    </form>
    </body></html>
    ''')
    
    return render_template_string(template, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Teacher registration - EXACT from main system."""
    message = None
    success = False
    generated_username = None
    
    if request.method == 'POST':
        try:
            teacher_name = request.form.get('teacher_name', '').strip()
            mobile_number = request.form.get('mobile_number', '').strip()
            staff_number = request.form.get('staff_number', '').strip() or None
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if not teacher_name or not mobile_number or not password or not confirm_password:
                message = '❌ Please complete all required fields'
            elif len(mobile_number) < 10:
                message = '❌ Mobile number should be at least 10 digits'
            elif password != confirm_password:
                message = '❌ Passwords do not match'
            elif len(password) < 6:
                message = '❌ Password should be at least 6 characters'
            else:
                generated_username = generate_teacher_username()
                if save_teacher_credentials(generated_username, password, teacher_name, mobile_number, staff_number):
                    success = True
                    message = f'✓ Account created! Username: <b>{generated_username}</b>'
                else:
                    message = '❌ Failed to create account - username may already exist'
        except Exception as e:
            message = f'❌ Error: {str(e)}'
            traceback.print_exc()
    
    template = TEMPLATES.get('REGISTER_TEMPLATE', '''
    <html><head><title>Register</title></head><body>
    <h1>Teacher Registration</h1>
    {% if message %}<p>{{ message|safe }}</p>{% endif %}
    <form method="POST">
    <input type="text" name="teacher_name" placeholder="Teacher Name" required>
    <input type="tel" name="mobile_number" placeholder="Mobile Number" required>
    <input type="text" name="staff_number" placeholder="Staff Number (optional)">
    <input type="password" name="password" placeholder="Password" required>
    <input type="password" name="confirm_password" placeholder="Confirm Password" required>
    <button>Register</button>
    </form>
    </body></html>
    ''')
    
    return render_template_string(template, message=message, success=success, generated_username=generated_username)

@app.route('/dashboard')
def dashboard():
    """Teacher dashboard - EXACT from main system."""
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
    <html><head><title>Dashboard</title></head><body>
    <h1>Dashboard</h1>
    <p>Welcome, {{ teacher_name }}!</p>
    <p>Students: {{ total_students }} | Exams: {{ total_exams }} | Subjects: {{ total_subjects }}</p>
    <a href="/logout">Logout</a>
    </body></html>
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
    session.clear()
    return redirect(url_for('login'))

@app.route('/check_results', methods=['GET', 'POST'])
def check_results():
    """Check results - EXACT from main system."""
    template = TEMPLATES.get('CHECK_RESULTS_TEMPLATE', '''
    <html><head><title>Check Results</title></head><body>
    <h1>Check Results</h1>
    <form method="POST">
    <input type="text" name="admission_number" placeholder="Admission Number" required>
    <input type="text" name="student_name" placeholder="Student Name" required>
    <button>Search</button>
    </form>
    <a href="/">← Home</a>
    </body></html>
    ''')
    
    return render_template_string(template)

@app.route('/candidate_login', methods=['GET', 'POST'])
def candidate_login():
    """Student/Candidate login - EXACT from main system."""
    template = TEMPLATES.get('CANDIDATE_LOGIN_TEMPLATE', '''
    <html><head><title>Student Portal</title></head><body>
    <h1>Student Portal - Grade 9 Candidates</h1>
    <form method="POST">
    <input type="text" name="admission_number" placeholder="Admission Number" required>
    <input type="text" name="student_name" placeholder="Student Name" required>
    <button>Access Portal</button>
    </form>
    <a href="/login">← Teacher Login</a>
    </body></html>
    ''')
    
    return render_template_string(template)

@app.route('/students')
def students_page():
    """Students management page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    template = TEMPLATES.get('STUDENTS_TEMPLATE', '<html><body><h1>Students</h1></body></html>')
    return render_template_string(template, grades=list(range(1, 10)))

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
    
    template = TEMPLATES.get('TEACHERS_TEMPLATE', '<html><body><h1>Teachers</h1></body></html>')
    return render_template_string(template, teachers=teachers, total_teachers=len(teachers))

@app.errorhandler(500)
def error_500(e):
    """Server error handler."""
    print(f"500 Error: {e}")
    traceback.print_exc()
    return '''<html><body>
    <h1>❌ Server Error</h1>
    <p>Please try again or contact support.</p>
    <a href="/">← Home</a>
    </body></html>''', 500

@app.errorhandler(404)
def error_404(e):
    """Not found handler."""
    return '''<html><body>
    <h1>❌ Page Not Found</h1>
    <a href="/">← Home</a>
    </body></html>''', 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
