# EDUSMART Deployment - Simple Setup Script
# This script initializes Git and prepares your code for GitHub

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  EDUSMART - Web Deployment Setup" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "[*] Checking if Git is installed..." -ForegroundColor Yellow

$gitCheck = git --version 2>$null
if ($gitCheck) {
    Write-Host "[OK] Git is installed: $gitCheck" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Git is NOT installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Then restart PowerShell and run this script again" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit
}

# Get deployment folder
$deployPath = "C:\Users\Administrator\Desktop\EDUSMART SOLUTIONS\web_deployment"
Write-Host ""
Write-Host "[+] Working in: $deployPath" -ForegroundColor Cyan

# Change to deployment folder
Set-Location $deployPath

# Configure Git
Write-Host "[*] Configuring Git..." -ForegroundColor Yellow
git config --global user.email "edusmart@school.com" 2>$null
git config --global user.name "EDUSMART Admin" 2>$null
Write-Host "[OK] Git configured" -ForegroundColor Green

# Initialize repository
Write-Host "[*] Initializing Git repository..." -ForegroundColor Yellow
git init 2>$null
Write-Host "[OK] Repository initialized" -ForegroundColor Green

# Add all files
Write-Host "[*] Adding files..." -ForegroundColor Yellow
git add . 2>$null
Write-Host "[OK] Files added" -ForegroundColor Green

# Create initial commit
Write-Host "[*] Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit - EDUSMART web app for Render deployment" 2>$null
Write-Host "[OK] Initial commit created" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "  Git Setup Complete!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""

# Show next steps
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. CREATE GITHUB REPOSITORY" -ForegroundColor White
Write-Host "   Go to: https://github.com/new" -ForegroundColor Gray
Write-Host "   Name: edusmart-web" -ForegroundColor Gray
Write-Host "   Click 'Create repository'" -ForegroundColor Gray
Write-Host ""

Write-Host "2. COPY GITHUB COMMANDS" -ForegroundColor White
Write-Host "   GitHub will show commands like:" -ForegroundColor Gray
Write-Host "   - git branch -M main" -ForegroundColor Gray
Write-Host "   - git remote add origin https://github.com/YOUR-USERNAME/edusmart-web.git" -ForegroundColor Gray
Write-Host "   - git push -u origin main" -ForegroundColor Gray
Write-Host ""

Write-Host "3. PASTE IN THIS POWERSHELL WINDOW" -ForegroundColor White
Write-Host "   Right-click → Paste to run the commands" -ForegroundColor Gray
Write-Host ""

Write-Host "4. DEPLOY TO RENDER" -ForegroundColor White
Write-Host "   Go to: https://dashboard.render.com" -ForegroundColor Gray
Write-Host "   New Web Service → Select edusmart-web repo" -ForegroundColor Gray
Write-Host ""

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter when ready to open GitHub"

# Open GitHub
Start-Process "https://github.com/new"

Write-Host ""
Write-Host "GitHub is opening in your browser..." -ForegroundColor Yellow
Write-Host "Create the repository, then return here and paste the commands" -ForegroundColor Yellow
Write-Host ""
