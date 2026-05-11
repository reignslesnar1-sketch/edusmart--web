# Pure HTML/CSS/JavaScript Templates - No Dependencies
# This file contains all extracted templates from exam_system.py
# No tkinter, no GUI libraries - works perfectly on Linux (Render)

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Exam Management System</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-container { background: white; padding: 50px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); width: 100%; max-width: 450px; }
        .logo { text-align: center; margin-bottom: 30px; font-size: 3rem; }
        h1 { text-align: center; color: #2b3e50; margin: 0 0 10px 0; font-size: 2rem; }
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #2b3e50; }
        input[type="text"], input[type="password"] { width: 100%; padding: 14px; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 16px; box-sizing: border-box; }
        input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        button { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 10px; }
        button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102,126,234,0.3); }
        .error { color: #e74c3c; margin-top: 10px; text-align: center; }
        .register-link { text-align: center; margin-top: 20px; }
        .register-link a { color: #667eea; text-decoration: none; font-weight: 600; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">📊</div>
        <h1>EDUSMART</h1>
        <p class="subtitle">Exam Management System</p>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <div class="register-link">
            Don't have an account? <a href="/register">Register here</a>
        </div>
    </div>
</body>
</html>
"""

CANDIDATE_LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Portal Login</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-container { background: white; padding: 50px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); width: 100%; max-width: 450px; }
        .logo { text-align: center; margin-bottom: 30px; font-size: 3rem; }
        h1 { text-align: center; color: #2b3e50; margin: 0 0 10px 0; font-size: 2rem; }
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #2b3e50; }
        input[type="text"], input[type="password"] { width: 100%; padding: 14px; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 16px; box-sizing: border-box; }
        input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        button { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 10px; }
        button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102,126,234,0.3); }
        .error { color: #e74c3c; margin-top: 10px; text-align: center; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">👨‍🎓</div>
        <h1>Student Portal</h1>
        <p class="subtitle">Grade 9 Candidates</p>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        <form method="POST">
            <div class="form-group">
                <label for="admission_number">Admission Number</label>
                <input type="text" id="admission_number" name="admission_number" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login to Portal</button>
        </form>
    </div>
</body>
</html>
"""

FORGOT_PASSWORD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forgot Password - Exam Management System</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: white; padding: 50px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); width: 100%; max-width: 450px; }
        .logo { text-align: center; margin-bottom: 30px; font-size: 3rem; }
        h1 { text-align: center; color: #2b3e50; margin: 0; font-size: 1.8rem; }
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #2b3e50; }
        input[type="text"] { width: 100%; padding: 14px; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 16px; box-sizing: border-box; }
        input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        button { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 10px; }
        button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102,126,234,0.3); }
        .message { text-align: center; margin-top: 10px; padding: 10px; border-radius: 10px; }
        .success { background: #d4edda; color: #0b6623; }
        .error { background: #f8d7da; color: #842029; }
        .back-link { text-align: center; margin-top: 20px; }
        .back-link a { color: #667eea; text-decoration: none; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🔑</div>
        <h1>Forgot Password</h1>
        <p class="subtitle">Reset your password</p>
        {% if message %}<div class="message {% if 'successfully' in message %}success{% else %}error{% endif %}">{{ message }}</div>{% endif %}
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Enter your username" required>
            </div>
            <button type="submit">Reset Password</button>
        </form>
        <div class="back-link">
            <a href="/login">← Back to Login</a>
        </div>
    </div>
</body>
</html>
"""

REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - Exam Management System</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; min-height: 100vh; }
        .register-container { background: white; padding: 50px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); width: 100%; max-width: 500px; margin: 0 auto; }
        .logo { text-align: center; margin-bottom: 20px; font-size: 2.5rem; }
        h1 { text-align: center; color: #2b3e50; margin: 0 0 10px 0; font-size: 1.8rem; }
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 25px; }
        .form-group { margin-bottom: 18px; }
        label { display: block; margin-bottom: 6px; font-weight: 600; color: #2b3e50; font-size: 0.95rem; }
        input[type="text"], input[type="email"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 15px; box-sizing: border-box; }
        input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        button { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 15px; }
        button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102,126,234,0.3); }
        .message { padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
        .success { background: #d4edda; color: #0b6623; }
        .error { background: #f8d7da; color: #842029; }
        .login-link { text-align: center; margin-top: 20px; }
        .login-link a { color: #667eea; text-decoration: none; font-weight: 600; }
    </style>
</head>
<body>
    <div class="register-container">
        <div class="logo">📝</div>
        <h1>Register</h1>
        <p class="subtitle">Create your teacher account</p>
        {% if message %}<div class="message {% if 'success' in message.lower() or 'successfully' in message.lower() %}success{% else %}error{% endif %}">{{ message }}</div>{% endif %}
        <form method="POST">
            <div class="form-group">
                <label for="teacher_name">Full Name</label>
                <input type="text" id="teacher_name" name="teacher_name" required>
            </div>
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required minlength="6">
            </div>
            <div class="form-group">
                <label for="confirm_password">Confirm Password</label>
                <input type="password" id="confirm_password" name="confirm_password" required minlength="6">
            </div>
            <div class="form-group">
                <label for="staff_number">Staff Number (Optional)</label>
                <input type="text" id="staff_number" name="staff_number">
            </div>
            <div class="form-group">
                <label for="school">School Name</label>
                <input type="text" id="school" name="school" required>
            </div>
            <button type="submit">Create Account</button>
        </form>
        <div class="login-link">
            Already have an account? <a href="/login">Login here</a>
        </div>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Exam Management System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f6f8fa; 
            color: #2b3e50;
            min-height: 100vh; 
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* Header Section */
        .header { 
            background: linear-gradient(135deg, #2e86de 0%, #1f6aa2 100%); 
            color: white; 
            padding: 40px; 
            border-radius: 16px; 
            margin-bottom: 30px; 
            box-shadow: 0 8px 24px rgba(46, 134, 222, 0.25);
        }
        .header-top { display: flex; justify-content: space-between; align-items: center; }
        .header h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 5px; }
        .header p { font-size: 1rem; opacity: 0.95; }
        .logout-btn { 
            background: #e74c3c; 
            color: white; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 8px; 
            text-decoration: none; 
            font-weight: 600; 
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.95rem;
        }
        .logout-btn:hover { background: #c0392b; transform: translateY(-2px); }
        
        /* Stats Grid */
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); 
            gap: 20px; 
            margin-bottom: 40px; 
        }
        .stat-card { 
            background: white; 
            padding: 30px; 
            border-radius: 12px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.08); 
            border-left: 5px solid #2e86de;
            transition: all 0.3s ease;
        }
        .stat-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 8px 25px rgba(0,0,0,0.12); 
        }
        .stat-card.green { border-left-color: #2ecc71; }
        .stat-card.orange { border-left-color: #f39c12; }
        .stat-card.purple { border-left-color: #9b59b6; }
        .stat-card h3 { 
            font-size: 0.9rem; 
            color: #7f8c8d; 
            font-weight: 600; 
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .stat-value { 
            font-size: 3rem; 
            font-weight: 700; 
            color: #2e86de; 
        }
        .stat-card.green .stat-value { color: #2ecc71; }
        .stat-card.orange .stat-value { color: #f39c12; }
        .stat-card.purple .stat-value { color: #9b59b6; }
        
        /* Section Title */
        .section-title { 
            font-size: 1.8rem; 
            font-weight: 700; 
            color: #2b3e50; 
            margin-bottom: 25px;
            margin-top: 30px;
            display: flex;
            align-items: center;
        }
        .section-title::before {
            content: '';
            width: 4px;
            height: 30px;
            background: #2e86de;
            border-radius: 2px;
            margin-right: 15px;
        }
        
        /* Navigation Cards */
        .nav-section { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); 
            gap: 20px; 
        }
        .nav-card { 
            background: white; 
            padding: 30px; 
            border-radius: 12px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.08); 
            text-decoration: none; 
            color: #2b3e50; 
            transition: all 0.3s ease;
            border-top: 4px solid #2e86de;
            display: flex;
            flex-direction: column;
        }
        .nav-card:hover { 
            transform: translateY(-8px); 
            box-shadow: 0 12px 30px rgba(0,0,0,0.15);
            border-top-color: #1f6aa2;
        }
        .nav-card.green { border-top-color: #2ecc71; }
        .nav-card.green:hover { border-top-color: #27ae60; }
        .nav-card.orange { border-top-color: #f39c12; }
        .nav-card.orange:hover { border-top-color: #d68910; }
        .nav-card.purple { border-top-color: #9b59b6; }
        .nav-card.purple:hover { border-top-color: #8e44ad; }
        .nav-card.red { border-top-color: #e74c3c; }
        .nav-card.red:hover { border-top-color: #c0392b; }
        
        .nav-icon { 
            font-size: 2.8rem; 
            margin-bottom: 15px;
            display: inline-block;
            width: 60px;
            height: 60px;
            background: #f0f4ff;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .nav-card.green .nav-icon { background: #f0fff4; }
        .nav-card.orange .nav-icon { background: #fffaf0; }
        .nav-card.purple .nav-icon { background: #faf5ff; }
        .nav-card.red .nav-icon { background: #fff5f5; }
        
        .nav-card h3 { 
            margin: 10px 0 8px 0; 
            font-size: 1.2rem;
            font-weight: 700;
        }
        .nav-card p { 
            margin: 0; 
            font-size: 0.9rem; 
            color: #7f8c8d;
            flex-grow: 1;
        }
        .nav-card::after {
            content: '→';
            margin-top: 15px;
            font-size: 1.3rem;
            color: #2e86de;
            align-self: flex-start;
        }
        .nav-card.green::after { color: #2ecc71; }
        .nav-card.orange::after { color: #f39c12; }
        .nav-card.purple::after { color: #9b59b6; }
        .nav-card.red::after { color: #e74c3c; }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header { padding: 30px; margin-bottom: 20px; }
            .header h1 { font-size: 1.8rem; }
            .header-top { flex-direction: column; gap: 15px; }
            .stats-grid { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
            .stat-card { padding: 20px; }
            .stat-value { font-size: 2rem; }
            .nav-section { grid-template-columns: 1fr; }
            .section-title { font-size: 1.3rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-top">
                <div>
                    <h1>Welcome, {{ username }}! 👋</h1>
                    <p>Exam Management System Dashboard</p>
                </div>
                <a href="/logout" class="logout-btn">🚪 Logout</a>
            </div>
        </div>

        <h2 class="section-title">📊 System Overview</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Students</h3>
                <div class="stat-value">{{ total_students }}</div>
            </div>
            <div class="stat-card green">
                <h3>Exams</h3>
                <div class="stat-value">{{ total_exams }}</div>
            </div>
            <div class="stat-card orange">
                <h3>Subjects</h3>
                <div class="stat-value">{{ total_subjects }}</div>
            </div>
            <div class="stat-card purple">
                <h3>Classes</h3>
                <div class="stat-value">{{ total_classes }}</div>
            </div>
        </div>

        <h2 class="section-title">⚡ Quick Access</h2>
        <div class="nav-section">
            <a href="/students" class="nav-card">
                <div class="nav-icon">👨‍🎓</div>
                <h3>Manage Students</h3>
                <p>Add, edit, or view student information and records</p>
            </a>
            <a href="/submit_marks" class="nav-card green">
                <div class="nav-icon">📝</div>
                <h3>Submit Marks</h3>
                <p>Enter and manage exam results for students</p>
            </a>
            <a href="/view_submissions" class="nav-card orange">
                <div class="nav-icon">📊</div>
                <h3>View Submissions</h3>
                <p>Review and edit student marks and scores</p>
            </a>
            <a href="/student_reports" class="nav-card purple">
                <div class="nav-icon">📑</div>
                <h3>Student Reports</h3>
                <p>View student performance and analytics</p>
            </a>
            <a href="/teachers" class="nav-card">
                <div class="nav-icon">👨‍🏫</div>
                <h3>Teachers</h3>
                <p>Manage and view registered teachers</p>
            </a>
            <a href="/notifications" class="nav-card red">
                <div class="nav-icon">🔔</div>
                <h3>Notifications</h3>
                <p>System notifications and documents</p>
            </a>
        </div>
    </div>
</body>
</html>
"""

STUDENTS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Students - Exam Management System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f6f8fa; 
            color: #2b3e50;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* Breadcrumb Navigation */
        .breadcrumb { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 25px;
            align-items: center;
            font-size: 0.95rem;
        }
        .breadcrumb a { 
            color: #2e86de; 
            text-decoration: none; 
            font-weight: 600;
            transition: color 0.3s;
        }
        .breadcrumb a:hover { color: #1f6aa2; }
        .breadcrumb span { color: #95a5a6; }
        
        /* Header Section */
        .header { 
            background: white; 
            padding: 30px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }
        .header-top { 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            margin-bottom: 20px;
        }
        .header h1 { 
            font-size: 2rem; 
            font-weight: 700;
            color: #2b3e50;
            margin: 0;
        }
        .header-actions { 
            display: flex; 
            gap: 10px;
        }
        .action-btn { 
            padding: 12px 20px; 
            border: none; 
            border-radius: 8px; 
            text-decoration: none; 
            color: white; 
            font-weight: 600; 
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.95rem;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-primary { background: #2e86de; }
        .btn-primary:hover { background: #1f6aa2; transform: translateY(-2px); }
        .btn-secondary { background: #95a5a6; }
        .btn-secondary:hover { background: #7f8c8d; }
        .btn-success { background: #2ecc71; }
        .btn-success:hover { background: #27ae60; }
        
        /* Filter & Search Section */
        .filter-section { 
            background: white; 
            padding: 25px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }
        .filter-title { 
            font-size: 1.1rem; 
            font-weight: 700;
            margin-bottom: 15px;
            color: #2b3e50;
        }
        .grade-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); 
            gap: 12px;
            margin-bottom: 20px;
        }
        .grade-btn { 
            padding: 14px; 
            background: #f0f4ff; 
            border: 2px solid #dbe9ff; 
            border-radius: 10px; 
            text-decoration: none; 
            color: #2e86de; 
            font-weight: 600; 
            text-align: center; 
            cursor: pointer; 
            transition: all 0.3s;
            font-size: 0.95rem;
        }
        .grade-btn:hover { 
            background: #dbe9ff; 
            border-color: #2e86de;
            transform: translateY(-2px);
        }
        .grade-btn.active { 
            background: #2e86de; 
            color: white; 
            border-color: #2e86de;
        }
        
        /* Search Bar */
        .search-container {
            display: flex;
            gap: 12px;
            margin-top: 15px;
        }
        .search-input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            font-size: 0.95rem;
            transition: all 0.3s;
        }
        .search-input:focus {
            outline: none;
            border-color: #2e86de;
            box-shadow: 0 0 0 3px rgba(46, 134, 222, 0.1);
        }
        .search-btn {
            padding: 12px 24px;
            background: #2e86de;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .search-btn:hover { background: #1f6aa2; }
        
        /* Stats Bar */
        .stats-bar { 
            display: flex; 
            gap: 20px; 
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .stats-bar div { 
            background: white; 
            padding: 15px 25px; 
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            font-weight: 600;
            color: #7f8c8d;
        }
        .stats-bar .value { 
            color: #2e86de; 
            font-size: 1.3rem;
            font-weight: 700;
        }
        
        /* Table Section */
        .table-section { 
            background: white; 
            padding: 0; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        .table-header { 
            padding: 25px; 
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .table-header h2 { 
            margin: 0; 
            font-size: 1.3rem;
            color: #2b3e50;
        }
        .view-toggle { 
            display: flex; 
            gap: 8px;
        }
        .toggle-btn { 
            padding: 8px 12px; 
            border: 1px solid #e9ecef; 
            background: white; 
            border-radius: 6px; 
            cursor: pointer;
            color: #7f8c8d;
            transition: all 0.2s;
        }
        .toggle-btn.active { 
            background: #2e86de; 
            color: white; 
            border-color: #2e86de;
        }
        
        /* Table Styles */
        .students-table { 
            width: 100%; 
            border-collapse: collapse;
        }
        .students-table thead { 
            background: #f8fbff; 
        }
        .students-table th { 
            padding: 15px 25px; 
            text-align: left; 
            font-weight: 700; 
            color: #2b3e50;
            border-bottom: 2px solid #e9ecef;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .students-table td { 
            padding: 15px 25px; 
            border-bottom: 1px solid #e9ecef;
        }
        .students-table tbody tr { 
            transition: background 0.2s;
        }
        .students-table tbody tr:hover { 
            background: #f8fbff; 
        }
        .students-table tbody tr:last-child td {
            border-bottom: none;
        }
        
        /* Name Column */
        .student-name {
            font-weight: 700;
            color: #2b3e50;
        }
        .student-admission {
            color: #7f8c8d;
            font-size: 0.9rem;
        }
        
        /* Action Buttons */
        .actions-cell { 
            display: flex; 
            gap: 8px;
        }
        .row-action { 
            padding: 6px 12px; 
            border: none; 
            border-radius: 6px; 
            text-decoration: none; 
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s;
            display: inline-block;
        }
        .edit-btn { 
            background: #2e86de; 
            color: white; 
        }
        .edit-btn:hover { 
            background: #1f6aa2; 
        }
        .delete-btn { 
            background: #e74c3c; 
            color: white; 
        }
        .delete-btn:hover { 
            background: #c0392b; 
        }
        .view-btn { 
            background: #2ecc71; 
            color: white; 
        }
        .view-btn:hover { 
            background: #27ae60; 
        }
        
        /* Empty State */
        .empty-state { 
            text-align: center; 
            padding: 60px 20px;
            color: #7f8c8d;
        }
        .empty-state h3 { 
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: #95a5a6;
        }
        .empty-state p { 
            margin: 0;
            font-size: 0.95rem;
        }
        
        /* Pagination */
        .pagination { 
            display: flex; 
            justify-content: center; 
            gap: 8px; 
            padding: 20px; 
            background: white;
            margin-top: 20px;
            border-radius: 8px;
        }
        .pagination a, .pagination span { 
            padding: 8px 12px; 
            border: 1px solid #e9ecef; 
            border-radius: 6px; 
            text-decoration: none; 
            color: #2e86de;
            font-weight: 600;
            transition: all 0.2s;
        }
        .pagination a:hover { 
            background: #2e86de; 
            color: white;
        }
        .pagination .current { 
            background: #2e86de; 
            color: white; 
            border-color: #2e86de;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header-top { flex-direction: column; gap: 15px; align-items: flex-start; }
            .header-actions { flex-wrap: wrap; }
            .grade-grid { grid-template-columns: repeat(2, 1fr); }
            .search-container { flex-direction: column; }
            .students-table { font-size: 0.9rem; }
            .students-table th, .students-table td { padding: 12px 10px; }
            .actions-cell { flex-direction: column; }
            .row-action { width: 100%; text-align: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Breadcrumb -->
        <div class="breadcrumb">
            <a href="/dashboard">📊 Dashboard</a>
            <span>/</span>
            <span>👨‍🎓 Students</span>
        </div>
        
        <div class="header">
            <div class="header-top">
                <h1>👨‍🎓 Student Management</h1>
                <div class="header-actions">
                    <a href="/add_student" class="action-btn btn-success">➕ Add New Student</a>
                    <a href="/import_students" class="action-btn btn-primary">📥 Import Students</a>
                </div>
            </div>
        </div>
        
        <!-- Filters -->
        <div class="filter-section">
            <div class="filter-title">📚 Filter by Grade</div>
            <div class="grade-grid">
                {% for grade in grades %}
                <a href="/students?grade={{ grade }}" class="grade-btn">Grade {{ grade }}</a>
                {% endfor %}
            </div>
            
            <div class="filter-title" style="margin-top: 20px;">🔍 Search Students</div>
            <div class="search-container">
                <input type="text" class="search-input" id="searchInput" placeholder="Search by name, admission number, or stream...">
                <button class="search-btn" id="searchBtn">Search</button>
            </div>
        </div>
        
        <!-- Stats -->
        <div class="stats-bar">
            <div>Total Students: <span class="value">{{ total_students }}</span></div>
            <div>Displaying: <span class="value">{{ students|length if students else 0 }}</span></div>
        </div>
        
        <!-- Table -->
        <div class="table-section">
            <div class="table-header">
                <h2>📋 Student Records</h2>
            </div>
            
            {% if students %}
            <table class="students-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Student Name</th>
                        <th>Admission #</th>
                        <th>Grade</th>
                        <th>Stream</th>
                        <th>Contact</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>
                            <div class="student-name">{{ student.student_name }}</div>
                        </td>
                        <td><span class="student-admission">{{ student.admission_number }}</span></td>
                        <td>{{ student.grade }}</td>
                        <td>{{ student.stream or '—' }}</td>
                        <td>{{ student.parent_phone[:4] if student.parent_phone else '—' }}...</td>
                        <td>
                            <div class="actions-cell">
                                <a href="/view_student/{{ student.id }}" class="row-action view-btn">👁️ View</a>
                                <a href="/edit_student/{{ student.id }}" class="row-action edit-btn">✏️ Edit</a>
                                <a href="/delete_student/{{ student.id }}" class="row-action delete-btn" onclick="return confirm('Are you sure you want to delete {{ student.student_name }}?');">🗑️ Delete</a>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                <h3>📭 No Students Found</h3>
                <p>Select a grade above or try a different search</p>
            </div>
            {% endif %}
        </div>
    </div>
    
    <script>
        document.getElementById('searchBtn').addEventListener('click', function() {
            const searchValue = document.getElementById('searchInput').value.toLowerCase();
            const rows = document.querySelectorAll('.students-table tbody tr');
            
            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(searchValue) ? '' : 'none';
            });
        });
        
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('searchBtn').click();
            }
        });
    </script>
</body>
</html>
"""

# Additional templates will be added here
# This file is designed to grow as more templates are extracted

TEACHERS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teachers - Exam Management System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f6f8fa; 
            color: #2b3e50;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* Breadcrumb Navigation */
        .breadcrumb { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 25px;
            align-items: center;
            font-size: 0.95rem;
        }
        .breadcrumb a { 
            color: #2e86de; 
            text-decoration: none; 
            font-weight: 600;
        }
        .breadcrumb a:hover { color: #1f6aa2; }
        .breadcrumb span { color: #95a5a6; }
        
        /* Header */
        .header { 
            background: white; 
            padding: 30px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { 
            font-size: 2rem; 
            font-weight: 700;
            color: #2b3e50;
            margin: 0;
        }
        .btn-primary { 
            padding: 12px 24px; 
            background: #2e86de; 
            color: white; 
            text-decoration: none; 
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary:hover { background: #1f6aa2; transform: translateY(-2px); }
        
        /* Stats */
        .stats-bar { 
            background: white; 
            padding: 20px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }
        .stat { 
            display: flex; 
            align-items: center; 
            gap: 10px;
        }
        .stat-label { 
            color: #7f8c8d; 
            font-weight: 600;
        }
        .stat-value { 
            color: #2e86de; 
            font-size: 1.5rem; 
            font-weight: 700;
        }
        
        /* Grid Layout for Teachers */
        .teachers-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); 
            gap: 20px;
        }
        .teacher-card { 
            background: white; 
            padding: 25px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border-left: 5px solid #2e86de;
            transition: all 0.3s;
        }
        .teacher-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }
        .teacher-avatar { 
            font-size: 2.5rem; 
            margin-bottom: 15px;
        }
        .teacher-name { 
            font-size: 1.1rem; 
            font-weight: 700; 
            margin-bottom: 5px;
            color: #2b3e50;
        }
        .teacher-info { 
            font-size: 0.9rem; 
            color: #7f8c8d;
            margin-bottom: 10px;
        }
        .teacher-actions { 
            display: flex; 
            gap: 8px; 
            margin-top: 15px;
        }
        .action-btn { 
            flex: 1;
            padding: 8px 12px; 
            border: none; 
            border-radius: 6px; 
            text-decoration: none; 
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: center;
            transition: all 0.2s;
        }
        .edit-btn { background: #2e86de; color: white; }
        .edit-btn:hover { background: #1f6aa2; }
        .delete-btn { background: #e74c3c; color: white; }
        .delete-btn:hover { background: #c0392b; }
        
        .empty-state { 
            text-align: center; 
            padding: 60px; 
            background: white; 
            border-radius: 12px;
            color: #7f8c8d;
        }
        .empty-state h3 { 
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: #95a5a6;
        }
        
        @media (max-width: 768px) {
            .header { flex-direction: column; gap: 15px; align-items: flex-start; }
            .teachers-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">
            <a href="/dashboard">📊 Dashboard</a>
            <span>/</span>
            <span>👨‍🏫 Teachers</span>
        </div>
        
        <div class="header">
            <h1>👨‍🏫 Teacher Management</h1>
            <a href="/register" class="btn-primary">➕ Add New Teacher</a>
        </div>
        
        <div class="stats-bar">
            <div class="stat">
                <span class="stat-label">Total Teachers:</span>
                <span class="stat-value">{{ total_teachers }}</span>
            </div>
        </div>
        
        {% if teachers %}
        <div class="teachers-grid">
            {% for teacher in teachers %}
            <div class="teacher-card">
                <div class="teacher-avatar">👨‍🏫</div>
                <div class="teacher-name">{{ teacher.teacher_name }}</div>
                <div class="teacher-info">
                    📱 {{ teacher.mobile_number }}<br>
                    🆔 {{ teacher.staff_number or 'N/A' }}
                </div>
                <div class="teacher-actions">
                    <a href="/edit_teacher/{{ teacher.id }}" class="action-btn edit-btn">Edit</a>
                    <a href="/delete_teacher/{{ teacher.id }}" class="action-btn delete-btn" onclick="return confirm('Delete?');">Delete</a>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="empty-state">
            <h3>📭 No Teachers Found</h3>
            <p>Register a new teacher to get started</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

SUBMIT_MARKS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submit Marks - Exam Management System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f6f8fa; 
            color: #2b3e50;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        
        .breadcrumb { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 25px;
            align-items: center;
        }
        .breadcrumb a { color: #2e86de; text-decoration: none; font-weight: 600; }
        .breadcrumb span { color: #95a5a6; }
        
        .form-container { 
            background: white; 
            padding: 40px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        .form-title { 
            font-size: 2rem; 
            font-weight: 700; 
            margin-bottom: 30px;
            color: #2b3e50;
        }
        
        .form-group { margin-bottom: 25px; }
        .form-label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600; 
            color: #2b3e50;
        }
        input[type="text"], 
        input[type="number"], 
        select { 
            width: 100%; 
            padding: 12px 16px; 
            border: 1px solid #e9ecef; 
            border-radius: 8px; 
            font-size: 0.95rem;
            transition: all 0.3s;
        }
        input:focus, 
        select:focus { 
            outline: none; 
            border-color: #2e86de; 
            box-shadow: 0 0 0 3px rgba(46, 134, 222, 0.1);
        }
        
        .marks-table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 20px;
        }
        .marks-table th { 
            background: #f8fbff; 
            padding: 15px; 
            text-align: left; 
            font-weight: 600;
            color: #2b3e50;
            border-bottom: 2px solid #e9ecef;
        }
        .marks-table td { 
            padding: 12px 15px; 
            border-bottom: 1px solid #e9ecef;
        }
        .marks-table tbody tr:hover { background: #f8fbff; }
        .marks-table input { 
            width: 100%; 
            padding: 8px 10px;
            border: 1px solid #e9ecef;
            border-radius: 6px;
        }
        
        .form-actions { 
            display: flex; 
            gap: 12px; 
            margin-top: 30px;
        }
        .btn { 
            padding: 12px 24px; 
            border: none; 
            border-radius: 8px; 
            font-weight: 600; 
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.95rem;
        }
        .btn-primary { background: #2ecc71; color: white; }
        .btn-primary:hover { background: #27ae60; transform: translateY(-2px); }
        .btn-secondary { background: #95a5a6; color: white; }
        .btn-secondary:hover { background: #7f8c8d; }
        
        @media (max-width: 768px) {
            .form-container { padding: 20px; }
            .form-title { font-size: 1.3rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">
            <a href="/dashboard">📊 Dashboard</a>
            <span>/</span>
            <span>📝 Submit Marks</span>
        </div>
        
        <div class="form-container">
            <h1 class="form-title">📝 Submit Exam Marks</h1>
            
            <form method="POST">
                <div class="form-group">
                    <label class="form-label">👨‍🎓 Student</label>
                    <select name="student_id" required>
                        <option value="">-- Select a student --</option>
                        {% for student in students %}
                        <option value="{{ student.id }}">{{ student.student_name }} ({{ student.admission_number }})</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">📚 Exam</label>
                    <select name="exam_id" required>
                        <option value="">-- Select an exam --</option>
                        {% for exam in exams %}
                        <option value="{{ exam.id }}">{{ exam.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">🎯 Marks Entry</label>
                    <table class="marks-table">
                        <thead>
                            <tr>
                                <th>Subject</th>
                                <th>Marks</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for subject in subjects %}
                            <tr>
                                <td>{{ subject.name }}</td>
                                <td><input type="number" name="marks_{{ subject.id }}" min="0" max="100" placeholder="0-100"></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">💾 Submit Marks</button>
                    <a href="/dashboard" class="btn btn-secondary">← Cancel</a>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""

VIEW_SUBMISSIONS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>View Submissions - Exam Management System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f6f8fa; 
            color: #2b3e50;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        .breadcrumb { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 25px;
            align-items: center;
        }
        .breadcrumb a { color: #2e86de; text-decoration: none; font-weight: 600; }
        .breadcrumb span { color: #95a5a6; }
        
        .header { 
            background: white; 
            padding: 30px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }
        .header h1 { 
            font-size: 2rem; 
            font-weight: 700;
            color: #2b3e50;
            margin: 0;
        }
        
        .submissions-table { 
            background: white; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        .table-header { 
            padding: 20px 25px; 
            border-bottom: 1px solid #e9ecef;
            background: #f8fbff;
        }
        .table-header h2 { 
            margin: 0; 
            font-size: 1.2rem;
            color: #2b3e50;
        }
        
        table { 
            width: 100%; 
            border-collapse: collapse;
        }
        th { 
            padding: 15px 25px; 
            text-align: left; 
            font-weight: 600; 
            color: #2b3e50;
            background: #f8fbff;
            border-bottom: 2px solid #e9ecef;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        td { 
            padding: 15px 25px; 
            border-bottom: 1px solid #e9ecef;
        }
        tbody tr:hover { background: #f8fbff; }
        
        .actions-cell { 
            display: flex; 
            gap: 8px;
        }
        .btn-small { 
            padding: 6px 12px; 
            border: none; 
            border-radius: 6px; 
            text-decoration: none; 
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .edit-btn { background: #2e86de; color: white; }
        .edit-btn:hover { background: #1f6aa2; }
        .delete-btn { background: #e74c3c; color: white; }
        .delete-btn:hover { background: #c0392b; }
        
        .empty-state { 
            text-align: center; 
            padding: 60px; 
            background: white; 
            border-radius: 12px;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">
            <a href="/dashboard">📊 Dashboard</a>
            <span>/</span>
            <span>📊 View Submissions</span>
        </div>
        
        <div class="header">
            <h1>📊 Exam Mark Submissions</h1>
        </div>
        
        {% if submissions %}
        <div class="submissions-table">
            <div class="table-header">
                <h2>📋 All Submissions</h2>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Student</th>
                        <th>Admission #</th>
                        <th>Exam</th>
                        <th>Subject</th>
                        <th>Marks</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for submission in submissions %}
                    <tr>
                        <td>{{ submission.student_name }}</td>
                        <td>{{ submission.admission_number }}</td>
                        <td>{{ submission.exam_name }}</td>
                        <td>{{ submission.subject_name }}</td>
                        <td>{{ submission.marks }}/100</td>
                        <td>
                            <div class="actions-cell">
                                <a href="/edit_submission/{{ submission.id }}" class="btn-small edit-btn">✏️ Edit</a>
                                <a href="/delete_submission/{{ submission.id }}" class="btn-small delete-btn" onclick="return confirm('Delete?');">🗑️ Delete</a>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="empty-state">
            <h3>📭 No Submissions Found</h3>
            <p>No marks have been submitted yet</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

CANDIDATE_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Portal - Exam Results</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f6f8fa; 
            color: #2b3e50;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        
        .header { 
            background: linear-gradient(135deg, #2e86de 0%, #1f6aa2 100%); 
            color: white; 
            padding: 40px; 
            border-radius: 16px; 
            margin-bottom: 30px;
            box-shadow: 0 8px 24px rgba(46, 134, 222, 0.25);
        }
        .header-content { 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .header h1 { 
            font-size: 2rem; 
            font-weight: 700; 
            margin-bottom: 5px;
        }
        .header p { opacity: 0.95; }
        .logout-btn { 
            background: #e74c3c; 
            color: white; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 8px; 
            text-decoration: none; 
            font-weight: 600; 
            cursor: pointer;
            transition: all 0.3s;
        }
        .logout-btn:hover { background: #c0392b; }
        
        .student-info { 
            background: white; 
            padding: 25px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .info-item { }
        .info-label { 
            font-size: 0.85rem; 
            color: #7f8c8d; 
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .info-value { 
            font-size: 1.1rem; 
            font-weight: 700;
            color: #2b3e50;
        }
        
        .results-section { 
            background: white; 
            padding: 30px; 
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        .results-title { 
            font-size: 1.5rem; 
            font-weight: 700;
            margin-bottom: 25px;
            color: #2b3e50;
        }
        
        .exam-results { 
            margin-bottom: 30px;
        }
        .exam-header { 
            background: #f8fbff; 
            padding: 15px 20px; 
            border-radius: 8px;
            border-left: 5px solid #2e86de;
            margin-bottom: 15px;
        }
        .exam-name { 
            font-size: 1.1rem; 
            font-weight: 700;
            color: #2b3e50;
        }
        
        .marks-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px;
        }
        .mark-card { 
            background: #f8fbff; 
            padding: 20px; 
            border-radius: 10px;
            border: 2px solid #e9ecef;
            text-align: center;
        }
        .subject-name { 
            font-weight: 700; 
            color: #2b3e50;
            margin-bottom: 10px;
        }
        .mark-value { 
            font-size: 2rem; 
            font-weight: 700; 
            color: #2e86de;
        }
        .mark-percentage { 
            font-size: 0.9rem; 
            color: #7f8c8d;
        }
        
        .empty-state { 
            text-align: center; 
            padding: 60px 20px;
            color: #7f8c8d;
        }
        
        @media (max-width: 768px) {
            .header-content { flex-direction: column; gap: 15px; align-items: flex-start; }
            .student-info { grid-template-columns: 1fr; }
            .marks-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <div>
                    <h1>Welcome, {{ student_name }}! 👋</h1>
                    <p>View Your Exam Results</p>
                </div>
                <a href="/logout" class="logout-btn">🚪 Logout</a>
            </div>
        </div>
        
        <div class="student-info">
            <div class="info-item">
                <div class="info-label">Admission Number</div>
                <div class="info-value">{{ admission_number }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Grade</div>
                <div class="info-value">Grade {{ grade }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Stream</div>
                <div class="info-value">{{ stream or 'N/A' }}</div>
            </div>
        </div>
        
        <div class="results-section">
            <h2 class="results-title">📊 Your Exam Results</h2>
            
            {% if results %}
                {% for exam_name, subjects_marks in grouped_results.items() %}
                <div class="exam-results">
                    <div class="exam-header">
                        <div class="exam-name">{{ exam_name }}</div>
                    </div>
                    <div class="marks-grid">
                        {% for subject, marks in subjects_marks %}
                        <div class="mark-card">
                            <div class="subject-name">{{ subject }}</div>
                            <div class="mark-value">{{ marks }}</div>
                            <div class="mark-percentage">out of 100 marks</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
            {% else %}
            <div class="empty-state">
                <h3>📭 No Results Available</h3>
                <p>Your exam results will appear here once they are published</p>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

