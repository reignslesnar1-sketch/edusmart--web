# Complete Flask Web Application Extraction

## File Source
**Source File:** `c:\Users\Administrator\Desktop\EDUSMART SOLUTIONS\claude\exam management system 2.py`

---

## TABLE OF CONTENTS
1. [Subject Order Dictionaries](#subject-order-dictionaries) - Lines 179-192
2. [Supporting Functions](#supporting-functions)
3. [Database Functions](#database-functions)
4. [HTML Templates](#html-templates)
5. [Flask Application Function](#flask-application-function)

---

## SUBJECT ORDER DICTIONARIES

### KPSEA_SUBJECT_ORDER (Lines 179-185)
```python
179 | KPSEA_SUBJECT_ORDER = {
180 |     "1": ["Maths", "English", "Kiswahili", "Integrated Science"],
181 |     "2": ["Maths", "English", "Kiswahili", "Integrated Science"],
182 |     "3": ["Maths", "English", "Kiswahili", "Integrated Science"],
183 |     "4": ["Maths", "English", "Kiswahili", "Science", "Creative Arts", "Social Studies\\C.R.E"],
184 |     "5": ["Maths", "English", "Kiswahili", "Science", "C.A.A.S"],
185 |     "6": ["Maths", "English", "Kiswahili", "Science", "Agriculture", "Social Studies\\C.R.E\\Creative Arts"]
186 | }
```

### KJSEA_SUBJECT_ORDER (Lines 188-191)
```python
188 | KJSEA_SUBJECT_ORDER = [
189 |     "Mathematics", "English", "Kiswahili", "Integrated Science", "Pre-Technical Studies",
190 |     "Social Studies", "Creative Arts", "Agriculture", "C.R.E"
191 | ]
192 | KJSEA_ALLOWED_SUBJECTS = set(KJSEA_SUBJECT_ORDER)
```

---

## SUPPORTING FUNCTIONS

### get_performance_level() Function (Lines 1919-1970)
```python
1919 | def get_performance_level(marks, level="KPSEA"):
1920 |     """
1921 |     Determine performance level based on marks and curriculum level
1922 |     
1923 |     KPSEA (Grades 1-6):
1924 |     75-100: Exceeding Expectation
1925 |     41-74: Meeting Expectation
1926 |     21-40: Approaching Expectation
1927 |     0-20: Below Expectation
1928 |     
1929 |     KJSEA (Grades 7-9):
1930 |     90-100: Exceeding Expectation 1 (8 points)
1931 |     75-89: Exceeding Expectation 2 (7 points)
1932 |     58-74: Meeting Expectation 1 (6 points)
1933 |     41-57: Meeting Expectation 2 (5 points)
1934 |     31-40: Approaching Expectation 1 (4 points)
1935 |     21-30: Approaching Expectation 2 (3 points)
1936 |     11-20: Below Expectation 1 (2 points)
1937 |     1-10: Below Expectation 2 (1 point)
1938 |     """
1939 |     if marks is None:
1940 |         return ("—", "—") if level == "KJSEA" else "—"
1941 |     
1942 |     marks = int(marks) if isinstance(marks, (int, float)) else 0
1943 |     
1944 |     if level == "KJSEA":
1945 |         # Return tuple of (performance_label, points)
1946 |         if marks >= 90:
1947 |             return ("Exceeding E1", "8")
1948 |         elif marks >= 75:
1949 |             return ("Exceeding E2", "7")
1950 |         elif marks >= 58:
1951 |             return ("Meeting E1", "6")
1952 |         elif marks >= 41:
1953 |             return ("Meeting E2", "5")
1954 |         elif marks >= 31:
1955 |             return ("Approaching E1", "4")
1956 |         elif marks >= 21:
1957 |             return ("Approaching E2", "3")
1958 |         elif marks >= 11:
1959 |             return ("Below E1", "2")
1960 |         else:
1961 |             return ("Below E2", "1")
1962 |     else:  # KPSEA
1963 |         # Return single string for KPSEA
1964 |         if marks >= 75:
1965 |             return "Exceeding"
1966 |         elif marks >= 41:
1967 |             return "Meeting"
1968 |         elif marks >= 21:
1969 |             return "Approaching"
1970 |         else:
1971 |             return "Below"
```

### ensure_default_teacher() Function (Lines 629-700)
```python
629  | def ensure_default_teacher():
630  |     """Create a default admin teacher account if no teacher accounts exist."""
631  |     try:
632  |         conn = sqlite3.connect(DB_FILE)
633  |         cursor = conn.cursor()
633  |         cursor.execute("SELECT COUNT(*) FROM teachers")
634  |         count = cursor.fetchone()[0]
635  |         if count == 0:
636  |             cursor.execute(
637  |                 "INSERT INTO teachers (username, password_hash, teacher_name) VALUES (?, ?, ?)",
638  |                 ("admin", hash_admin_password(), "Administrator")
639  |             )
640  |             conn.commit()
641  |         conn.close()
642  |     except Exception as e:
643  |         print(f"Error ensuring default teacher account: {e}")
```

---

## DATABASE FUNCTIONS

### ensure_tables() Function (Lines 8962-9100)
Creates all required database tables for the web application.

```python
8962 | def ensure_tables():
8963 |     cursor.execute("""
8964 |     CREATE TABLE IF NOT EXISTS students(
8965 |         id INTEGER PRIMARY KEY AUTOINCREMENT,
8966 |         admission_number TEXT UNIQUE,
8967 |         student_name TEXT,
8968 |         level TEXT,
8969 |         grade INTEGER,
8970 |         stream TEXT,
8971 |         parent_name TEXT,
8972 |         parent_phone TEXT,
8973 |         student_details TEXT,
8974 |         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
8975 |     )
8976 |     """)
8977 |
8978 |     cursor.execute("""
8979 |     CREATE TABLE IF NOT EXISTS subjects(
8980 |         id INTEGER PRIMARY KEY AUTOINCREMENT,
8981 |         name TEXT
8982 |     )
8983 |     """)
8984 |
8985 |     cursor.execute("""
8986 |     CREATE TABLE IF NOT EXISTS subject_levels(
8987 |         id INTEGER PRIMARY KEY AUTOINCREMENT,
8988 |         subject_id INTEGER,
8989 |         level TEXT,
8990 |         grade INTEGER
8991 |     )
8992 |     """)
8993 |
8994 |     # If this table was created by an older version, ensure the grade column exists.
8995 |     table_info = cursor.execute("PRAGMA table_info(subject_levels)").fetchall()
8996 |     columns = [row[1] for row in table_info]
8997 |     if "grade" not in columns:
8998 |         try:
8999 |             cursor.execute("ALTER TABLE subject_levels ADD COLUMN grade INTEGER")
9000 |         except sqlite3.OperationalError:
9001 |             pass
9002 |
9003 |     # Check if students table has stream column (added in later versions)
9004 |     students_table_info = cursor.execute("PRAGMA table_info(students)").fetchall()
9004 |     students_columns = [row[1] for row in students_table_info]
9005 |     if "stream" not in students_columns:
9006 |         try:
9007 |             cursor.execute("ALTER TABLE students ADD COLUMN stream TEXT")
9008 |         except sqlite3.OperationalError:
9009 |             pass
9010 |
9011 |     # make sure a given subject/level/grade row can only exist once
9012 |     # remove any existing duplicate rows so the unique index can be created.
9013 |     cursor.execute("""
9014 |         DELETE FROM subject_levels
9015 |         WHERE rowid NOT IN (
9016 |             SELECT MIN(rowid) FROM subject_levels
9017 |             GROUP BY subject_id, level, grade
9018 |         )
9019 |     """)
9020 |
9021 |     # Remove any old index that only used subject_id and level.
9022 |     cursor.execute("DROP INDEX IF EXISTS idx_subj_levels_unique")
9023 |
9024 |     try:
9025 |         cursor.execute("""
9026 |             CREATE UNIQUE INDEX IF NOT EXISTS idx_subj_levels_unique
9027 |             ON subject_levels(subject_id, level, grade)
9028 |         """)
9029 |     except sqlite3.OperationalError:
9030 |         # older SQLite versions or unexpected issues; ignore
9031 |         pass
9032 |
9033 |     cursor.execute("""
9034 |     CREATE TABLE IF NOT EXISTS streams(
9035 |         id INTEGER PRIMARY KEY AUTOINCREMENT,
9036 |         name TEXT UNIQUE,
9037 |         level TEXT,
9038 |         grade INTEGER,
9039 |         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
9040 |     )
9041 |     """)
9042 |     # migrate existing databases that don't have the grade column
9043 |     try:
9044 |         cursor.execute("ALTER TABLE streams ADD COLUMN grade INTEGER")
9045 |     except sqlite3.OperationalError:
9046 |         # column probably already exists
9047 |         pass
9048 |
9049 |     cursor.execute("""
9050 |     CREATE TABLE IF NOT EXISTS exams(
9051 |         id INTEGER PRIMARY KEY AUTOINCREMENT,
9052 |         exam_id TEXT UNIQUE,
9053 |         name TEXT,
9054 |         start_date TEXT,
9055 |         end_date TEXT,
9056 |         duration_days INTEGER,
9057 |         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
9058 |     )
9059 |     """)
9060 |
9061 |     cursor.execute("""
9062 |     CREATE TABLE IF NOT EXISTS teachers(
9062 |         id INTEGER PRIMARY KEY AUTOINCREMENT,
9063 |         username TEXT UNIQUE,
9064 |         password_hash TEXT,
9065 |         teacher_name TEXT,
9066 |         mobile_number TEXT,
9067 |         staff_number TEXT,
9068 |         admission_num TEXT,
9069 |         first_school TEXT,
9070 |         village TEXT,
9071 |         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
9072 |     )
9073 |     """)
9074 |     try:
9075 |         cursor.execute("ALTER TABLE teachers ADD COLUMN admission_num TEXT")
9076 |         cursor.execute("ALTER TABLE teachers ADD COLUMN first_school TEXT")
9077 |         cursor.execute("ALTER TABLE teachers ADD COLUMN village TEXT")
9078 |     except sqlite3.OperationalError:
9079 |         pass
9080 |
9081 |     cursor.execute("""
9082 |     CREATE TABLE IF NOT EXISTS results(
9082 |         id INTEGER PRIMARY KEY AUTOINCREMENT,
9083 |         student_id INTEGER,
9084 |         subject_id INTEGER,
9085 |         exam_id INTEGER,
9086 |         teacher_id INTEGER,
9087 |         marks INTEGER,
9088 |         submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
9089 |     )
9090 |     """)
9091 |     try:
9092 |         cursor.execute("ALTER TABLE results ADD COLUMN teacher_id INTEGER")
9093 |     except sqlite3.OperationalError:
9094 |         pass
9095 |     try:
9096 |         cursor.execute("ALTER TABLE results ADD COLUMN submitted_at TIMESTAMP")
9097 |     except sqlite3.OperationalError:
9098 |         pass
```

### ensure_default_subjects() Function (Lines 9247-9328)
Creates default subjects for each curriculum level.

```python
9247 | def ensure_default_subjects():
9248 |     cursor.execute("SELECT COUNT(*) FROM subject_levels")
9249 |     if cursor.fetchone()[0] > 0:
9250 |         return
9251 |
9252 |     # ensure the database contains at least the known subjects for each
9253 |     # level; the level‑specific order is defined above.
9254 |     # For KPSEA, collect all subjects from all grades
9255 |     kpsea_subjects = set()
9256 |     for grade_subjects in KPSEA_SUBJECT_ORDER.values():
9257 |         kpsea_subjects.update(grade_subjects)
9258 |     kpsea_subjects = list(kpsea_subjects)
9259 |     
9260 |     kjsea_subjects = KJSEA_SUBJECT_ORDER
9261 |
9262 |     # helper to add a subject and level association with optional grade
9263 |     def add_subj(name, level, grade=None):
9264 |         cursor.execute("SELECT id FROM subjects WHERE name=?", (name,))
9265 |         row = cursor.fetchone()
9266 |         if row:
9267 |             sid = row[0]
9268 |         else:
9269 |             cursor.execute("INSERT INTO subjects(name) VALUES(?)", (name,))
9270 |             sid = cursor.lastrowid
9271 |         # ensure level and grade link exists
9272 |         cursor.execute(
9273 |             "SELECT 1 FROM subject_levels WHERE subject_id=? AND level=? AND grade IS ?",
9274 |             (sid, level, grade)
9275 |         )
9276 |         if not cursor.fetchone():
9277 |             cursor.execute(
9278 |                 "INSERT INTO subject_levels(subject_id, level, grade) VALUES(?,?,?)",
9279 |                 (sid, level, grade)
9280 |             )
9281 |
9282 |     for grade, grade_subjects in KPSEA_SUBJECT_ORDER.items():
9283 |         for s in grade_subjects:
9284 |             add_subj(s, "KPSEA", int(grade))
9285 |     for grade in (7, 8, 9):
9286 |         for s in kjsea_subjects:
9287 |             add_subj(s, "KJSEA", grade)
9288 |
9289 |     conn.commit()
```

---

## HTML TEMPLATES

All templates are defined in the source file at the line numbers noted. Due to length, here's the location map:

| Template Name | Line | File Location |
|---|---|---|
| LOGIN_TEMPLATE | 2148 | Web teacher login page |
| CANDIDATE_LOGIN_TEMPLATE | 2222 | Student/candidate login page |
| DASHBOARD_TEMPLATE | 2451 | Teacher dashboard |
| STUDENTS_TEMPLATE | 2930 | Student management interface |
| CANDIDATE_DASHBOARD_TEMPLATE | 3719 | Student academic dashboard |
| ADD_STUDENT_TEMPLATE | 3065 | Add new student form |
| EDIT_STUDENT_TEMPLATE | 3163 | Edit student information |
| CANDIDATES_TEMPLATE | 3261 | Grade 9 candidate targets |
| CANDIDATES_ANALYTICS_TEMPLATE | 3482 | Candidate performance analytics |
| SUBMIT_MARKS_TEMPLATE | 4076 | Marks submission interface |
| NOTIFICATIONS_TEMPLATE | 4327 | Teacher notifications/audits |
| VIEW_SUBMISSIONS_TEMPLATE | 4759 | View & edit submissions |
| STUDENT_REPORTS_TEMPLATE | 5151 | Generate student reports |
| TRACK_PROGRESS_TEMPLATE | 5479 | Track exam submission progress |
| TEACHERS_TEMPLATE | 5685 | Manage teacher accounts |
| SIDEBAR_PAGE_TEMPLATE | 5635 | Generic page template with sidebar |
| FORGOT_PASSWORD_TEMPLATE | 2292 | Password recovery page |
| REGISTER_TEMPLATE | 2342 | Teacher registration page |
| CHECK_RESULTS_TEMPLATE | 8640+ | Public results checking page |

---

## FLASK APPLICATION FUNCTION

### create_flask_app() Function (Lines 5986-8916)

**Function Start:** Line 5986
**Function End:** Line 8916 (returns web_app)

#### Function Structure Overview:

1. **Initialization (Lines 5986-6010)**
   - Flask app creation
   - Secret key generation
   - URL encoding filter registration
   - Database connection setup
   - Table and subject initialization

2. **Authentication Routes (Lines 6187-6415)**
   - `@web_app.route('/')` - Index/welcome page (lines 6048-6187)
   - `@web_app.route('/login', methods=['GET', 'POST'])` - Teacher login (lines 6190-6322)
   - `@web_app.route('/register', methods=['GET', 'POST'])` - Teacher registration (lines 6325-6410)
   - `@web_app.route('/forgot_password', methods=['GET', 'POST'])` - Password recovery (lines 6413-6418)

3. **Teacher Dashboard Routes (Lines 6420-6453)**
   - `@web_app.route('/dashboard')` - Main dashboard (lines 6420-6444)
   - `@web_app.route('/logout')` - Logout (lines 6446-6449)

4. **Student Management Routes (Lines 6455-6720)**
   - `@web_app.route('/students')` - Student listing by grades (lines 6456-6471)
   - `@web_app.route('/students/grade/<int:grade>')` - Students by grade (lines 6473-6491)
   - `@web_app.route('/students/grade/<int:grade>/stream/<stream>')` - Students by stream (lines 6493-6527)
   - `@web_app.route('/students/add', methods=['GET', 'POST'])` - Add student (lines 6529-6628)
   - `@web_app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])` - Edit student (lines 6630-6720)

5. **Teacher Management Route (Lines 6475-6522)**
   - `@web_app.route('/teachers')` - View all teachers (lines 6475-6500)
   - `@web_app.route('/teachers/delete/<int:teacher_id>', methods=['POST'])` - Delete teacher (lines 6502-6513)

6. **Candidate (Grade 9) Routes (Lines 6722-6972)**
   - `@web_app.route('/candidates')` - Candidate management (lines 6722-6775)
   - `@web_app.route('/candidates/submit', methods=['POST'])` - Submit targets (lines 6777-6840)
   - `@web_app.route('/candidates/load_students', methods=['POST'])` - Load candidate students (lines 6842-6922)
   - `@web_app.route('/candidates/analytics')` - Candidate analytics (lines 6924-6972)

7. **Student Portal Routes (Lines 6974-7130)**
   - `@web_app.route('/candidate_login', methods=['GET', 'POST'])` - Student login (lines 6974-7021)
   - `@web_app.route('/candidate_dashboard', methods=['GET', 'POST'])` - Student dashboard (lines 7023-7132)
   - `@web_app.route('/candidate_logout')` - Student logout (lines 7134-7142)

8. **Marks Submission Routes (Lines 7144-7815)**
   - `@web_app.route('/submit_marks', methods=['GET', 'POST'])` - Submit marks (lines 7144-7284)
   - `@web_app.route('/get_students/<exam_id>/<subject_id>')` - Get students for exam/subject (lines 7286-7345)

9. **Results Viewing Routes (Lines 7347-7600)**
   - `@web_app.route('/view_submissions', methods=['GET', 'POST'])` - View submissions (lines 7347-7600)
   - `@web_app.route('/update_marks', methods=['POST'])` - Update marks (lines 7602-7700)
   - `@web_app.route('/approval_action', methods=['POST'])` - Approval actions (lines 7702-7730)

10. **Reporting Routes (Lines 7732-7815)**
    - `@web_app.route('/student_reports', methods=['GET', 'POST'])` - Student reports (lines 7732-7755)
    - `@web_app.route('/track_progress')` - Track exam progress (lines 7757-7815)
    - `@web_app.route('/request_submission')` - Request mark submission (lines 7817-7850)

11. **Public Results Routes (Lines 7852-8916)**
    - `@web_app.route('/check_results', methods=['GET', 'POST'])` - Public results page (lines 7852-8916)
    - `@web_app.route('/api/qr_code_image')` - QR code API (lines 7840-7860)
    - `@web_app.route('/api/student/<admission_number>/results')` - Student results API (lines 7618-7690)
    - `@web_app.route('/api/students')` - Students API (lines 7692-7735)
    - `@web_app.route('/api/stats')` - Statistics API (lines 7737-7785)

12. **Utility Routes**
    - `@web_app.route('/export_results')` - Export results to CSV
    - `@web_app.route('/manage_exams')` - Manage exams page
    - `@web_app.route('/settings', methods=['GET', 'POST'])` - Teacher settings
    - `@web_app.route('/notifications')` - Notifications page
    - `@web_app.route('/download_pdf/<filename>')` - Download PDF
    - `@web_app.route('/view_pdf/<filename>')` - View PDF

---

## KEY IMPLEMENTATION DETAILS

### URL Encoding Filter (Line 6001-6002)
```python
from urllib.parse import quote as url_quote
web_app.jinja_env.filters['urlencode'] = lambda s: url_quote(str(s))
```

This fixes the `| urlencode` filter for stream names with special characters.

### Database Connection (Lines 6005-6009)
```python
web_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
web_cursor = web_conn.cursor()
ensure_tables()
```

### Global Variables Used
- `web_app` - Flask application instance
- `web_conn` - Web server database connection
- `web_cursor` - Web server database cursor
- `FLASK_AVAILABLE` - Boolean flag for Flask availability
- `QR_AVAILABLE` - Boolean flag for QR code library availability

### Route Authentication
Most protected routes check:
```python
if 'username' not in session:
    return redirect(url_for('login'))
```

---

## INTEGRATION INSTRUCTIONS

1. Copy the entire `create_flask_app()` function (lines 5986-8916)
2. Include all subject order dictionaries (lines 179-192)
3. Include helper functions: `get_performance_level()`, `ensure_tables()`, `ensure_default_subjects()`, `ensure_default_teacher()`
4. Include all template definitions referenced in the routes
5. Ensure Flask, sqlite3, and dependencies are imported at file top
6. Initialize the app with: `web_app = create_flask_app()`
7. Run with: `web_app.run(debug=False, host='0.0.0.0', port=5000)`

---

## DEPENDENCIES REQUIRED
- Flask
- sqlite3 (built-in)
- qrcode (optional, for QR functionality)
- PIL/Pillow (with qrcode)
- jinja2 (included with Flask)
- csv, io, json, datetime, secrets, base64, os (all built-in)

---

**Extraction Complete** - Total: ~3,800 lines of code consolidated
