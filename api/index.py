"""
Vercel Serverless Function Handler for Career Advisor MVP
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set environment variables if not present
if not os.getenv('GEMINI_API_KEY'):
    os.environ['GEMINI_API_KEY'] = 'AIzaSyCKjW_jlXUGHzo5fyfyX9F0uUNjhKFdtfg'
if not os.getenv('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'career-advisor-secret-key-2024-secure-random-string'

# Import the Flask app
from app import app as application

# Vercel expects a variable named 'app'
app = application

# For local testing
if __name__ == "__main__":
    application.run(debug=False)
