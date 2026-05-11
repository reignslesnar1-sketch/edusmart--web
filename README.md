# EDUSMART - Exam Management System
## Professional Web Dashboard & Student Portal

A complete exam management system with a professional Flask web dashboard deployed on Render.

### Features

✅ **Teacher Dashboard**
- View student statistics (total students, exams, subjects)
- Quick access navigation cards
- Professional gradient header

✅ **Student Management**
- Search and filter students by grade
- View all student information (name, admission #, grade, stream)
- Add/Edit/Delete student records
- Professional data tables with pagination

✅ **Mark Submission**
- Submit exam marks for students
- Organize by student, exam, and subject
- Store marks in database

✅ **View Submissions**
- Review all submitted marks
- Edit/Delete submissions
- Organized by student and exam

✅ **Teacher Management**
- Card-based layout for teacher profiles
- View teacher contact info and staff number
- Add/Edit/Delete teacher records

✅ **Student Portal**
- Students login with admission number
- View their exam results
- Results grouped by exam and subject
- Professional result cards

### Technology Stack

- **Backend**: Python 3.11+ with Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Deployment**: Render

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the app**:
```bash
python app.py
```

3. **Access the app**:
- Teacher portal: `http://localhost:5000/login`
- Student portal: `http://localhost:5000/candidate_login`

### Database

The app uses SQLite with the following tables:
- **teachers** - Teacher credentials and info
- **students** - Student records with grade/stream info
- **exams** - Exam names and IDs
- **subjects** - Subject names
- **results** - Exam results linking students, exams, subjects, and marks

### Routes

#### Teacher Routes
- `GET /` - Home page
- `GET/POST /login` - Teacher login
- `GET/POST /register` - Teacher registration
- `GET /dashboard` - Teacher dashboard
- `GET /logout` - Logout
- `GET /students` - Student management page
- `GET /teachers` - Teacher management page
- `GET/POST /submit_marks` - Submit exam marks
- `GET /view_submissions` - View mark submissions
- `GET /student_reports` - Student performance reports
- `GET /notifications` - System notifications

#### Student Routes
- `GET/POST /candidate_login` - Student login
- `GET /candidate_dashboard` - View results
- `GET /logout` - Logout

### Deployment on Render

1. **Push code to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/edusmart.git
git branch -M main
git push -u origin main
```

2. **Create Render Web Service**:
   - Go to [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Set environment:
     - **Runtime**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
     - **Port**: 5000

3. **Render will automatically deploy** when you push to GitHub!

### Environment Variables

For production deployment on Render, set these in the Render dashboard:
```
FLASK_ENV=production
PORT=5000
```

### Project Structure

```
.
├── app.py                 # Flask application (all routes)
├── templates.py          # HTML templates for all pages
├── requirements.txt      # Python dependencies
├── Procfile             # Render process configuration
├── render.yaml          # Render deployment configuration
└── .gitignore           # Git ignore rules
```

### Color Scheme

- **Primary Blue**: #2e86de - Main actions
- **Success Green**: #2ecc71 - Add/Success
- **Warning Orange**: #f39c12 - Warnings
- **Danger Red**: #e74c3c - Delete/Danger
- **Background**: #f6f8fa - Light background

### Features in Dashboard

- **Breadcrumb Navigation** - Easy page navigation
- **Search & Filter** - Find students by grade/name
- **Responsive Design** - Works on mobile and desktop
- **Professional Cards** - Modern UI with hover effects
- **Data Tables** - Organized student/teacher information
- **Action Buttons** - Quick edit/delete/view actions
- **Stats Display** - Shows system metrics

### Database Initialization

The app automatically creates all required tables on first run. Just ensure you have write permissions to store the SQLite database file.

### Support & Troubleshooting

- **Port already in use**: Change port in `app.py` line with `app.run()`
- **Database errors**: Check file permissions in the app directory
- **Template not loading**: Verify `templates.py` is in the same directory as `app.py`
- **Static files not serving**: Check `.gitignore` isn't excluding needed files

### Author
EDUSMART Solutions

### License
All rights reserved
