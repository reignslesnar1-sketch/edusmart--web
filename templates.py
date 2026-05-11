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
