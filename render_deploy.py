#!/usr/bin/env python3
"""
EDUSMART Render Deployment Script
Automatically deploys the app to Render using the API
"""

import os
import sys
import json
import subprocess
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

GITHUB_REPO = "https://github.com/reignslesnar1-sketch/edusmart--web"
RENDER_API_URL = "https://api.render.com/v1/services"

def get_render_api_key():
    """Get Render API key from user or environment"""
    api_key = os.environ.get('RENDER_API_KEY')
    if not api_key:
        print("\n" + "="*60)
        print("EDUSMART - Render Deployment")
        print("="*60)
        print("\nTo deploy to Render, you need an API key.")
        print("Get it from: https://dashboard.render.com/account/api-tokens")
        print("\nSteps:")
        print("1. Go to https://dashboard.render.com")
        print("2. Click your profile icon → Account")
        print("3. Go to 'API Tokens' section")
        print("4. Click 'Create API Token'")
        print("5. Copy the token and paste it below")
        print("\n" + "-"*60)
        api_key = input("\nPaste your Render API Key: ").strip()
        
        if not api_key:
            print("❌ API key is required")
            sys.exit(1)
    
    return api_key

def deploy_to_render(api_key):
    """Deploy the app to Render using the API"""
    
    deployment_data = {
        "type": "web_service",
        "name": "edusmart-exam-system",
        "ownerId": None,
        "region": "ohio",
        "envSpecificDetails": {
            "env": "python"
        },
        "repo": GITHUB_REPO,
        "branch": "main",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "python app.py",
        "envVars": [
            {
                "key": "PORT",
                "value": "5000"
            },
            {
                "key": "FLASK_ENV",
                "value": "production"
            }
        ]
    }
    
    print("\n📤 Creating Render web service...")
    print(f"📦 Repository: {GITHUB_REPO}")
    print("⚙️  Build Command: pip install -r requirements.txt")
    print("▶️  Start Command: python app.py")
    
    try:
        data = json.dumps(deployment_data).encode('utf-8')
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        request = Request(RENDER_API_URL, data=data, headers=headers, method='POST')
        
        with urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            service_id = result.get('service', {}).get('id')
            service_url = result.get('service', {}).get('serviceDetails', {}).get('url')
            
            print("\n" + "="*60)
            print("✅ DEPLOYMENT SUCCESSFUL!")
            print("="*60)
            print(f"\n🆔 Service ID: {service_id}")
            print(f"🌐 Service URL: {service_url}")
            print(f"\n📊 Dashboard: https://dashboard.render.com/web/{service_id}")
            print("\n⏳ Render is now building and deploying your app...")
            print("   This usually takes 2-5 minutes.")
            print(f"\n✨ Your app will be live at: {service_url}")
            print("\n" + "="*60)
            
            return True
            
    except HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8'))
        print(f"\n❌ Deployment failed!")
        print(f"Error: {error_data.get('message', str(e))}")
        return False
    except URLError as e:
        print(f"\n❌ Connection error: {e}")
        print("Make sure you have internet connection and the API key is correct")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def main():
    """Main deployment function"""
    print("\n" + "="*60)
    print("🚀 EDUSMART - Automated Render Deployment")
    print("="*60)
    print("\nThis script will deploy your app to Render.")
    print("Your GitHub repository must be connected to Render first.")
    print("\nVerifying GitHub connection...")
    
    # Check if repo exists
    try:
        subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                      capture_output=True, check=True)
        print("✅ GitHub repository configured")
    except:
        print("❌ GitHub repository not configured")
        sys.exit(1)
    
    # Get API key
    api_key = get_render_api_key()
    
    # Deploy
    if deploy_to_render(api_key):
        print("\n✅ Deployment initiated successfully!")
        print("   Check your Render dashboard to monitor the build progress.")
        sys.exit(0)
    else:
        print("\n❌ Deployment failed. Please try again or check the error above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
