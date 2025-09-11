from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from social_auth import social_auth_bp

# Load environment variables
load_dotenv()
load_dotenv('.env.production')  # Also try loading production env

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.getenv('FLASK_SECRET_KEY', 'career-advisor-secret-key-2024-secure-random-string'))
CORS(app)

# Register social auth blueprint
app.register_blueprint(social_auth_bp)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None
    print("Warning: Gemini API key not found. AI features will be limited.")

# Database helper functions
def get_db_connection():
    # Use /tmp for Vercel serverless functions
    db_path = '/tmp/career_advisor.db' if os.environ.get('VERCEL') else 'database/career_advisor.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database if it doesn't exist"""
    db_path = '/tmp/career_advisor.db' if os.environ.get('VERCEL') else 'database/career_advisor.db'
    if not os.path.exists(db_path):
        # For Vercel, we'll create a simple in-memory database structure
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                education_level TEXT,
                interests TEXT,
                current_skills TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS career_paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                industry TEXT,
                required_skills TEXT,
                average_salary_min INTEGER,
                average_salary_max INTEGER,
                growth_potential TEXT,
                education_requirements TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                difficulty_level TEXT,
                learning_resources TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

# Initialize database on startup
init_db()

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (name, email, age, education_level, interests, current_skills)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data.get('age'),
            data.get('education_level'),
            json.dumps(data.get('interests', [])),
            json.dumps(data.get('current_skills', []))
        ))
        conn.commit()
        user_id = cursor.lastrowid
        session['user_id'] = user_id
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'User registered successfully'
        })
    except sqlite3.IntegrityError:
        return jsonify({
            'success': False,
            'message': 'Email already exists'
        }), 400
    finally:
        conn.close()

@app.route('/api/careers', methods=['GET'])
def get_careers():
    """Get all available career paths"""
    conn = get_db_connection()
    careers = conn.execute('SELECT * FROM career_paths').fetchall()
    conn.close()
    
    career_list = []
    for career in careers:
        career_dict = dict(career)
        career_dict['required_skills'] = json.loads(career_dict['required_skills'])
        career_list.append(career_dict)
    
    return jsonify(career_list)

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all available skills"""
    conn = get_db_connection()
    skills = conn.execute('SELECT * FROM skills').fetchall()
    conn.close()
    
    skill_list = []
    for skill in skills:
        skill_dict = dict(skill)
        skill_dict['learning_resources'] = json.loads(skill_dict['learning_resources'])
        skill_list.append(skill_dict)
    
    return jsonify(skill_list)

@app.route('/api/assess', methods=['POST'])
def assess_user():
    """Assess user and provide career recommendations"""
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'message': 'User ID required'}), 400
    
    # Get user data
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    user_dict = dict(user)
    user_interests = json.loads(user_dict['interests']) if user_dict['interests'] else []
    user_skills = json.loads(user_dict['current_skills']) if user_dict['current_skills'] else []
    
    # Get all career paths
    careers = conn.execute('SELECT * FROM career_paths').fetchall()
    
    recommendations = []
    
    if model:
        # Use AI for personalized recommendations
        for career in careers:
            career_dict = dict(career)
            required_skills = json.loads(career_dict['required_skills'])
            
            # Create prompt for AI
            prompt = f"""
            Analyze the career match for an Indian student with the following profile:
            - Education Level: {user_dict['education_level']}
            - Age: {user_dict['age']}
            - Interests: {', '.join(user_interests)}
            - Current Skills: {', '.join(user_skills)}
            
            Career Path: {career_dict['title']}
            Required Skills: {', '.join(required_skills)}
            Industry: {career_dict['industry']}
            
            Provide:
            1. Match score (0-100)
            2. Brief reasoning (2-3 sentences)
            3. Top 3 skill gaps
            
            Format response as JSON with keys: match_score, reasoning, skill_gaps
            """
            
            try:
                response = model.generate_content(prompt)
                # Parse AI response (simplified for MVP)
                ai_analysis = response.text
                
                # Simple scoring based on skill overlap (fallback if AI parsing fails)
                skill_overlap = len(set(user_skills) & set(required_skills))
                match_score = min(100, (skill_overlap / max(len(required_skills), 1)) * 100 + 20)
                
                recommendations.append({
                    'career_id': career_dict['id'],
                    'career_title': career_dict['title'],
                    'match_score': match_score,
                    'reasoning': f"Based on your skills and interests, this career aligns well with your profile.",
                    'skill_gaps': list(set(required_skills) - set(user_skills))[:3],
                    'career_details': career_dict
                })
            except Exception as e:
                print(f"AI error: {e}")
                # Fallback to simple matching
                skill_overlap = len(set(user_skills) & set(required_skills))
                match_score = min(100, (skill_overlap / max(len(required_skills), 1)) * 100)
                
                recommendations.append({
                    'career_id': career_dict['id'],
                    'career_title': career_dict['title'],
                    'match_score': match_score,
                    'reasoning': f"You have {skill_overlap} out of {len(required_skills)} required skills.",
                    'skill_gaps': list(set(required_skills) - set(user_skills))[:3],
                    'career_details': career_dict
                })
    else:
        # Simple rule-based matching without AI
        for career in careers:
            career_dict = dict(career)
            required_skills = json.loads(career_dict['required_skills'])
            
            skill_overlap = len(set(user_skills) & set(required_skills))
            match_score = min(100, (skill_overlap / max(len(required_skills), 1)) * 100)
            
            recommendations.append({
                'career_id': career_dict['id'],
                'career_title': career_dict['title'],
                'match_score': match_score,
                'reasoning': f"You have {skill_overlap} out of {len(required_skills)} required skills.",
                'skill_gaps': list(set(required_skills) - set(user_skills))[:3],
                'career_details': career_dict
            })
    
    # Sort by match score
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Save assessment results
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO assessments (user_id, assessment_type, results, recommendations)
        VALUES (?, ?, ?, ?)
    ''', (
        user_id,
        'career_match',
        json.dumps({'user_skills': user_skills, 'user_interests': user_interests}),
        json.dumps(recommendations[:5])  # Top 5 recommendations
    ))
    
    # Save top recommendations
    for rec in recommendations[:3]:
        cursor.execute('''
            INSERT INTO recommendations (user_id, career_path_id, match_score, reasoning, skill_gaps)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            rec['career_id'],
            rec['match_score'],
            rec['reasoning'],
            json.dumps(rec['skill_gaps'])
        ))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'recommendations': recommendations[:5],
        'assessment_summary': {
            'total_careers_analyzed': len(careers),
            'top_match_score': recommendations[0]['match_score'] if recommendations else 0,
            'skills_evaluated': len(user_skills)
        }
    })

