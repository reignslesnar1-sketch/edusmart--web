# EDUSMART - Render Deployment Guide

## ✅ Step-by-Step Deployment to Render

### Prerequisites:
- GitHub Account (username: **reignslesnar1-sketch**)
- Render.com Account (free tier available)
- This code pushed to GitHub repository

---

## 📋 Step 1: Push Code to GitHub

### 1.1 Initialize Git Repository (First Time Only)
```bash
cd "c:\Users\Administrator\Desktop\KANGA SCHOOL LOGO"
git init
git add .
git commit -m "Initial EDUSMART deployment setup"
```

### 1.2 Add Remote Repository
```bash
git remote add origin https://github.com/reignslesnar1-sketch/EDUSMART.git
git branch -M main
git push -u origin main
```

### 1.3 For Future Updates
```bash
git add .
git commit -m "Updated features - enhanced student views"
git push origin main
```

---

## 🚀 Step 2: Deploy on Render.com

### 2.1 Create New Web Service
1. Go to **https://dashboard.render.com**
2. Click **"New +"** → Select **"Web Service"**
3. Click **"Connect Repository"**
4. Search for `EDUSMART` repository
5. Click **"Connect"**

### 2.2 Configure Web Service
```
Service Name: edusmart-school
Environment: Python 3
Region: Choose closest to you
```

### 2.3 Build & Start Settings
- **Build Command**: Leave blank (Render auto-detects)
- **Start Command**: `gunicorn app:app`

### 2.4 Environment Variables
No additional env vars needed (uses SQLite in `/tmp/`)

### 2.5 Deploy
- Click **"Create Web Service"**
- Wait for deployment (2-3 minutes)
- Once live, you'll get a URL like: `https://edusmart-school.onrender.com`

---

## 📊 Step 3: Access Your EDUSMART System

### Login to Dashboard
```
URL: https://edusmart-school.onrender.com
Default Access: Teacher Login or Register
```

### 🔑 Key Features Available

#### View All Students
```
URL: https://edusmart-school.onrender.com/students
- See all registered students
- Filter by grade and search
- Beautiful modern UI
- Mobile responsive
```

#### Export Student Data (JSON API)
```
URL: https://edusmart-school.onrender.com/api/students
Returns JSON with:
- All registered students
- Total count
- Grades covered
- School metadata
- GitHub username integration
```

#### Teacher Dashboard
```
URL: https://edusmart-school.onrender.com/dashboard
- Real-time statistics
- Quick access menu
- Submit marks
- View submissions
```

---

## 🔄 Step 4: Auto-Deployment with GitHub

### Enable Auto-Deploy
1. In Render dashboard, go to your Web Service
2. Settings → Deploy Hook
3. Copy the webhook URL
4. Go to GitHub repo Settings → Webhooks
5. Add new webhook with the Render URL
6. Content type: `application/json`
7. Trigger: `push` events

**Now every GitHub push will auto-deploy!**

---

## 💾 Database Information

### Database Location
- **Development**: `exam_system.db` (local file)
- **Render**: `/tmp/exam_system.db` (ephemeral storage)

### ⚠️ Important: Data Persistence
Render free tier uses ephemeral storage. Data is lost on app restart.

### ✅ Solution: Add PostgreSQL
```
1. On Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Add to your project
4. Render will provide DATABASE_URL
5. Update app.py to use PostgreSQL instead of SQLite
```

---

## 🧪 Testing Your Deployment

### Test Student Listing
```bash
# Open browser or use curl
curl https://edusmart-school.onrender.com/students
# Navigate to /api/students to see JSON output
```

### Create Test Teacher
1. Go to home page
2. Click "Register Teacher"
3. Fill form and register
4. Login with credentials
5. Add students via dashboard

### Add Sample Students
```bash
# You can import from CSV: Books_by_Form.csv
# Or add manually via the Teachers Portal
```

---

## 🐛 Troubleshooting

### App Won't Start
- Check logs on Render dashboard
- Ensure `requirements.txt` is correct
- Verify `app.py` has no syntax errors

### Database Connection Error
- SQLite works out of box - /tmp/ exists on Render
- All tables created automatically
- No manual setup needed

### 404 Routes Not Found
- Make sure Flask routes are defined in app.py
- Check file uploaded correctly
- Clear Render cache: Settings → Restart Instance

### Students Not Showing
- Check if database is initialized
- Manually add students via Teacher Portal
- Use `/api/students` endpoint to verify data

---

## 🔗 Frontend Links & Features

### Public Endpoints (No Login)
- `/` - Home page
- `/login` - Teacher login
- `/register` - Teacher registration
- `/candidate_login` - Student portal
- `/check_results` - Check exam results
- `/api/students` - JSON export (Public API)

### Protected Endpoints (Teacher Login Required)
- `/dashboard` - Main dashboard
- `/students` - View all students
- `/teachers` - View teachers
- `/submit_marks` - Submit exam marks
- `/view_submissions` - View mark submissions
- `/student_reports` - Reports page
- `/notifications` - Notifications

### Student Endpoints
- `/candidate_dashboard` - Student results view

---

## 📈 GitHub Integration

### Repository URL
```
https://github.com/reignslesnar1-sketch/EDUSMART
```

### GitHub Username
- Configured: **reignslesnar1-sketch**
- Display: Shows in Dashboard footer & API response

### Update System from GitHub
```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# Render auto-deploys within 1-2 minutes!
```

---

## 🎯 Next Steps

1. ✅ Push code to GitHub
2. ✅ Create Render Web Service
3. ✅ Deploy and test
4. ✅ Share deployment URL with teachers
5. ✅ Add students to system
6. ✅ Begin uploading marks

---

## 📞 Support

### Common Commands
```bash
# Check GitHub status
git status

# View deployment logs (Render)
# Dashboard → Service → Logs

# Test locally before deploying
python app.py
# Visit http://localhost:5000
```

### Deployment URL
```
https://edusmart-school.onrender.com
```

---

**All students registered to your system will be visible at:**
```
https://edusmart-school.onrender.com/students
```

**Data Export Available at:**
```
https://edusmart-school.onrender.com/api/students
```

---

*Setup Date: 2024 | System: EDUSMART v1.0 | GitHub: reignslesnar1-sketch*
