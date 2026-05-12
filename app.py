#!/usr/bin/env python
"""
EDUSMART - Online Exam Results Management System (Deployed)
This app imports and uses the EXACT website from the main exam_system.py
"""

print("[STARTUP] Python app starting...")

import os
import sys
import sqlite3
import secrets
import traceback

print(f"[STARTUP] Python version: {sys.version.split()[0]}")
print("[STARTUP] Core imports successful")

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import Flask
print("[STARTUP] Importing Flask...")
try:
    from flask import Flask, render_template_string, request, redirect, url_for, session
    print("[STARTUP] Flask imported successfully")
except ImportError as e:
    print(f"[STARTUP] ERROR: Flask not installed: {e}")
    sys.exit(1)

# Try to import templates - they should be in templates.py (no tkinter dependency)
print("[STARTUP] Loading templates module...")
try:
    # Import the templates file - this has ONLY HTML templates, no GUI
    import templates as template_module
    print("[STARTUP] âœ“ Loaded templates module")
    HAS_TEMPLATES_MODULE = True
except ImportError as e:
    print(f"âš  Could not import templates: {e}")
    HAS_TEMPLATES_MODULE = False

# Database configuration - use /tmp on servers, local folder on dev
import tempfile
if os.path.exists('/tmp'):
    # Server environment (Render, Linux)
    DB_FILE = '/tmp/exam_system.db'
else:
    # Local development (Windows)
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
                print(f"  âœ“ {template_name}")
        except Exception as e:
            print(f"  âš  Could not load {template_name}: {e}")

print(f"âœ“ Loaded {len(TEMPLATES)} templates")

# ==================== CREATE FLASK APP ====================

try:
    print("Creating Flask app...")
    app = Flask(__name__, static_folder='.')
    app.secret_key = secrets.token_hex(16)
    print("âœ“ Flask app created")

    # Add URL encoding filter
    print("Adding URL encoding filter...")
    from urllib.parse import quote as url_quote
    app.jinja_env.filters['urlencode'] = lambda s: url_quote(str(s))
    print("âœ“ URL filter added")

    # Initialize database
    print("Initializing database...")
    ensure_tables()
    print("âœ“ Database ready")
    
    print("âœ“ EDUSMART Web Server ready")
    print("=" * 60)

