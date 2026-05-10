"""
EDUSMART Solutions - Online Results Web Application
Standalone Flask Web Server for Render.com Deployment

This is a simplified version that works with the exam management system database.
"""

import os
import sqlite3
import secrets
from flask import Flask, render_template_string, request, redirect, url_for, session, send_file
from urllib.parse import quote as url_quote
import json
from datetime import datetime

# Initialize Flask App
app = Flask(__name__, static_folder='.')
app.secret_key = secrets.token_hex(16)

# Add URL encoding filter to Jinja2 environment
app.jinja_env.filters['urlencode'] = lambda s: url_quote(str(s))

# Alias for backward compatibility
web_app = app

# ==================== DATABASE CONFIG ====================
# Use DATABASE_URL from Render environment, or SQLite for local development
database_url = os.environ.get('DATABASE_URL')
DB_FILE = os.path.join(os.path.dirname(__file__), 'exam_system.db')

web_conn = None
web_cursor = None

def get_db_connection():
    """Get or create database connection"""
    global web_conn, web_cursor
    
    if web_conn is None:
        try:
            # For local development, use SQLite
            web_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
            web_cursor = web_conn.cursor()
            print(f"✓ Connected to database: {DB_FILE}")
        except Exception as e:
            print(f"✗ Database connection error: {e}")
            raise
    
    return web_conn, web_cursor

# ==================== DATABASE INITIALIZATION ====================
def ensure_tables():
    """Create database tables if they don't exist"""
    conn, cursor = get_db_connection()
    
    try:
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admission_number TEXT UNIQUE,
                student_name TEXT,
                assessment_number TEXT,
                level TEXT,
                grade INTEGER,
                stream TEXT,
                parent_phone TEXT,
                parent_id TEXT
            )
        """)
        
        # Teachers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                teacher_name TEXT,
                mobile_number TEXT,
                staff_number TEXT,
                admission_num TEXT,
                first_school TEXT,
                village TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Exams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id TEXT UNIQUE,
                name TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Subjects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        
        # Subject levels table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subject_levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER,
                level TEXT,
                grade INTEGER,
                FOREIGN KEY(subject_id) REFERENCES subjects(id)
            )
        """)
        
        # Results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject_id INTEGER,
                exam_id INTEGER,
                teacher_id INTEGER,
                marks INTEGER,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(subject_id) REFERENCES subjects(id),
                FOREIGN KEY(exam_id) REFERENCES exams(id),
                FOREIGN KEY(teacher_id) REFERENCES teachers(id)
            )
        """)
        
        # Candidate targets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidate_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject_id INTEGER,
                target REAL,
                UNIQUE(student_id, subject_id),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(subject_id) REFERENCES subjects(id)
            )
        """)
        
        conn.commit()
        print("✓ Database tables initialized")
    except Exception as e:
        print(f"✗ Error initializing tables: {e}")

