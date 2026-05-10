@echo off
REM EDUSMART Git Installation Helper

cls
echo.
echo =====================================================
echo  EDUSMART - Git Installation Required
echo =====================================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is NOT installed on your system
    echo.
    echo ACTION REQUIRED:
    echo ============================================
    echo 1. Visit: https://git-scm.com/download/win
    echo.
    echo 2. Click the green download button
    echo.
    echo 3. Run the installer (Git-xxx-64-bit.exe)
    echo.
    echo 4. Click "Next" for all screens (use defaults)
    echo.
    echo 5. Wait for installation to complete
    echo.
    echo 6. RESTART YOUR COMPUTER
    echo.
    echo 7. Return to this folder and double-click this file again
    echo.
    timeout /t 5
    
    REM Open the Git download page
    start https://git-scm.com/download/win
    
    pause
    exit /b 1
) else (
    echo [OK] Git is installed!
    echo.
    echo Running EDUSMART deployment setup...
    echo.
    
    REM Change to current directory
    cd /d "%~dp0"
    
    REM Configure Git
    echo Configuring Git...
    git config --global user.email "edusmart@school.com" >nul 2>&1
    git config --global user.name "EDUSMART Admin" >nul 2>&1
    
    REM Initialize repository
    echo Initializing repository...
    git init >nul 2>&1
    
    REM Add files
    echo Adding files...
    git add . >nul 2>&1
    
    REM Commit
    echo Creating commit...
    git commit -m "Initial commit - EDUSMART web app" >nul 2>&1
    
    echo.
    echo =====================================================
    echo [OK] Git Setup Complete!
    echo =====================================================
    echo.
    echo NEXT STEPS:
    echo 1. Go to: https://github.com/new
    echo 2. Create repository: edusmart-web
    echo 3. Copy the commands shown
    echo 4. Paste them in PowerShell window
    echo.
    echo Then deploy to Render at: https://dashboard.render.com
    echo.
    
    pause
)