except Exception as e:
    print(f"âœ— STARTUP ERROR: {e}")
    print(f"âœ— Traceback: {traceback.format_exc()}")
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
    <h1>ðŸŽ“ EDUSMART SOLUTIONS</h1>
    <p>Online Exam Results Management System</p>
    <div>
    <a href="/login" class="btn">ðŸ‘¨â€ðŸ« Teacher Login</a>
    <a href="/register" class="btn">ðŸ“ Register Teacher</a>
    <a href="/candidate_login" class="btn">ðŸ‘¨â€ðŸŽ“ Student Portal</a>
    <a href="/check_results" class="btn">ðŸ“Š Check Results</a>
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
                message = 'âŒ Please complete all required fields'
            elif len(mobile_number) < 10:
                message = 'âŒ Mobile number should be at least 10 digits'
            elif password != confirm_password:
                message = 'âŒ Passwords do not match'
            elif len(password) < 6:
                message = 'âŒ Password should be at least 6 characters'
            else:
                generated_username = generate_teacher_username()
                if save_teacher_credentials(generated_username, password, teacher_name, mobile_number, staff_number):
                    success = True
                    message = f'âœ“ Account created! Username: <b>{generated_username}</b>'
                else:
                    message = 'âŒ Failed to create account - username may already exist'
        except Exception as e:
            message = f'âŒ Error: {str(e)}'
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
    
    enhanced_dashboard = '''
    <html>
    <head>
        <title>Dashboard - EDUSMART</title>
        <meta charset="UTF-8">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 40px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 20px;
            }
            h1 {
                color: #667eea;
                font-size: 2.5em;
            }
            .user-info {
                text-align: right;
            }
            .user-info .teacher-name {
                font-size: 1.3em;
                color: #333;
                font-weight: 600;
            }
            .user-info .username {
                color: #999;
                font-size: 0.9em;
                margin-top: 5px;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                text-align: center;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
            }
            .stat-card .icon {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .stat-card .label {
                font-size: 0.95em;
                opacity: 0.9;
                margin-bottom: 15px;
            }
            .stat-card .number {
                font-size: 2.8em;
                font-weight: bold;
                line-height: 1;
            }
            .menu-section {
                margin-bottom: 40px;
            }
            .menu-section h2 {
                color: #667eea;
                font-size: 1.4em;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #eee;
            }
            .menu-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
            }
            .menu-item {
                display: block;
                padding: 20px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #333;
                text-decoration: none;
                border-radius: 10px;
                text-align: center;
                font-weight: 600;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .menu-item:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .menu-item .icon {
                font-size: 2em;
                margin-bottom: 10px;
            }
            .menu-item .label {
                font-size: 0.9em;
            }
            .footer {
                margin-top: 50px;
                padding-top: 20px;
                border-top: 2px solid #eee;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 15px;
            }
            .btn-logout {
                padding: 12px 30px;
                background: #e74c3c;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: background 0.3s;
                border: none;
                cursor: pointer;
            }
            .btn-logout:hover {
                background: #c0392b;
            }
            .system-info {
                color: #999;
                font-size: 0.85em;
            }
            @media (max-width: 768px) {
                .container { padding: 20px; }
                h1 { font-size: 1.8em; }
                .header { flex-direction: column; gap: 20px; }
                .user-info { text-align: left; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 EDUSMART Dashboard</h1>
                <div class="user-info">
                    <div class="teacher-name">{{ teacher_name }}</div>
                    <div class="username">@{{ username }}</div>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="icon">👨‍🎓</div>
                    <div class="label">Total Students</div>
                    <div class="number">{{ total_students }}</div>
                </div>
                <div class="stat-card">
                    <div class="icon">📝</div>
                    <div class="label">Exams</div>
                    <div class="number">{{ total_exams }}</div>
                </div>
                <div class="stat-card">
                    <div class="icon">📚</div>
                    <div class="label">Subjects</div>
                    <div class="number">{{ total_subjects }}</div>
                </div>
            </div>
            
            <div class="menu-section">
                <h2>📊 Management</h2>
                <div class="menu-grid">
                    <a href="/students" class="menu-item">
                        <div class="icon">👥</div>
                        <div class="label">View All Students</div>
                    </a>
                    <a href="/teachers" class="menu-item">
                        <div class="icon">👨‍🏫</div>
                        <div class="label">View Teachers</div>
                    </a>
                    <a href="/submit_marks" class="menu-item">
                        <div class="icon">✍️</div>
                        <div class="label">Submit Marks</div>
                    </a>
                    <a href="/view_submissions" class="menu-item">
                        <div class="icon">📋</div>
                        <div class="label">View Submissions</div>
                    </a>
                </div>
            </div>
            
            <div class="menu-section">
                <h2>📈 Reports & Analysis</h2>
                <div class="menu-grid">
                    <a href="/student_reports" class="menu-item">
                        <div class="icon">📑</div>
                        <div class="label">Student Reports</div>
                    </a>
                    <a href="/notifications" class="menu-item">
                        <div class="icon">🔔</div>
                        <div class="label">Notifications</div>
                    </a>
                    <a href="/api/students" class="menu-item">
                        <div class="icon">📥</div>
                        <div class="label">Export Data (JSON)</div>
                    </a>
                </div>
            </div>
            
            <div class="footer">
                <div class="system-info">
                    EDUSMART v1.0 | School: KANGA SCHOOL | GitHub: reignslesnar1-sketch
                </div>
                <a href="/logout" class="btn-logout">🚪 Logout</a>
            </div>
        </div>
    </body>
    </html>
    '''
    
    template = TEMPLATES.get('DASHBOARD_TEMPLATE', enhanced_dashboard)
    return render_template_string(template,
        username=session['username'],
        teacher_name=teacher_name,
        total_students=stats['total_students'],
        total_exams=stats['total_exams'],
        total_subjects=stats['total_subjects'],
        total_classes=stats['total_classes'])

