# 🚀 Quick Start Guide - Career Advisor MVP

## 1-Minute Setup

### Option A: Automatic Setup (Windows)
Just double-click `run.bat` and the application will:
- Create virtual environment
- Install all dependencies
- Initialize database
- Start the server

### Option B: Manual Setup

1. **Install Python dependencies:**
```bash
pip install Flask flask-cors google-generativeai python-dotenv
```

2. **Create `.env` file:**
   - Copy `.env.example` to `.env`
   - Add your Gemini API key (get free at https://makersuite.google.com/app/apikey)

3. **Initialize database:**
```bash
python database/init_db.py
```

4. **Run the app:**
```bash
python app.py
```

5. **Open browser:**
   Navigate to http://localhost:5000

## First Time Usage

1. Click "Get Started" on homepage
2. Fill registration form with:
   - Name: Your Name
   - Email: your@email.com
   - Age: 20
   - Education: Bachelor's Degree
   - Interests: Technology, Business
   - Skills: Python, Excel

3. Click "Create Profile"
4. You'll be redirected to Dashboard
5. Click "Run Career Assessment"
6. View your personalized recommendations!

## Test Without AI (No API Key)
The app works without Gemini API key using basic skill matching. You'll still get:
- Career recommendations based on skill overlap
- Skill gap analysis
- Learning paths

## Sample Test Data
Try these combinations for different results:

**Tech Profile:**
- Skills: Python, Data Structures, Git
- Interests: Technology, Startups
- Result: Software Engineer, Data Scientist

**Business Profile:**
- Skills: Communication Skills, Excel
- Interests: Business, Corporate
- Result: Product Manager, Digital Marketing

**Creative Profile:**
- Skills: UI Design, Photography
- Interests: Design, Freelance
- Result: UI/UX Designer, Content Creator

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "Port 5000 already in use" | Close other Flask apps or change port in app.py |
| "Database error" | Delete `database/career_advisor.db` and run `python database/init_db.py` |
| "No recommendations showing" | Make sure you have registered a user first |

## Features to Try

✅ **Registration** - Create multiple student profiles
✅ **Career Browser** - View all available career paths
✅ **Assessment** - Test different skill combinations
✅ **Recommendations** - Get AI-powered career matches
✅ **Learning Paths** - See personalized skill development plans
✅ **Skill Gap Analysis** - Identify what to learn next

## Next Steps

1. Add your Gemini API key for AI-powered recommendations
2. Customize career paths in `database/init_db.py`
3. Modify styling in `static/css/style.css`
4. Add more features as needed

---

**Need help?** Check the full README.md for detailed documentation.