@app.route('/api/learning-path', methods=['POST'])
def get_learning_path():
    """Generate personalized learning path"""
    data = request.json
    career_id = data.get('career_id')
    user_id = data.get('user_id')
    
    conn = get_db_connection()
    
    # Get career details
    career = conn.execute('SELECT * FROM career_paths WHERE id = ?', (career_id,)).fetchone()
    if not career:
        conn.close()
        return jsonify({'success': False, 'message': 'Career not found'}), 404
    
    career_dict = dict(career)
    required_skills = json.loads(career_dict['required_skills'])
    
    # Get user's current skills
    user = conn.execute('SELECT current_skills FROM users WHERE id = ?', (user_id,)).fetchone()
    user_skills = json.loads(user['current_skills']) if user and user['current_skills'] else []
    
    # Get skill details and resources
    skill_gaps = list(set(required_skills) - set(user_skills))
    learning_resources = {}
    
    for skill in skill_gaps:
        skill_data = conn.execute('SELECT * FROM skills WHERE name = ?', (skill,)).fetchone()
        if skill_data:
            skill_dict = dict(skill_data)
            learning_resources[skill] = {
                'difficulty': skill_dict['difficulty_level'],
                'resources': json.loads(skill_dict['learning_resources'])
            }
    
    conn.close()
    
    # Create learning path
    learning_path = {
        'career_goal': career_dict['title'],
        'current_skills': user_skills,
        'skills_to_learn': skill_gaps,
        'learning_resources': learning_resources,
        'estimated_timeline': f"{len(skill_gaps) * 2} - {len(skill_gaps) * 4} months",
        'steps': [
            {
                'phase': 'Foundation',
                'duration': '1-2 months',
                'skills': [s for s in skill_gaps if learning_resources.get(s, {}).get('difficulty') == 'Beginner'][:2],
                'focus': 'Build fundamental knowledge'
            },
            {
                'phase': 'Core Skills',
                'duration': '2-3 months',
                'skills': [s for s in skill_gaps if learning_resources.get(s, {}).get('difficulty') == 'Intermediate'][:3],
                'focus': 'Develop job-ready skills'
            },
            {
                'phase': 'Advanced',
                'duration': '2-3 months',
                'skills': [s for s in skill_gaps if learning_resources.get(s, {}).get('difficulty') == 'Advanced'][:2],
                'focus': 'Master specialized skills'
            }
        ]
    }
    
    return jsonify({
        'success': True,
        'learning_path': learning_path
    })

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

@app.route('/assessment')
def assessment():
    """Skills assessment page"""
    return render_template('assessment.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
