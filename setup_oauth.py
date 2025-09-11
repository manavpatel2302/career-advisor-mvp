#!/usr/bin/env python3
"""
OAuth Setup Script for Career Advisor MVP
This script helps you configure Google and LinkedIn OAuth credentials
"""

import os
import sys
import json
from pathlib import Path
import webbrowser
from urllib.parse import quote

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(number, text):
    """Print a formatted step"""
    print(f"\n✅ Step {number}: {text}")
    print("-" * 40)

def update_env_file(key, value):
    """Update or add a key in the .env file"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found. Creating one...")
        env_path.touch()
    
    # Read existing content
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Check if key exists and update it
    key_found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            key_found = True
            break
    
    # If key doesn't exist, append it
    if not key_found:
        lines.append(f"\n{key}={value}\n")
    
    # Write back to file
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Updated {key} in .env file")

def setup_google_oauth():
    """Setup Google OAuth"""
    print_header("Google OAuth Setup")
    
    print("📌 To set up Google OAuth, you need to:")
    print("1. Go to Google Cloud Console")
    print("2. Create a new project or select existing one")
    print("3. Enable Google+ API")
    print("4. Create OAuth 2.0 credentials")
    
    open_browser = input("\n🌐 Open Google Cloud Console in browser? (y/n): ").lower()
    if open_browser == 'y':
        webbrowser.open("https://console.cloud.google.com/apis/credentials")
    
    print("\n📝 After creating your OAuth client:")
    print("   - Application type: Web application")
    print("   - Authorized JavaScript origins:")
    print("     • http://localhost:5000")
    print("     • https://career-advisor-mvp.vercel.app")
    
    client_id = input("\n🔑 Enter your Google Client ID: ").strip()
    
    if client_id:
        update_env_file("GOOGLE_CLIENT_ID", client_id)
        
        # Also update the JavaScript file
        js_file = Path("static/js/social_auth.js")
        if js_file.exists():
            with open(js_file, 'r') as f:
                content = f.read()
            
            # Replace the placeholder
            content = content.replace(
                "const GOOGLE_CLIENT_ID = '973526458923-your-google-client-id.apps.googleusercontent.com';",
                f"const GOOGLE_CLIENT_ID = '{client_id}';"
            )
            
            with open(js_file, 'w') as f:
                f.write(content)
            
            print("✅ Updated Google Client ID in social_auth.js")
    else:
        print("⚠️  Skipping Google OAuth setup")

def setup_linkedin_oauth():
    """Setup LinkedIn OAuth"""
    print_header("LinkedIn OAuth Setup")
    
    print("📌 To set up LinkedIn OAuth, you need to:")
    print("1. Go to LinkedIn Developers")
    print("2. Create a new app")
    print("3. Configure OAuth 2.0 settings")
    print("4. Request 'Sign In with LinkedIn using OpenID Connect' product")
    
    open_browser = input("\n🌐 Open LinkedIn Developers in browser? (y/n): ").lower()
    if open_browser == 'y':
        webbrowser.open("https://www.linkedin.com/developers/apps")
    
    print("\n📝 Add these Authorized redirect URLs:")
    print("   • http://localhost:5000/auth/linkedin/callback")
    print("   • https://career-advisor-mvp.vercel.app/auth/linkedin/callback")
    
    client_id = input("\n🔑 Enter your LinkedIn Client ID: ").strip()
    client_secret = input("🔐 Enter your LinkedIn Client Secret: ").strip()
    
    if client_id:
        update_env_file("LINKEDIN_CLIENT_ID", client_id)
        
        # Also update the JavaScript file
        js_file = Path("static/js/social_auth.js")
        if js_file.exists():
            with open(js_file, 'r') as f:
                content = f.read()
            
            # Replace the placeholder
            content = content.replace(
                "const LINKEDIN_CLIENT_ID = 'your-linkedin-client-id';",
                f"const LINKEDIN_CLIENT_ID = '{client_id}';"
            )
            
            with open(js_file, 'w') as f:
                f.write(content)
            
            print("✅ Updated LinkedIn Client ID in social_auth.js")
    
    if client_secret:
        update_env_file("LINKEDIN_CLIENT_SECRET", client_secret)
    
    if not client_id and not client_secret:
        print("⚠️  Skipping LinkedIn OAuth setup")

def setup_demo_mode():
    """Configure demo mode"""
    print_header("Demo Mode Configuration")
    
    print("📌 Demo mode allows testing without real OAuth credentials")
    
    enable_demo = input("\n🎮 Enable demo mode? (y/n): ").lower()
    
    if enable_demo == 'y':
        update_env_file("DEMO_MODE", "True")
        print("✅ Demo mode enabled")
        print("   Users can test with mock authentication")
    else:
        update_env_file("DEMO_MODE", "False")
        print("✅ Demo mode disabled")
        print("   Real OAuth credentials will be required")

def verify_setup():
    """Verify the OAuth setup"""
    print_header("Verifying Setup")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    checks = {
        "Google Client ID": os.getenv('GOOGLE_CLIENT_ID', ''),
        "LinkedIn Client ID": os.getenv('LINKEDIN_CLIENT_ID', ''),
        "LinkedIn Client Secret": os.getenv('LINKEDIN_CLIENT_SECRET', ''),
        "JWT Secret": os.getenv('JWT_SECRET', ''),
        "Demo Mode": os.getenv('DEMO_MODE', 'False')
    }
    
    all_good = True
    for key, value in checks.items():
        if value and value not in ['', 'your-', 'change-this']:
            print(f"✅ {key}: Configured")
        else:
            print(f"⚠️  {key}: Not configured")
            if key != "Demo Mode":
                all_good = False
    
    if all_good or os.getenv('DEMO_MODE') == 'True':
        print("\n🎉 Setup complete! You can now run the application.")
        return True
    else:
        print("\n⚠️  Some configurations are missing.")
        print("   You can still run in demo mode for testing.")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    print("📦 Installing required Python packages...")
    os.system("pip install -r requirements.txt")
    print("✅ Dependencies installed")

def main():
    """Main setup function"""
    print_header("🚀 Career Advisor MVP - OAuth Setup Wizard")
    
    print("This wizard will help you configure:")
    print("  • Google Sign-In")
    print("  • LinkedIn OAuth")
    print("  • Demo mode for testing")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("\n❌ Python 3.7+ is required")
        sys.exit(1)
    
    # Install dependencies first
    install_deps = input("\n📦 Install/update Python dependencies? (y/n): ").lower()
    if install_deps == 'y':
        install_dependencies()
    
    # Setup OAuth providers
    setup_google = input("\n🔷 Set up Google OAuth? (y/n): ").lower()
    if setup_google == 'y':
        setup_google_oauth()
    
    setup_linkedin = input("\n🔷 Set up LinkedIn OAuth? (y/n): ").lower()
    if setup_linkedin == 'y':
        setup_linkedin_oauth()
    
    # Setup demo mode
    setup_demo_mode()
    
    # Verify setup
    verify_setup()
    
    # Offer to run the app
    print("\n" + "="*60)
    run_app = input("\n🚀 Run the application now? (y/n): ").lower()
    if run_app == 'y':
        print("\n🌟 Starting Career Advisor MVP...")
        print("   Open http://localhost:5000 in your browser")
        print("   Press Ctrl+C to stop the server\n")
        os.system("python app.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
