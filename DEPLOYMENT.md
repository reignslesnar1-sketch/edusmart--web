# EDUSMART Solutions - Deployment Guide to Render.com

## 📋 Quick Overview

This guide helps you deploy the EDUSMART exam management system's web application to **Render.com** (free hosting).

Your system will be accessible online via a public URL like: `https://your-app-name.onrender.com`

---

## ✅ Prerequisites

1. **GitHub Account** - Create one at [github.com](https://github.com)
2. **Render Account** - Create one at [render.com](https://render.com) (Free tier available)
3. **Git installed** - Download from [git-scm.com](https://git-scm.com)
4. **Your database file** - Ensure `exam_system.db` is ready

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Files

1. Copy your database file (`exam_system.db`) to this folder:
   ```
   web_deployment/exam_system.db
   ```

2. You should now have these files in `web_deployment/`:
   - `app.py` - Main Flask application
   - `requirements.txt` - Python dependencies
   - `Procfile` - Render configuration
   - `.gitignore` - Files to exclude from git
   - `.env.example` - Environment variables template
   - `exam_system.db` - Your database
   - `DEPLOYMENT.md` - This file

### Step 2: Set Up Git Repository

Open PowerShell/Command Prompt in the `web_deployment` folder and run:

```bash
# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - EDUSMART web app for Render deployment"

# Configure your Git identity (one-time setup)
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

### Step 3: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository called `edusmart-web`
3. **Do NOT initialize with README** (you already have files)
4. Click "Create repository"
5. Follow the commands shown for "...or push an existing repository from the command line"

Copy and run these commands in PowerShell (replace `YOUR-USERNAME`):

```bash
# Add remote repository
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/edusmart-web.git

# Push to GitHub
git push -u origin main
```

### Step 4: Deploy to Render

#### Method A: Using Render Dashboard (Easiest for beginners)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select **"Connect a repository"** → Choose `edusmart-web`
5. Fill in the form:
   - **Name:** `edusmart-web` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT app:web_app`
6. Click **"Create Web Service"**
7. Wait for build to complete (2-3 minutes)

#### Method B: Using render.yaml (Advanced)

Create `render.yaml` in your repo:

```yaml
services:
  - type: web
    name: edusmart-web
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT app:web_app
    envVars:
      - key: FLASK_ENV
        value: production
```

Then push to GitHub and Render will auto-deploy.

### Step 5: Access Your App

Once deployment is complete, you'll get a URL like:
```
https://edusmart-web.onrender.com
```

Your app will be live! 🎉

---

## 🔧 Common Issues & Fixes

### Issue: Build fails with "No module named flask"
**Fix:** Ensure `requirements.txt` is in the root folder

### Issue: App crashes after deploy
**Check Logs:**
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Look for error messages

### Issue: Database not found after deployment
**Solution:** Upload `exam_system.db` to your GitHub repo:
```bash
git add exam_system.db
git commit -m "Add production database"
git push
```

### Issue: Free tier app goes to sleep
**Note:** Render's free tier goes to sleep after 15 minutes of inactivity. Upgrade to paid tier to keep it always running.

---

## 📝 Making Updates

After making changes to your code:

```bash
# Navigate to web_deployment folder
cd C:\Users\Administrator\Desktop\EDUSMART\ SOLUTIONS\web_deployment

# Add changes
git add .

# Commit
git commit -m "Update: describe your changes"

# Push to GitHub
git push

# Render auto-deploys in 1-2 minutes!
```

---

## 🌐 Features Available Online

✅ Teacher Login/Registration  
✅ Student Results Viewing  
✅ Mark Submission  
✅ Exam Management  
✅ Secure Access  

---

## 💰 Pricing

- **Free Tier:** Perfect for small schools
  - 750 hours/month (enough for continuous running)
  - SQLite database
  - Auto-deployed from GitHub

- **Paid Tier:** For larger institutions
  - Unlimited uptime
  - PostgreSQL database
  - Advanced analytics

---

## 📧 Support

For issues:
1. Check Render Logs
2. Check Flask error messages
3. Verify `requirements.txt` has all dependencies
4. Ensure database file is committed to Git

---

## 🎯 Next Steps

1. ✅ Complete all steps above
2. ✅ Test the web app
3. ✅ Share URL with teachers/students
4. ✅ Monitor logs for issues
5. ✅ Keep database updated

---

**Your EDUSMART web app is now online and accessible from anywhere! 🚀**
