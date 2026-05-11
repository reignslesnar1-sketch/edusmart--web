@echo off
REM EDUSMART Deployment Setup - Direct Git Access

cd /d "C:\Users\Administrator\Desktop\EDUSMART SOLUTIONS\web_deployment"

echo.
echo =====================================================
echo  EDUSMART - Web Deployment Setup
echo =====================================================
echo.

echo [+] Configuring Git...
git config --global user.email "edusmart@school.com"
git config --global user.name "EDUSMART Admin"

echo [+] Initializing repository...
git init

echo [+] Adding files...
git add .

echo [+] Creating initial commit...
git commit -m "Initial commit - EDUSMART web app for Render deployment"

echo.
echo =====================================================
echo [OK] Setup Complete!
echo =====================================================
echo.

echo NEXT STEPS:
echo.
echo 1. CREATE GITHUB REPOSITORY
echo    Go to: https://github.com/new
echo    Repository name: edusmart-web
echo    Click 'Create repository'
echo.
echo 2. COPY GITHUB COMMANDS
echo    Look for: "or push an existing repository from the command line"
echo    Copy all 3 commands
echo.
echo 3. PASTE IN COMMAND PROMPT
echo    Right-click this window title bar
echo    Click: Edit ^> Paste
echo.
echo 4. DEPLOY TO RENDER
echo    Go to: https://dashboard.render.com
echo    New Web Service ^> Select edusmart-web
echo.

pause

REM Open GitHub
start https://github.com/new

echo GitHub is opening in your browser...
echo Create the repository and copy the commands back here.
echo.
pause
