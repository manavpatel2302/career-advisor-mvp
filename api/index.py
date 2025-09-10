"""
Vercel Serverless Function Handler for Career Advisor MVP
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the Flask app
from app import app

# Vercel expects a variable named 'app'
# This will be used as the entry point
application = app

# For local testing
if __name__ == "__main__":
    app.run(debug=False)