# ==================== HELPER FUNCTIONS ====================
def hash_password(password):
    """Hash password using SHA256"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def verify_teacher_credentials(username, password):
    """Verify teacher login credentials"""
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT teacher_name, password_hash FROM teachers WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if row:
            teacher_name, password_hash = row
            if hash_password(password) == password_hash:
                return True, teacher_name
        
        return False, None
    except Exception as e:
        print(f"Error verifying credentials: {e}")
        return False, None

def get_teacher_info(username):
    """Get teacher information"""
    try:
        conn, cursor = get_db_connection()
        cursor.execute("""
            SELECT id, teacher_name, mobile_number, staff_number 
            FROM teachers WHERE username = ?
        """, (username,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'mobile': row[2],
                'staff_number': row[3]
            }
        return None
    except Exception as e:
        print(f"Error getting teacher info: {e}")
        return None

def save_teacher_credentials(username, password, teacher_name, mobile_number, staff_number=None):
    """Save new teacher credentials"""
    try:
        conn, cursor = get_db_connection()
        password_hash = hash_password(password)
        
        cursor.execute("""
            INSERT INTO teachers (username, password_hash, teacher_name, mobile_number, staff_number)
            VALUES (?, ?, ?, ?, ?)
        """, (username, password_hash, teacher_name, mobile_number, staff_number))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving teacher credentials: {e}")
        return False

def generate_teacher_username():
    """Generate a unique teacher username"""
    import random
    conn, cursor = get_db_connection()
    
    while True:
        username = f"teacher_{random.randint(100000, 999999)}"
        cursor.execute("SELECT id FROM teachers WHERE username = ?", (username,))
        if not cursor.fetchone():
            return username

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home/Welcome page"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    welcome_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EDUSMART SOLUTIONS - Online Results</title>
        <style>
            *, *::before, *::after { box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header {
                background: white;
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            }
            .school-name {
                color: #667eea;
                font-size: 2rem;
                font-weight: 700;
                margin: 0 0 10px 0;
            }
            .school-motto {
                color: #7f8c8d;
                font-size: 1.1rem;
                font-style: italic;
                margin: 0;
            }
            .content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }
            .card {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            }
            .card h2 {
                color: #2b3e50;
                font-size: 1.8rem;
                margin-top: 0;
                margin-bottom: 20px;
                text-align: center;
            }
            .action-buttons {
                display: flex;
                gap: 15px;
                margin-top: 25px;
                flex-wrap: wrap;
            }
            .btn {
                flex: 1;
                min-width: 150px;
                padding: 14px 24px;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                text-align: center;
                transition: all 0.3s ease;
                display: inline-block;
                border: none;
                cursor: pointer;
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .btn-primary:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
            }
            .btn-secondary {
                background: white;
                color: #667eea;
                border: 2px solid #667eea;
            }
            .btn-secondary:hover {
                background: #667eea;
                color: white;
            }
            .footer {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                text-align: center;
                padding: 20px;
                border-radius: 12px;
            }
            @media (max-width: 900px) {
                .content { grid-template-columns: 1fr; }
                .school-name { font-size: 1.5rem; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 class="school-name">🎓 EDUSMART SOLUTIONS</h1>
                <p class="school-motto">Online Exam Results Management System</p>
            </div>
            
            <div class="content">
                <div class="card">
                    <h2>📖 For Students & Parents</h2>
                    <p>Access your exam results securely using your admission number and name.</p>
                    <div class="action-buttons">
                        <a href="/check_results" class="btn btn-primary">Check Results</a>
                    </div>
                </div>
                
                <div class="card">
                    <h2>👨‍🏫 For Teachers</h2>
                    <p>Submit marks, manage students, and view detailed analytics.</p>
                    <div class="action-buttons">
                        <a href="/login" class="btn btn-primary">Teacher Login</a>
                        <a href="/register" class="btn btn-secondary">Create Account</a>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>🌐 Online Exam Results Management System | © 2024 EDUSMART SOLUTIONS</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(welcome_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Teacher login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        success, teacher_name = verify_teacher_credentials(username, password)
        if success:
            session['username'] = username
            session['teacher_name'] = teacher_name
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password"
            return render_template_string(LOGIN_TEMPLATE, error=error)
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Teacher registration"""
    message = None
    success = False
    
    if request.method == 'POST':
        teacher_name = request.form.get('teacher_name', '').strip()
        mobile_number = request.form.get('mobile_number', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not teacher_name or not mobile_number or not password:
            message = '❌ Please fill all required fields'
        elif password != confirm_password:
            message = '❌ Passwords do not match'
        elif len(password) < 6:
            message = '❌ Password must be at least 6 characters'
        else:
            username = generate_teacher_username()
            if save_teacher_credentials(username, password, teacher_name, mobile_number):
                success = True
                message = f'✓ Account created! Username: {username}'
            else:
                message = '❌ Failed to create account'
    
    return render_template_string(REGISTER_TEMPLATE, message=message, success=success)

@app.route('/dashboard')
def dashboard():
    """Teacher dashboard"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM exams")
        total_exams = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM subjects")
        total_subjects = cursor.fetchone()[0]
        
    except Exception as e:
        print(f"Error: {e}")
        total_students = total_exams = total_subjects = 0
    
    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - EDUSMART</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; background: #f5f5f5; }}
            .dashboard {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
            .header h1 {{ color: #667eea; }}
            .logout {{ background: #e74c3c; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; }}
            .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
            .stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .stat-card h3 {{ margin: 0; color: #999; font-size: 14px; }}
            .stat-card .number {{ font-size: 36px; font-weight: bold; color: #667eea; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <div>
                    <h1>🎓 Dashboard</h1>
                    <p>Welcome, {session.get('teacher_name', session.get('username'))}</p>
                </div>
                <a href="/logout" class="logout">Logout</a>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Students</h3>
                    <div class="number">{total_students}</div>
                </div>
                <div class="stat-card">
                    <h3>Total Exams</h3>
                    <div class="number">{total_exams}</div>
                </div>
                <div class="stat-card">
                    <h3>Total Subjects</h3>
                    <div class="number">{total_subjects}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(dashboard_html)

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/check_results', methods=['GET', 'POST'])
def check_results():
    """Student results page"""
    results = None
    error = None
    
    if request.method == 'POST':
        admission_number = request.form.get('admission_number', '').strip()
        student_name = request.form.get('student_name', '').strip()
        
        if admission_number and student_name:
            try:
                conn, cursor = get_db_connection()
                cursor.execute("""
                    SELECT s.student_name, s.admission_number, s.grade, s.stream,
                           sub.name, e.name, r.marks
                    FROM results r
                    JOIN students s ON r.student_id = s.id
                    JOIN subjects sub ON r.subject_id = sub.id
                    JOIN exams e ON r.exam_id = e.id
                    WHERE s.admission_number = ? AND s.student_name = ?
                    ORDER BY e.name, sub.name
                """, (admission_number, student_name))
                
                rows = cursor.fetchall()
                if rows:
                    results = rows
                else:
                    error = "No results found. Please check your admission number and name."
            except Exception as e:
                error = f"Error retrieving results: {str(e)}"
        else:
            error = "Please enter admission number and student name"
    
    results_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Check Results - EDUSMART</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            h1 {{ color: #667eea; text-align: center; }}
            .form-group {{ margin-bottom: 20px; }}
            label {{ display: block; margin-bottom: 8px; font-weight: bold; }}
            input {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
            button {{ background: #667eea; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }}
            button:hover {{ background: #764ba2; }}
            .error {{ color: #e74c3c; padding: 15px; background: #ffe0e0; border-radius: 5px; margin-bottom: 20px; }}
            .success {{ color: #27ae60; padding: 15px; background: #e0ffe0; border-radius: 5px; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #667eea; color: white; }}
            tr:hover {{ background: #f5f5f5; }}
            .home-link {{ text-align: center; margin-top: 20px; }}
            .home-link a {{ color: #667eea; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Check Your Results</h1>
            
            <form method="POST">
                <div class="form-group">
                    <label>Admission Number:</label>
                    <input type="text" name="admission_number" required>
                </div>
                <div class="form-group">
                    <label>Student Name:</label>
                    <input type="text" name="student_name" required>
                </div>
                <button type="submit">Search Results</button>
            </form>
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            
            {% if results %}
            <div class="success">
                <strong>✓ Results Found</strong> - {{ results[0][1] }} (Grade {{ results[0][2] }})
            </div>
            <table>
                <tr>
                    <th>Exam</th>
                    <th>Subject</th>
                    <th>Marks</th>
                </tr>
                {% for result in results %}
                <tr>
                    <td>{{ result[5] }}</td>
                    <td>{{ result[4] }}</td>
                    <td><strong>{{ result[6] }}</strong></td>
                </tr>
                {% endfor %}
            </table>
            {% endif %}
            
            <div class="home-link">
                <a href="/">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(results_html, error=error, results=results)

# ==================== HTML TEMPLATES ====================

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Teacher Login - EDUSMART</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
        .form-container {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); max-width: 400px; width: 100%; }}
        h1 {{ color: #667eea; text-align: center; margin-top: 0; }}
        .form-group {{ margin-bottom: 20px; }}
        label {{ display: block; margin-bottom: 8px; font-weight: bold; color: #333; }}
        input {{ width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }}
        input:focus {{ outline: none; border-color: #667eea; }}
        button {{ width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; }}
        button:hover {{ background: #764ba2; }}
        .error {{ color: #e74c3c; background: #ffe0e0; padding: 12px; border-radius: 5px; margin-bottom: 20px; }}
        .links {{ text-align: center; margin-top: 20px; }}
        .links a {{ color: #667eea; text-decoration: none; margin: 0 10px; }}
        .links a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="form-container">
        <h1>👨‍🏫 Teacher Login</h1>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="POST">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        
        <div class="links">
            <a href="/register">Create Account</a>
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
"""

REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Teacher Registration - EDUSMART</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
        .form-container {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); max-width: 400px; width: 100%; }}
        h1 {{ color: #667eea; text-align: center; margin-top: 0; }}
        .form-group {{ margin-bottom: 20px; }}
        label {{ display: block; margin-bottom: 8px; font-weight: bold; color: #333; }}
        input {{ width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }}
        input:focus {{ outline: none; border-color: #667eea; }}
        button {{ width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; }}
        button:hover {{ background: #764ba2; }}
        .message {{ padding: 12px; border-radius: 5px; margin-bottom: 20px; }}
        .error {{ color: #e74c3c; background: #ffe0e0; }}
        .success {{ color: #27ae60; background: #e0ffe0; }}
        .links {{ text-align: center; margin-top: 20px; }}
        .links a {{ color: #667eea; text-decoration: none; margin: 0 10px; }}
    </style>
</head>
<body>
    <div class="form-container">
        <h1>📝 Teacher Registration</h1>
        
        {% if message %}
        <div class="message {% if success %}success{% else %}error{% endif %}">{{ message }}</div>
        {% endif %}
        
        {% if not success %}
        <form method="POST">
            <div class="form-group">
                <label>Teacher Name:</label>
                <input type="text" name="teacher_name" required>
            </div>
            <div class="form-group">
                <label>Mobile Number:</label>
                <input type="tel" name="mobile_number" required>
            </div>
            <div class="form-group">
                <label>Password (min 6 characters):</label>
                <input type="password" name="password" required>
            </div>
            <div class="form-group">
                <label>Confirm Password:</label>
                <input type="password" name="confirm_password" required>
            </div>
            <button type="submit">Create Account</button>
        </form>
        {% endif %}
        
        <div class="links">
            <a href="/login">Already have account?</a>
            <a href="/">Back to Home</a>
        </div>
    </div>
</body>
</html>
"""

# ==================== INITIALIZATION ====================

if __name__ != '__main__':
    # Initialize on startup when running with gunicorn
    try:
        ensure_tables()
        print("✓ Web app initialized successfully")
    except Exception as e:
        print(f"✗ Initialization error: {e}")

if __name__ == '__main__':
    # For local development
    ensure_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)
