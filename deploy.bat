@echo off
REM EDUSMART Deployment Helper Script (Windows)
REM This script helps push your code to GitHub and deploy to Render

echo.
echo ======================================
echo EDUSMART Deployment Helper
echo ======================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [X] Git is not installed. Please install Git first.
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Show current git status
echo [INFO] Current Git Status:
git status
echo.

REM Ask for GitHub repository URL
set /p REPO_URL="Enter your GitHub repository URL: "

if "%REPO_URL%"=="" (
    echo [X] Repository URL is required
    pause
    exit /b 1
)

echo.
echo [INFO] Setting up remote and pushing...
echo.

REM Remove existing remote if it exists
git remote remove origin 2>nul

REM Add new remote
git remote add origin %REPO_URL%

REM Rename branch to main and push
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo [OK] Successfully pushed to GitHub!
    echo.
    echo [INFO] Next steps for Render deployment:
    echo.
    echo 1. Go to https://dashboard.render.com
    echo 2. Click 'New +' and select 'Web Service'
    echo 3. Connect your GitHub account and select this repository
    echo 4. Configure:
    echo    - Name: edusmart-exam-system
    echo    - Environment: Python
    echo    - Build Command: pip install -r requirements.txt
    echo    - Start Command: python app.py
    echo 5. Click 'Create Web Service'
    echo.
    echo Render will deploy automatically!
    echo.
    pause
) else (
    echo.
    echo [X] Failed to push to GitHub
    echo Please check your repository URL and try again
    echo.
    pause
    exit /b 1
)
