# EDUSMART Deployment Setup Script

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  EDUSMART Solutions - Complete Deployment Setup" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "[✓] Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] Git is NOT installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "After installation, restart PowerShell and run this script again"
    Write-Host ""
    Read-Host "Press Enter to open the Git download page"
    Start-Process "https://git-scm.com/download/win"
    exit 1
}

# Navigate to deployment folder
$deployPath = "C:\Users\Administrator\Desktop\EDUSMART SOLUTIONS\web_deployment"
Write-Host "[+] Navigating to: $deployPath" -ForegroundColor Cyan
Set-Location $deployPath

# Configure Git
Write-Host "[+] Configuring Git..." -ForegroundColor Yellow
git config --global user.email "edusmart@school.com"
git config --global user.name "EDUSMART Admin"

# Initialize repository
Write-Host "[+] Initializing Git repository..." -ForegroundColor Yellow
git init

# Add all files
Write-Host "[+] Adding all files to Git..." -ForegroundColor Yellow
git add .

# Create commit
Write-Host "[+] Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit - EDUSMART web app for Render deployment"

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "  Git Setup Complete!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""

# Display next steps
Write-Host "IMPORTANT - Follow these steps to deploy:" -ForegroundColor Yellow
Write-Host ""
Write-Host "STEP 1: Create GitHub Repository" -ForegroundColor Cyan
Write-Host "  1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "  2. Repository name: edusmart-web" -ForegroundColor White
Write-Host "  3. Click 'Create repository'" -ForegroundColor White
Write-Host "  4. Copy the commands shown (look for 'push an existing repository')" -ForegroundColor White
Write-Host ""

Write-Host "STEP 2: Push Code to GitHub" -ForegroundColor Cyan
Write-Host "  1. Return to PowerShell window" -ForegroundColor White
Write-Host "  2. Paste the GitHub commands one at a time:" -ForegroundColor White
Write-Host ""
Write-Host "     git branch -M main" -ForegroundColor Gray
Write-Host "     git remote add origin https://github.com/YOUR-USERNAME/edusmart-web.git" -ForegroundColor Gray
Write-Host "     git push -u origin main" -ForegroundColor Gray
Write-Host ""

Write-Host "STEP 3: Deploy to Render" -ForegroundColor Cyan
Write-Host "  1. Go to: https://dashboard.render.com" -ForegroundColor White
Write-Host "  2. Sign up (use GitHub login)" -ForegroundColor White
Write-Host "  3. Click 'New +' → 'Web Service'" -ForegroundColor White
Write-Host "  4. Select repository: edusmart-web" -ForegroundColor White
Write-Host "  5. Settings:" -ForegroundColor White
Write-Host "     - Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "     - Start Command: gunicorn -w 4 -b 0.0.0.0:\$PORT app:web_app" -ForegroundColor Gray
Write-Host "  6. Click 'Create Web Service'" -ForegroundColor White
Write-Host ""

Write-Host "STEP 4: Keep This Window Open" -ForegroundColor Cyan
Write-Host "  You'll need to paste your GitHub access token below" -ForegroundColor White
Write-Host ""

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Ready to proceed?" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter when you've completed Step 1 (created GitHub repo)"

Write-Host ""
Write-Host "Now complete Step 2 in this window:" -ForegroundColor Cyan
Write-Host ""

# Optionally open GitHub in browser
$github = Read-Host "Open GitHub in browser? (y/n)"
if ($github -eq 'y' -or $github -eq 'Y') {
    Start-Process "https://github.com/new"
}

Write-Host ""
Write-Host "Ready to push? Complete STEP 2 commands when prompted" -ForegroundColor Yellow
Write-Host ""
Write-Host "Script completed successfully!" -ForegroundColor Green
