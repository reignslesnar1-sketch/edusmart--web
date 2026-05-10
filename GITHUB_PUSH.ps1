# GitHub Push Helper - Customize Commands with Your Username

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  EDUSMART - GitHub Push Setup" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Ask for GitHub username
Write-Host "First, what is your GitHub username?" -ForegroundColor Yellow
Write-Host "(The username you use to login to github.com)" -ForegroundColor Gray
Write-Host ""

$username = Read-Host "Enter your GitHub username"

if ([string]::IsNullOrWhiteSpace($username)) {
    Write-Host "[ERROR] Username cannot be empty!" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Great! Your username is: $username" -ForegroundColor Green
Write-Host ""

# Create the actual commands
$commands = @(
    "& `"C:\Program Files\Git\cmd\git.exe`" branch -M main",
    "& `"C:\Program Files\Git\cmd\git.exe`" remote add origin https://github.com/$username/edusmart-web.git",
    "& `"C:\Program Files\Git\cmd\git.exe`" push -u origin main"
)

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  COMMANDS TO RUN (Copy one at a time)" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Display commands
for ($i = 0; $i -lt $commands.Count; $i++) {
    $num = $i + 1
    Write-Host "Step $num of 3:" -ForegroundColor Yellow
    Write-Host $commands[$i] -ForegroundColor White
    Write-Host ""
}

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  BEFORE YOU PASTE:" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Did you create the GitHub repository?" -ForegroundColor Yellow
Write-Host "   Go to: https://github.com/new" -ForegroundColor Gray
Write-Host "   Name: edusmart-web" -ForegroundColor Gray
Write-Host "   Click 'Create repository'" -ForegroundColor Gray
Write-Host ""

Write-Host "2. When asked for password:" -ForegroundColor Yellow
Write-Host "   a) Go to: https://github.com/settings/tokens" -ForegroundColor Gray
Write-Host "   b) Click 'Generate new token'" -ForegroundColor Gray
Write-Host "   c) Name: deployment" -ForegroundColor Gray
Write-Host "   d) Check: repo" -ForegroundColor Gray
Write-Host "   e) Click 'Generate token'" -ForegroundColor Gray
Write-Host "   f) Copy the token (long string)" -ForegroundColor Gray
Write-Host "   g) Paste as password when prompted" -ForegroundColor Gray
Write-Host ""

# Ask to proceed
$proceed = Read-Host "Ready to continue? (y/n)"

if ($proceed -ne 'y' -and $proceed -ne 'Y') {
    Write-Host "Exiting. Run this script again when ready." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "  PASTE THESE COMMANDS ONE AT A TIME:" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""

$currentPath = Get-Location
Write-Host "Current location: $currentPath" -ForegroundColor Gray
Write-Host ""

# Copy first command to clipboard and ask user to paste
Write-Host "Ready to push to GitHub?" -ForegroundColor Yellow
$ready = Read-Host "Press Enter when ready, or type 'skip' to copy commands to file"

if ($ready -eq 'skip') {
    # Save commands to file
    $outputFile = "C:\Users\Administrator\Desktop\EDUSMART SOLUTIONS\web_deployment\GITHUB_COMMANDS.txt"
    
    @"
GITHUB PUSH COMMANDS FOR: $username
======================================

Paste these commands one at a time in PowerShell:

COMMAND 1:
& "C:\Program Files\Git\cmd\git.exe" branch -M main

COMMAND 2:
& "C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/$username/edusmart-web.git

COMMAND 3:
& "C:\Program Files\Git\cmd\git.exe" push -u origin main

======================================

When prompted for password:
- Username: $username
- Password: Your Personal Access Token (from https://github.com/settings/tokens)

STEPS:
1. Create token: https://github.com/settings/tokens
2. Click "Generate new token"
3. Name: deployment
4. Check: repo
5. Click "Generate token"
6. Copy the token value
7. Paste back here when asked for password
"@ | Set-Content $outputFile

    Write-Host "[OK] Commands saved to: $outputFile" -ForegroundColor Green
    Write-Host ""
    exit
}

# Navigate to deployment folder
cd "C:\Users\Administrator\Desktop\EDUSMART SOLUTIONS\web_deployment"

Write-Host ""
Write-Host "Running commands..." -ForegroundColor Yellow
Write-Host ""

try {
    # Command 1
    Write-Host "Executing: git branch -M main" -ForegroundColor Cyan
    & "C:\Program Files\Git\cmd\git.exe" branch -M main
    Write-Host "[OK] Branch set to main" -ForegroundColor Green
    Write-Host ""
    
    # Command 2
    Write-Host "Executing: git remote add origin" -ForegroundColor Cyan
    & "C:\Program Files\Git\cmd\git.exe" remote add origin "https://github.com/$username/edusmart-web.git"
    Write-Host "[OK] Remote repository added" -ForegroundColor Green
    Write-Host ""
    
    # Command 3
    Write-Host "Executing: git push -u origin main" -ForegroundColor Cyan
    Write-Host "(You'll be prompted for your GitHub credentials)" -ForegroundColor Yellow
    Write-Host ""
    & "C:\Program Files\Git\cmd\git.exe" push -u origin main
    Write-Host ""
    Write-Host "[OK] Code pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "[ERROR] Something went wrong:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit
}

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "  SUCCESS!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your code is now on GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEP: Deploy to Render" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Click 'New +' > 'Web Service'" -ForegroundColor White
Write-Host "3. Connect repository: edusmart-web" -ForegroundColor White
Write-Host "4. Settings:" -ForegroundColor White
Write-Host "   Build: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   Start: gunicorn -w 4 -b 0.0.0.0:\$PORT app:web_app" -ForegroundColor Gray
Write-Host "5. Click 'Create Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "Your app will be live in 2-3 minutes!" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to finish"
