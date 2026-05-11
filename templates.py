"""
EDUSMART Solutions - Web Server Templates
All HTML templates for the Flask web server, extracted from exam_system.py
No tkinter dependencies - pure HTML/CSS/JavaScript templates.
"""

# ============================================================================
# LOGIN, REGISTRATION, & AUTHENTICATION TEMPLATES
# ============================================================================

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDUSMART SOLUTIONS - Teacher Login</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { width: min(100%, 450px); margin: 40px auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 25px 80px rgba(0,0,0,0.15); position: relative; overflow: hidden; }
        .container::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; background: linear-gradient(90deg, #667eea, #764ba2); }
        .logo { text-align: center; margin-bottom: 20px; }
        .logo img { max-width: 80px; height: auto; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #2b3e50; margin-bottom: 30px; font-size: 1.8rem; font-weight: 600; }
        h1::before { content: '🎓'; margin-right: 10px; }
        .form-group { margin-bottom: 24px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; font-size: 0.95rem; }
        input[type="text"], input[type="password"] { width: 100%; padding: 16px; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 16px; background: #fafafa; transition: border-color 0.3s ease, box-shadow 0.3s ease; }
        input[type="text"]:focus, input[type="password"]:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 4px rgba(102,126,234,0.1); background: white; }
        button { width: 100%; padding: 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; }
        button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.3); }
        .error, .success { text-align: center; margin-top: 15px; padding: 12px; border-radius: 8px; font-weight: 500; }
        .error { color: #dc2626; background: #fef2f2; border: 1px solid #fecaca; }
        .success { color: #16a34a; background: #f0fdf4; border: 1px solid #bbf7d0; }
        .forgot-password { text-align: center; margin-top: 16px; }
        .forgot-password a { color: #667eea; text-decoration: none; font-weight: 600; }
        .forgot-password a:hover { text-decoration: underline; }
        @media (max-width: 500px) {
            .container { margin: 20px; padding: 30px; }
            h1 { font-size: 1.5rem; }
            .logo img { max-width: 60px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="/static/school_logo.png" alt="EDUSMART SOLUTIONS Logo">
        </div>
        <h1>EDUSMART SOLUTIONS - Teacher Login</h1>
        <form method="POST">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
            
            <div style="margin-top: 16px; text-align: center;">
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 12px;">Don't have an account yet?</p>
                <a href="/register" style="display: inline-block; padding: 10px 24px; background: #4CAF50; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; transition: background 0.3s ease;">+ Create Account</a>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #f0f7ff; border-left: 4px solid #667eea; border-radius: 6px; text-align: center;">
                <p style="margin: 0 0 10px 0; color: #333; font-size: 0.9rem; font-weight: 600;">Are you a Grade 9 Candidate?</p>
                <a href="/candidate_login" style="display: inline-block; padding: 8px 16px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 0.9rem;">📱 Access Student Portal</a>
            </div>
            
            <div class="forgot-password">
                <a href="/forgot_password">Forgot Password?</a>
            </div>
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
        </form>
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
    <title>Student Candidate Portal - EDUSMART SOLUTIONS</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { width: min(100%, 450px); margin: 40px auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 25px 80px rgba(0,0,0,0.15); position: relative; overflow: hidden; }
        .container::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; background: linear-gradient(90deg, #667eea, #764ba2); }
        .logo { text-align: center; margin-bottom: 20px; }
        .logo img { max-width: 80px; height: auto; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #2b3e50; margin-bottom: 10px; font-size: 1.8rem; font-weight: 600; }
        h1::before { content: '🎓'; margin-right: 10px; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; font-size: 0.95rem; }
        .form-group { margin-bottom: 24px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; font-size: 0.95rem; }
        input[type="text"], input[type="password"] { width: 100%; padding: 16px; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 16px; background: #fafafa; transition: border-color 0.3s ease, box-shadow 0.3s ease; }
        input[type="text"]:focus, input[type="password"]:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 4px rgba(102,126,234,0.1); background: white; }
        button { width: 100%; padding: 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; }
        button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.3); }
        .error, .success { text-align: center; margin-top: 15px; padding: 12px; border-radius: 8px; font-weight: 500; }
        .error { color: #dc2626; background: #fef2f2; border: 1px solid #fecaca; }
        .success { color: #16a34a; background: #f0fdf4; border: 1px solid #bbf7d0; }
        .footer-links { text-align: center; margin-top: 20px; }
        .footer-links a { color: #667eea; text-decoration: none; font-weight: 600; margin: 0 10px; }
        .footer-links a:hover { text-decoration: underline; }
        .divider { text-align: center; margin: 20px 0; color: #999; }
        @media (max-width: 500px) {
            .container { margin: 20px; padding: 30px; }
            h1 { font-size: 1.5rem; }
            .logo img { max-width: 60px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="/static/school_logo.png" alt="EDUSMART SOLUTIONS Logo">
        </div>
        <h1>Student Portal</h1>
        <p class="subtitle">Grade 9 Candidates - Set Your Targets</p>
        <form method="POST">
            <div class="form-group">
                <label for="admission_number">Admission Number</label>
                <input type="text" id="admission_number" name="admission_number" placeholder="e.g., 001" required>
            </div>
            <div class="form-group">
                <label for="student_name">Student Name</label>
                <input type="text" id="student_name" name="student_name" placeholder="Your full name" required>
            </div>
            <button type="submit">Access Portal</button>
            
            <div class="divider">—— or ——</div>
            
            <div class="footer-links">
                <a href="/login">🔐 Teacher Login</a>
            </div>
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
        </form>
    </div>
</body>
</html>
"""

# ============================================================================
# DASHBOARD TEMPLATE
# ============================================================================

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Online Results - Exam Management System</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            position: relative;
        }
        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="%23ffffff" opacity="0.03"/><circle cx="75" cy="75" r="1" fill="%23ffffff" opacity="0.03"/><circle cx="50" cy="10" r="0.5" fill="%23ffffff" opacity="0.02"/><circle cx="10" cy="50" r="0.5" fill="%23ffffff" opacity="0.02"/><circle cx="90" cy="30" r="0.5" fill="%23ffffff" opacity="0.02"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            pointer-events: none;
        }
        .container {
            width: min(100%, 1200px);
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 0;
            border-radius: 24px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.15);
            overflow: hidden;
            position: relative;
        }
        .greeting-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px 30px 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .school-branding {
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        .school-branding .school-name {
            font-size: 1.4rem;
            font-weight: 700;
            letter-spacing: 2px;
            text-shadow: 0 2px 8px rgba(0,0,0,0.2);
            margin: 0 0 5px 0;
            text-transform: uppercase;
        }
        .school-branding .school-motto {
            font-size: 0.9rem;
            font-style: italic;
            opacity: 0.95;
            margin: 0;
            font-weight: 300;
            letter-spacing: 1px;
        }
        .school-branding::after {
            content: '';
            display: block;
            width: 80px;
            height: 3px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
            margin: 12px auto 0;
        }
        .greeting-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        .greeting-header h1 {
            margin: 0 0 10px 0;
            font-size: 2.5rem;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }
        .greeting-header .subtitle {
            margin: 0;
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 300;
            position: relative;
            z-index: 1;
        }
        .welcome-message {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            margin: 0;
            font-size: 1.2rem;
            font-weight: 500;
            position: relative;
        }
        .welcome-message::before {
            content: '👋';
            font-size: 1.5rem;
            margin-right: 10px;
        }
        .layout {
            display: flex;
            flex-wrap: wrap;
            gap: 0;
            align-items: stretch;
        }
        .sidebar {
            flex: 0 0 280px;
            min-width: 280px;
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px 25px;
            position: relative;
        }
        .sidebar::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="sidebar-pattern" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23sidebar-pattern)"/></svg>');
        }
        .sidebar h2 {
            margin-top: 0;
            margin-bottom: 30px;
            font-size: 1.4rem;
            color: #ecf0f1;
            font-weight: 600;
            text-align: center;
            position: relative;
            padding-bottom: 15px;
        }
        .sidebar h2::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #3498db, #2980b9);
            border-radius: 2px;
        }
        .sidebar a {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            margin-bottom: 8px;
            color: #ecf0f1;
            text-decoration: none;
            border-radius: 12px;
            border: 1px solid transparent;
            transition: all 0.3s ease;
            font-weight: 500;
            position: relative;
            overflow: hidden;
        }
        .sidebar a::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s ease;
        }
        .sidebar a:hover {
            background: rgba(255,255,255,0.1);
            border-color: rgba(255,255,255,0.2);
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .sidebar a:hover::before {
            left: 100%;
        }
        .sidebar a:active {
            transform: translateX(3px);
        }
        .main {
            flex: 1;
            min-width: 0;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: stretch;
            min-height: 400px;
        }
        .main h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
        }
        .main > p {
            color: #7f8c8d;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 40px;
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
            padding: 25px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stat-card:nth-child(2) {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            box-shadow: 0 8px 25px rgba(245, 87, 108, 0.3);
        }
        .stat-card:nth-child(3) {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
        }
        .stat-card:nth-child(4) {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            box-shadow: 0 8px 25px rgba(67, 233, 123, 0.3);
        }
        .stat-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.2);
        }
        .stat-card-icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .stat-card-label {
            font-size: 0.95rem;
            opacity: 0.9;
            font-weight: 500;
            margin-bottom: 8px;
        }
        .stat-card-value {
            font-size: 2.2rem;
            font-weight: 700;
        }
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 40px;
        }
        .action-btn {
            background: white;
            border: 2px solid #e0e7ff;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            text-decoration: none;
            color: #2c3e50;
            transition: all 0.3s ease;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .action-btn:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: transparent;
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        .action-btn-icon {
            font-size: 1.8rem;
        }
        .features-section {
            background: white;
            border: 2px dashed #e0e7ff;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            color: #2c3e50;
        }
        .features-section h3 {
            margin-top: 0;
            color: #667eea;
            font-size: 1.2rem;
        }
        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .features-list li {
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .logout {
            margin-top: auto;
            text-align: center;
        }
        .logout a {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #e74c3c;
            text-decoration: none;
            font-weight: 600;
            padding: 12px 24px;
            border-radius: 25px;
            border: 2px solid #e74c3c;
            transition: all 0.3s ease;
            background: transparent;
        }
        .logout a:hover {
            background: #e74c3c;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(231,76,60,0.3);
        }
        .logout a::before {
            content: '🚪';
            font-size: 1.1rem;
        }
        @media (max-width: 900px) {
            .layout { flex-direction: column; }
            .sidebar { width: 100%; order: 2; }
            .main { order: 1; }
            .greeting-header h1 { font-size: 2rem; }
            .welcome-message { font-size: 1rem; }
        }
        @media (max-width: 600px) {
            .sidebar { padding: 20px; }
            .sidebar a { padding: 12px 15px; font-size: 0.9rem; }
            .main { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="greeting-header">
            <div class="school-branding">
                <h2 class="school-name">🎓 EDUSMART SOLUTIONS WEBSITE</h2>
                <p class="school-motto">Knowledge is Power</p>
            </div>
            <h1>📚 Exam Management System</h1>
            <p class="subtitle">Streamline Your Academic Assessment Process</p>
        </div>
        <div class="welcome-message">
            Welcome back, {{ teacher_name }}! Ready to manage your exams efficiently.
        </div>
        <div class="layout">
            <aside class="sidebar">
                <h2>📋 Navigation</h2>
                <a href="/submit_marks">📝 Submit Marks</a>
                <a href="/students">👩‍🎓 Students</a>
                <a href="/teachers">👨‍🏫 Teachers</a>
                <a href="/notifications">🔔 Notifications</a>
                <a href="/settings">⚙️ Settings</a>
                <a href="/view_submissions">📊 View Submissions</a>
                <a href="/track_progress">📈 Track Progress</a>
                <a href="/student_reports">📑 Student Reports</a>
                <a href="/export_results">💾 Export CSV</a>
                <a href="/manage_exams">📋 Manage Exams</a>
            </aside>
            <main class="main">
                <h1>Dashboard Overview</h1>
                <p>Welcome! Get a quick overview of your system and access key functions below.</p>

                <!-- Statistics Cards -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-card-icon">👨‍🎓</div>
                        <div class="stat-card-label">Total Students</div>
                        <div class="stat-card-value">{{ total_students }}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-icon">📝</div>
                        <div class="stat-card-label">Total Exams</div>
                        <div class="stat-card-value">{{ total_exams }}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-icon">📚</div>
                        <div class="stat-card-label">Total Subjects</div>
                        <div class="stat-card-value">{{ total_subjects }}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-icon">🏫</div>
                        <div class="stat-card-label">Total Classes</div>
                        <div class="stat-card-value">{{ total_classes }}</div>
                    </div>
                </div>

                <!-- Quick Action Buttons -->
                <h3 style="color: #2c3e50; margin-top: 30px; margin-bottom: 20px; text-align: center; font-size: 1.3rem;">Quick Access</h3>
                <div class="quick-actions">
                    <a href="/submit_marks" class="action-btn">
                        <div class="action-btn-icon">📝</div>
                        Submit Marks
                    </a>
                    <a href="/students" class="action-btn">
                        <div class="action-btn-icon">👩‍🎓</div>
                        Manage Students
                    </a>
                    <a href="/view_submissions" class="action-btn">
                        <div class="action-btn-icon">📊</div>
                        View Submissions
                    </a>
                    <a href="/track_progress" class="action-btn">
                        <div class="action-btn-icon">📈</div>
                        Track Progress
                    </a>
                    <a href="/student_reports" class="action-btn">
                        <div class="action-btn-icon">📑</div>
                        Reports
                    </a>
                    <a href="/manage_exams" class="action-btn">
                        <div class="action-btn-icon">⚙️</div>
                        Manage Exams
                    </a>
                </div>

                <!-- Features Section -->
                <div class="features-section">
                    <h3>✨ Key Features</h3>
                    <ul class="features-list">
                        <li>📊 <strong>Real-time Analytics</strong> - Track exam submissions in real-time</li>
                        <li>🎯 <strong>Grade Management</strong> - Organized by grade and stream</li>
                        <li>🔔 <strong>Notifications</strong> - Stay updated with system alerts</li>
                        <li>📈 <strong>Progress Tracking</strong> - Monitor exam submission status</li>
                        <li>📑 <strong>Detailed Reports</strong> - Generate comprehensive student reports</li>
                        <li>💾 <strong>Data Export</strong> - Export results to CSV format</li>
                    </ul>
                </div>

                <div class="logout">
                    <a href="/logout">Logout</a>
                </div>
            </main>
        </div>
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
    <title>Forgot Password - EDUSMART SOLUTIONS</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { width: min(100%, 450px); margin: 40px auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 25px 80px rgba(0,0,0,0.15); position: relative; overflow: hidden; }
        .container::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; background: linear-gradient(90deg, #667eea, #764ba2); }
        h1 { text-align: center; color: #2b3e50; margin-bottom: 20px; font-size: 1.8rem; font-weight: 600; }
        p { text-align: center; color: #4b5563; margin-bottom: 24px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; font-size: 0.95rem; }
        input[type="text"] { width: 100%; padding: 16px; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 16px; background: #fafafa; transition: border-color 0.3s ease, box-shadow 0.3s ease; }
        input[type="text"]:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 4px rgba(102,126,234,0.1); background: white; }
        button { width: 100%; padding: 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; }
        button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.3); }
        .message { margin-top: 16px; text-align: center; padding: 14px; border-radius: 12px; }
        .success { background: #ecfdf5; color: #166534; border: 1px solid #bbf7d0; }
        .error { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
        .back-link { margin-top: 18px; text-align: center; }
        .back-link a { color: #667eea; text-decoration: none; font-weight: 600; }
        .back-link a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Forgot Password</h1>
        <p>Enter your username below and an administrator will help you reset your password.</p>
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <button type="submit">Request Reset</button>
            {% if message %}
            <div class="message {{ 'success' if success else 'error' }}">{{ message }}</div>
            {% endif %}
        </form>
        <div class="back-link">
            <a href="/login">Back to Login</a>
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
    <title>Create Teacher Account - EDUSMART SOLUTIONS</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { width: min(100%, 500px); background: white; padding: 40px; border-radius: 20px; box-shadow: 0 25px 80px rgba(0,0,0,0.15); position: relative; overflow: hidden; }
        .container::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; background: linear-gradient(90deg, #667eea, #764ba2); }
        h1 { text-align: center; color: #2b3e50; margin-bottom: 10px; font-size: 1.8rem; font-weight: 600; }
        .subtitle { text-align: center; color: #4b5563; margin-bottom: 24px; font-size: 0.95rem; }
        .form-group { margin-bottom: 18px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; font-size: 0.95rem; }
        .required { color: #dc2626; }
        .optional { color: #9ca3af; font-size: 0.85rem; font-weight: 400; }
        input { width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 15px; background: #fafafa; transition: border-color 0.3s ease, box-shadow 0.3s ease; }
        input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 4px rgba(102,126,234,0.1); background: white; }
        button { width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; margin-top: 10px; }
        button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.3); }
        .message { margin-top: 16px; text-align: center; padding: 14px; border-radius: 12px; word-break: break-word; white-space: pre-wrap; line-height: 1.6; }
        .success { background: #ecfdf5; color: #166534; border: 1px solid #bbf7d0; }
        .error { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
        .success-details { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; padding: 16px; margin-top: 16px; }
        .success-details h3 { color: #0c4a6e; margin: 0 0 12px 0; font-size: 1rem; }
        .credential-box { background: white; padding: 12px; border-radius: 8px; border-left: 4px solid #667eea; margin: 8px 0; font-family: 'Courier New', monospace; }
        .credential-label { color: #666; font-size: 0.85rem; font-weight: 600; }
        .credential-value { color: #1f2937; font-size: 1.1rem; font-weight: bold; margin-top: 4px; overflow-wrap: break-word; }
        .back-link { margin-top: 18px; text-align: center; }
        .back-link a { color: #667eea; text-decoration: none; font-weight: 600; }
        .back-link a:hover { text-decoration: underline; }
        .divider { margin: 24px 0; border-top: 1px solid #e5e7eb; position: relative; }
        .divider-text { position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: white; padding: 0 8px; color: #9ca3af; font-size: 0.85rem; }
    </style>
</head>
<body>
    <div class="container">
        {% if success %}
            <h1>✓ Account Created!</h1>
            <p class="subtitle">Your teacher account has been registered</p>
            
            <div class="success-details">
                <h3>Your Login Credentials:</h3>
                <div class="credential-box">
                    <div class="credential-label">Username:</div>
                    <div class="credential-value">{{ generated_username }}</div>
                </div>
                <div class="credential-box">
                    <div class="credential-label">Password:</div>
                    <div class="credential-value">••••••••</div>
                </div>
                <p style="color: #666; font-size: 0.9rem; margin-top: 12px;">
                    ℹ️ <strong>Keep your username safe!</strong> Use it to log in to the exam management system.
                </p>
            </div>
            
            <div class="back-link" style="margin-top: 24px;">
                <a href="/login">Proceed to Login</a>
            </div>
        {% else %}
            <h1>Create Teacher Account</h1>
            <p class="subtitle">Register to access the exam management system</p>
            
            {% if message %}
            <div class="message {{ 'success' if success else 'error' }}">{{ message }}</div>
            {% endif %}
            
            <form method="POST" action="/register">
                <div class="form-group">
                    <label for="teacher_name">Teacher Name <span class="required">*</span></label>
                    <input type="text" id="teacher_name" name="teacher_name" placeholder="e.g., John Mwangi" required>
                </div>
                <div class="form-group">
                    <label for="mobile_number">Mobile Number <span class="required">*</span></label>
                    <input type="tel" id="mobile_number" name="mobile_number" placeholder="e.g., +254712345678" required>
                </div>
                <div class="form-group">
                    <label for="staff_number">Staff Number / TSC Number <span class="optional">(Optional)</span></label>
                    <input type="text" id="staff_number" name="staff_number" placeholder="e.g., TSC/2023/001234">
                </div>
                
                <div class="divider"><span class="divider-text">Account Credentials</span></div>
                
                <div class="form-group">
                    <label for="password">Password <span class="required">*</span></label>
                    <input type="password" id="password" name="password" placeholder="Create a strong password" required>
                </div>
                <div class="form-group">
                    <label for="confirm_password">Confirm Password <span class="required">*</span></label>
                    <input type="password" id="confirm_password" name="confirm_password" placeholder="Re-enter your password" required>
                </div>
                
                <p style="font-size: 0.9rem; color: #666; background: #f3f4f6; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                    ℹ️ Your username will be automatically generated after registration.
                </p>
                
                <button type="submit">Create Account</button>
            </form>
            <div class="back-link">
                <a href="/login">Back to Login</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""