@app.route('/logout')
def logout():
    """Logout for both teachers and students."""
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
    <a href="/">â† Home</a>
    </body></html>
    ''')
    
    return render_template_string(template)

@app.route('/candidate_login', methods=['GET', 'POST'])
def candidate_login():
    """Student/Candidate login - EXACT from main system."""
    error = None
    
    if request.method == 'POST':
        admission_number = request.form.get('admission_number')
        password = request.form.get('password')
        
        try:
            conn, cursor = get_db_connection()
            cursor.execute("""
                SELECT id, student_name, grade, stream 
                FROM students 
                WHERE admission_number = ?
            """, (admission_number,))
            student = cursor.fetchone()
            
            if student:
                session['student_id'] = student[0]
                session['student_name'] = student[1]
                session['admission_number'] = admission_number
                session['grade'] = student[2]
                session['stream'] = student[3]
                return redirect(url_for('candidate_dashboard'))
            else:
                error = "Invalid admission number"
        except Exception as e:
            error = f"Login error: {str(e)}"
    
    template = TEMPLATES.get('CANDIDATE_LOGIN_TEMPLATE', '''
    <html><head><title>Student Portal</title></head><body>
    <h1>Student Portal - Grade 9 Candidates</h1>
    <form method="POST">
    <input type="text" name="admission_number" placeholder="Admission Number" required>
    <input type="password" name="password" placeholder="Password" required>
    <button>Access Portal</button>
    </form>
    <a href="/login">← Teacher Login</a>
    </body></html>
    ''')
    
    return render_template_string(template, error=error)

@app.route('/candidate_dashboard')
def candidate_dashboard():
    """Student portal dashboard - view results."""
    if 'student_id' not in session:
        return redirect(url_for('candidate_login'))
    
    results = []
    grouped_results = {}
    
    try:
        conn, cursor = get_db_connection()
        
        # Get student results
        cursor.execute("""
            SELECT 
                e.name as exam_name,
                sb.name as subject_name,
                r.marks
            FROM results r
            JOIN students s ON r.student_id = s.id
            JOIN exams e ON r.exam_id = e.id
            JOIN subjects sb ON r.subject_id = sb.id
            WHERE s.id = ?
            ORDER BY e.name, sb.name
        """, (session['student_id'],))
        
        rows = cursor.fetchall()
        
        # Group results by exam
        for row in rows:
            exam_name = row[0]
            if exam_name not in grouped_results:
                grouped_results[exam_name] = []
            grouped_results[exam_name].append((row[1], row[2]))
    
    except Exception as e:
        print(f"Error fetching results: {e}")
    
    template = TEMPLATES.get('CANDIDATE_DASHBOARD_TEMPLATE', '''
    <html><head><title>Student Results</title></head><body>
    <h1>Student Results</h1>
    <p>{{ student_name }}</p>
    <a href="/logout">Logout</a>
    </body></html>
    ''')
    
    return render_template_string(template,
        student_name=session.get('student_name', 'Student'),
        admission_number=session.get('admission_number', ''),
        grade=session.get('grade', ''),
        stream=session.get('stream', ''),
        results=results,
        grouped_results=grouped_results)

@app.route('/students')
def students_page():
    """Students management page with enhanced data."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    students = []
    total_students = 0
    grades = list(range(1, 13))  # Grades 1-12
    
    try:
        conn, cursor = get_db_connection()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        
        # Get all students sorted by grade
        cursor.execute("""
            SELECT id, student_name, admission_number, grade, stream, parent_phone 
            FROM students 
            ORDER BY grade, student_name
        """)
        
        students = [
            {
                'id': r[0],
                'student_name': r[1],
                'admission_number': r[2],
                'grade': r[3],
                'stream': r[4],
                'parent_phone': r[5]
            }
            for r in cursor.fetchall()
        ]
    except Exception as e:
        print(f"Error fetching students: {e}")
        pass
    
    # Enhanced HTML template for all students
    enhanced_template = '''
    <html>
    <head>
        <title>All Registered Students - EDUSMART</title>
        <meta charset="UTF-8">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                padding: 40px; 
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 20px;
            }
            h1 { 
                color: #667eea; 
                font-size: 2.2em;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .stats {
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }
            .stat-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                flex: 1;
                min-width: 150px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }
            .stat-box h3 { font-size: 0.9em; opacity: 0.9; margin-bottom: 10px; }
            .stat-box .number { font-size: 2.5em; font-weight: bold; }
            
            .search-filter {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            .search-filter input, .search-filter select {
                padding: 10px 15px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 0.95em;
                flex: 1;
                min-width: 200px;
            }
            .search-filter button {
                padding: 10px 25px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: background 0.3s;
            }
            .search-filter button:hover {
                background: #764ba2;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th {
                background: #667eea;
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: 600;
            }
            td {
                padding: 12px 15px;
                border-bottom: 1px solid #eee;
            }
            tr:hover {
                background: #f8f9ff;
            }
            .grade-badge {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
            }
            .stream-badge {
                display: inline-block;
                background: #764ba2;
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85em;
            }
            .action-buttons {
                display: flex;
                gap: 5px;
            }
            .btn-small {
                padding: 6px 12px;
                font-size: 0.85em;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                color: white;
                background: #667eea;
                transition: background 0.3s;
            }
            .btn-small:hover {
                background: #764ba2;
            }
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #eee;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 15px;
            }
            .btn-primary {
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            }
            .no-students {
                text-align: center;
                padding: 40px 20px;
                color: #999;
            }
            .no-students p { font-size: 1.1em; }
            @media (max-width: 768px) {
                .container { padding: 20px; }
                h1 { font-size: 1.5em; }
                table { font-size: 0.9em; }
                thead { display: none; }
                tr { display: block; margin-bottom: 20px; border: 1px solid #ddd; }
                td { display: block; text-align: right; padding-left: 50%; position: relative; }
                td:before { content: attr(data-label); position: absolute; left: 15px; font-weight: 600; color: #667eea; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Registered Students</h1>
                <span style="color: #999; font-size: 0.9em;">School: KANGA SCHOOL</span>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>Total Students</h3>
                    <div class="number">{{ total_students }}</div>
                </div>
                <div class="stat-box">
                    <h3>Grades Covered</h3>
                    <div class="number">{{ grades|length }}</div>
                </div>
            </div>
            
            <div class="search-filter">
                <input type="text" id="searchInput" placeholder="Search by name or admission number...">
                <select id="gradeFilter">
                    <option value="">All Grades</option>
                    {% for grade in grades %}
                    <option value="{{ grade }}">Grade {{ grade }}</option>
                    {% endfor %}
                </select>
                <button onclick="applyFilters()">🔍 Search</button>
            </div>
            
            {% if students %}
            <table id="studentTable">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Student Name</th>
                        <th>Admission No.</th>
                        <th>Grade</th>
                        <th>Stream</th>
                        <th>Parent Phone</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr class="student-row" data-grade="{{ student.grade }}" data-name="{{ student.student_name|lower }}" data-admission="{{ student.admission_number|lower }}">
                        <td data-label="#">{{ loop.index }}</td>
                        <td data-label="Student Name">{{ student.student_name }}</td>
                        <td data-label="Admission No.">{{ student.admission_number }}</td>
                        <td data-label="Grade"><span class="grade-badge">{{ student.grade }}</span></td>
                        <td data-label="Stream"><span class="stream-badge">{{ student.stream or 'N/A' }}</span></td>
                        <td data-label="Parent Phone">{{ student.parent_phone or 'N/A' }}</td>
                        <td data-label="Actions"><button class="btn-small">View</button></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="no-students">
                <p>📭 No students registered yet.</p>
                <p style="color: #ccc; margin-top: 10px;">Students will appear here once they are added to the system.</p>
            </div>
            {% endif %}
            
            <div class="footer">
                <a href="/dashboard" class="btn-primary">← Back to Dashboard</a>
                <a href="/api/students" class="btn-primary" style="background: #764ba2;">📥 Export as JSON</a>
                <span style="color: #999; font-size: 0.9em;">Students System Active</span>
            </div>
        </div>
        
        <script>
            function applyFilters() {
                const searchText = document.getElementById('searchInput').value.toLowerCase();
                const gradeFilter = document.getElementById('gradeFilter').value;
                const rows = document.querySelectorAll('.student-row');
                let visibleCount = 0;
                
                rows.forEach(row => {
                    const name = row.getAttribute('data-name');
                    const admission = row.getAttribute('data-admission');
                    const grade = row.getAttribute('data-grade');
                    
                    const nameMatch = name.includes(searchText) || admission.includes(searchText);
                    const gradeMatch = gradeFilter === '' || grade === gradeFilter;
                    
                    if (nameMatch && gradeMatch) {
                        row.style.display = '';
                        visibleCount++;
                    } else {
                        row.style.display = 'none';
                    }
                });
                
                if (visibleCount === 0) {
                    const tbody = document.querySelector('table tbody');
                    if (tbody) {
                        const tr = document.createElement('tr');
                        tr.innerHTML = '<td colspan="7" style="text-align: center; color: #999; padding: 30px;">No students found matching your criteria.</td>';
                        tbody.appendChild(tr);
                        setTimeout(() => tr.remove(), 3000);
                    }
                }
            }
            
            // Real-time search
            document.getElementById('searchInput')?.addEventListener('keyup', applyFilters);
        </script>
    </body>
    </html>
    '''
    
    template = TEMPLATES.get('STUDENTS_TEMPLATE', enhanced_template)
    return render_template_string(template, 
        grades=grades,
        students=students,
        total_students=total_students)

@app.route('/api/students')
def api_students():
    """API endpoint to get all registered students as JSON."""
    import json
    
    try:
        conn, cursor = get_db_connection()
        
        # Get all students
        cursor.execute("""
            SELECT id, student_name, admission_number, grade, stream, parent_phone
            FROM students 
            ORDER BY grade, student_name
        """)
        
        students_data = []
        for row in cursor.fetchall():
            students_data.append({
                'id': row[0],
                'student_name': row[1],
                'admission_number': row[2],
                'grade': row[3],
                'stream': row[4],
                'parent_phone': row[5]
            })
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM students")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT grade) FROM students")
        total_grades = cursor.fetchone()[0]
        
        return {
            'success': True,
            'total_students': total_count,
            'grades_covered': total_grades,
            'students': students_data,
            'metadata': {
                'school': 'KANGA SCHOOL',
                'system': 'EDUSMART',
                'github_username': 'reignslesnar1-sketch'
            }
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }, 500

@app.route('/teachers')
    """Teachers management page with enhanced data."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    teachers = []
    total_teachers = 0
    
    try:
        conn, cursor = get_db_connection()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM teachers")
        total_teachers = cursor.fetchone()[0]
        
        # Get all teachers
        cursor.execute("""
            SELECT id, teacher_name, username, mobile_number, staff_number 
            FROM teachers 
            ORDER BY teacher_name
        """)
        
        teachers = [
            {
                'id': r[0],
                'teacher_name': r[1],
                'username': r[2],
                'mobile_number': r[3],
                'staff_number': r[4]
            }
            for r in cursor.fetchall()
        ]
    except Exception as e:
        print(f"Error fetching teachers: {e}")
        pass
    
    template = TEMPLATES.get('TEACHERS_TEMPLATE', '<html><body><h1>Teachers</h1></body></html>')
    return render_template_string(template, 
        teachers=teachers, 
        total_teachers=total_teachers)

@app.route('/submit_marks', methods=['GET', 'POST'])
def submit_marks():
    """Submit exam marks page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    students = []
    exams = []
    subjects = []
    message = ''
    success = False
    
    try:
        conn, cursor = get_db_connection()
        
        # Get students
        cursor.execute("SELECT id, student_name, admission_number FROM students ORDER BY student_name")
        students = [{'id': r[0], 'student_name': r[1], 'admission_number': r[2]} for r in cursor.fetchall()]
        
        # Get exams
        cursor.execute("SELECT id, name FROM exams ORDER BY name")
        exams = [{'id': r[0], 'name': r[1]} for r in cursor.fetchall()]
        
        # Get subjects
        cursor.execute("SELECT id, name FROM subjects ORDER BY name")
        subjects = [{'id': r[0], 'name': r[1]} for r in cursor.fetchall()]
        
        if request.method == 'POST':
            student_id = request.form.get('student_id')
            exam_id = request.form.get('exam_id')
            
            # Insert marks for each subject
            for subject in subjects:
                marks = request.form.get(f"marks_{subject['id']}")
                if marks:
                    try:
                        cursor.execute("""
                            INSERT OR REPLACE INTO results 
                            (student_id, subject_id, exam_id, marks) 
                            VALUES (?, ?, ?, ?)
                        """, (student_id, subject['id'], exam_id, int(marks)))
                    except:
                        pass
            
            conn.commit()
            success = True
            message = "✅ Marks submitted successfully!"
    
    except Exception as e:
        print(f"Error in submit_marks: {e}")
        message = f"Error: {str(e)}"
    
    template = TEMPLATES.get('SUBMIT_MARKS_TEMPLATE', '<html><body><h1>Submit Marks</h1></body></html>')
    return render_template_string(template,
        students=students,
        exams=exams,
        subjects=subjects,
        message=message,
        success=success)

@app.route('/view_submissions')
def view_submissions():
    """View mark submissions page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    submissions = []
    
    try:
        conn, cursor = get_db_connection()
        cursor.execute("""
            SELECT 
                r.id,
                s.student_name,
                s.admission_number,
                e.name as exam_name,
                sb.name as subject_name,
                r.marks
            FROM results r
            JOIN students s ON r.student_id = s.id
            JOIN exams e ON r.exam_id = e.id
            JOIN subjects sb ON r.subject_id = sb.id
            ORDER BY s.student_name, e.name, sb.name
        """)
        
        submissions = [
            {
                'id': r[0],
                'student_name': r[1],
                'admission_number': r[2],
                'exam_name': r[3],
                'subject_name': r[4],
                'marks': r[5]
            }
            for r in cursor.fetchall()
        ]
    except Exception as e:
        print(f"Error fetching submissions: {e}")
    
    template = TEMPLATES.get('VIEW_SUBMISSIONS_TEMPLATE', '<html><body><h1>View Submissions</h1></body></html>')
    return render_template_string(template, submissions=submissions)

@app.route('/student_reports')
def student_reports():
    """Student reports page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template_string('''
    <html><head><title>Student Reports</title><meta charset="UTF-8"></head>
    <body style="font-family: Arial; padding: 20px; background: #f6f8fa;">
    <div style="max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px;">
        <h1>📑 Student Reports</h1>
        <p style="color: #7f8c8d;">Reports functionality will be implemented here.</p>
        <a href="/dashboard" style="color: #2e86de; text-decoration: none; font-weight: 600;">← Back to Dashboard</a>
    </div>
    </body></html>
    ''')

@app.route('/notifications')
def notifications():
    """Notifications page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template_string('''
    <html><head><title>Notifications</title><meta charset="UTF-8"></head>
    <body style="font-family: Arial; padding: 20px; background: #f6f8fa;">
    <div style="max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px;">
        <h1>🔔 Notifications</h1>
        <p style="color: #7f8c8d;">System notifications will appear here.</p>
        <a href="/dashboard" style="color: #2e86de; text-decoration: none; font-weight: 600;">← Back to Dashboard</a>
    </div>
    </body></html>
    ''')

@app.errorhandler(500)
def error_500(e):
    """Server error handler."""
    print(f"500 Error: {e}")
    traceback.print_exc()
    return '''<html><body>
    <h1>âŒ Server Error</h1>
    <p>Please try again or contact support.</p>
    <a href="/">â† Home</a>
    </body></html>''', 500

@app.errorhandler(404)
def error_404(e):
    """Not found handler."""
    return '''<html><body>
    <h1>âŒ Page Not Found</h1>
    <a href="/">â† Home</a>
    </body></html>''', 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
