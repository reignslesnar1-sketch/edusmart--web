#!/bin/bash
# EDUSMART Deployment Helper Script
# This script helps push your code to GitHub and deploy to Render

echo "======================================"
echo "EDUSMART Deployment Helper"
echo "======================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Check current git status
echo "📊 Current Git Status:"
git status
echo ""

# Ask for GitHub repository URL
echo "🔗 To push to GitHub:"
echo ""
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/edusmart.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Repository URL is required"
    exit 1
fi

# Add remote and push
echo ""
echo "🚀 Setting up remote and pushing..."

# Remove existing remote if it exists
git remote remove origin 2>/dev/null

# Add new remote
git remote add origin "$REPO_URL"

# Push to main branch
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "📱 Next steps for Render deployment:"
    echo "1. Go to https://dashboard.render.com"
    echo "2. Click 'New +' and select 'Web Service'"
    echo "3. Connect your GitHub account and select this repository"
    echo "4. Configure:"
    echo "   - Name: edusmart-exam-system"
    echo "   - Environment: Python"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: python app.py"
    echo "5. Click 'Create Web Service'"
    echo ""
    echo "Render will deploy automatically! 🎉"
else
    echo "❌ Failed to push to GitHub"
    echo "Please check your repository URL and try again"
    exit 1
fi
