@echo off
REM EDUSMART Deployment Setup Script
REM This script will initialize git, create GitHub repo, and deploy to Render

echo.
echo ======================================================
echo  EDUSMART Solutions - Deployment Setup
echo ======================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [!] Git is not installed on your system
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, close this window and run this script again
    echo.
    pause
    exit /b 1
)

echo [+] Git is installed
echo.

REM Change to deployment folder
cd /d "C:\Users\Administrator\Desktop\EDUSMART SOLUTIONS\web_deployment"

echo [+] Setting up Git configuration...
git config --global user.email "edusmart@school.com"
git config --global user.name "EDUSMART Admin"

echo [+] Initializing Git repository...
git init

echo [+] Adding all files...
git add .

echo [+] Creating initial commit...
git commit -m "Initial commit - EDUSMART web app for Render deployment"

echo.
echo ======================================================
echo  NEXT STEPS
echo ======================================================
echo.
echo 1. GITHUB SETUP:
echo    Visit: https://github.com/new
echo    Create a new repository named: edusmart-web
echo    Do NOT initialize with README (you have files)
echo    Copy the commands under "push an existing repository"
echo.
echo 2. PUSH TO GITHUB:
echo    Run the GitHub commands in PowerShell
echo.
echo 3. RENDER DEPLOYMENT:
echo    Visit: https://dashboard.render.com
echo    Sign up with GitHub
echo    New --> Web Service
echo    Select edusmart-web repository
echo    Build Command: pip install -r requirements.txt
echo    Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:web_app
echo    Click Create Web Service
echo.
echo 4. WAIT FOR DEPLOYMENT:
echo    Your app will be live in 2-3 minutes!
echo.
echo ======================================================
echo.
pause
