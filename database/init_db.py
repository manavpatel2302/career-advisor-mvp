import sqlite3
import json
from datetime import datetime

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('database/career_advisor.db')
    cursor = conn.cursor()
    
    # Users table
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
    
    # Career paths table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS career_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            industry TEXT,
            average_salary_range TEXT,
            growth_potential TEXT,
            required_skills TEXT,
            education_requirements TEXT,
            job_outlook TEXT
        )
    ''')
    
    # Skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT,
            difficulty_level TEXT,
            learning_resources TEXT
        )
    ''')
    
    # Assessment results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            assessment_type TEXT,
            results TEXT,
            recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # User career recommendations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            career_path_id INTEGER,
            match_score REAL,
            reasoning TEXT,
            skill_gaps TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (career_path_id) REFERENCES career_paths (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def seed_sample_data():
    """Add sample career paths and skills relevant to Indian students"""
    conn = sqlite3.connect('database/career_advisor.db')
    cursor = conn.cursor()
    
    # Sample career paths popular in India
    career_paths = [
        {
            'title': 'Software Engineer',
            'description': 'Design, develop, and maintain software applications',
            'industry': 'Information Technology',
            'average_salary_range': '₹4-15 LPA',
            'growth_potential': 'Very High',
            'required_skills': json.dumps(['Python', 'Java', 'Data Structures', 'Algorithms', 'Git']),
            'education_requirements': 'B.Tech/BE in CS/IT or equivalent',
            'job_outlook': 'Excellent - High demand in India and globally'
        },
        {
            'title': 'Data Scientist',
            'description': 'Analyze complex data to help companies make better decisions',
            'industry': 'Analytics & AI',
            'average_salary_range': '₹6-20 LPA',
            'growth_potential': 'Very High',
            'required_skills': json.dumps(['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization']),
            'education_requirements': 'B.Tech/M.Tech or B.Sc/M.Sc in relevant field',
            'job_outlook': 'Excellent - Growing demand in Indian startups and MNCs'
        },
        {
            'title': 'Digital Marketing Manager',
            'description': 'Plan and execute digital marketing campaigns',
            'industry': 'Marketing & Advertising',
            'average_salary_range': '₹4-12 LPA',
            'growth_potential': 'High',
            'required_skills': json.dumps(['SEO', 'Social Media Marketing', 'Content Marketing', 'Analytics', 'Google Ads']),
            'education_requirements': 'Any Bachelor\'s degree with relevant certifications',
            'job_outlook': 'Very Good - Essential for all businesses'
        },
        {
            'title': 'Product Manager',
            'description': 'Lead product development from conception to launch',
            'industry': 'Product & Business',
            'average_salary_range': '₹8-25 LPA',
            'growth_potential': 'Very High',
            'required_skills': json.dumps(['Product Strategy', 'User Research', 'Data Analysis', 'Leadership', 'Agile']),
            'education_requirements': 'B.Tech/MBA preferred',
            'job_outlook': 'Excellent - High demand in tech companies'
        },
        {
            'title': 'Chartered Accountant',
            'description': 'Provide financial advice and handle accounts for organizations',
            'industry': 'Finance & Accounting',
            'average_salary_range': '₹6-15 LPA',
            'growth_potential': 'High',
            'required_skills': json.dumps(['Accounting', 'Taxation', 'Auditing', 'Financial Analysis', 'Tally/SAP']),
            'education_requirements': 'CA qualification from ICAI',
            'job_outlook': 'Good - Consistent demand across industries'
        },
        {
            'title': 'UI/UX Designer',
            'description': 'Design user interfaces and experiences for digital products',
            'industry': 'Design & Creative',
            'average_salary_range': '₹4-12 LPA',
            'growth_potential': 'High',
            'required_skills': json.dumps(['Figma', 'Adobe XD', 'User Research', 'Prototyping', 'Design Thinking']),
            'education_requirements': 'Bachelor\'s in Design or relevant portfolio',
            'job_outlook': 'Very Good - Growing with digital transformation'
        },
        {
            'title': 'Civil Engineer',
            'description': 'Design and oversee construction of infrastructure projects',
            'industry': 'Construction & Infrastructure',
            'average_salary_range': '₹3-10 LPA',
            'growth_potential': 'Moderate',
            'required_skills': json.dumps(['AutoCAD', 'Structural Analysis', 'Project Management', 'STAAD Pro', 'Site Management']),
            'education_requirements': 'B.Tech/BE in Civil Engineering',
            'job_outlook': 'Good - Infrastructure development in India'
        },
        {
            'title': 'Content Creator',
            'description': 'Create engaging content for various digital platforms',
            'industry': 'Media & Entertainment',
            'average_salary_range': '₹2-10 LPA',
            'growth_potential': 'High',
            'required_skills': json.dumps(['Video Editing', 'Content Writing', 'Social Media', 'SEO', 'Photography']),
            'education_requirements': 'Any degree with creative skills',
            'job_outlook': 'Very Good - Booming creator economy'
        }
    ]
    
    # Sample skills
    skills = [
        {'name': 'Python', 'category': 'Programming', 'difficulty_level': 'Intermediate', 
         'learning_resources': json.dumps(['Coursera', 'Udemy', 'YouTube - Corey Schafer'])},
        {'name': 'Machine Learning', 'category': 'AI/ML', 'difficulty_level': 'Advanced',
         'learning_resources': json.dumps(['Andrew Ng Course', 'Fast.ai', 'Kaggle Learn'])},
        {'name': 'Digital Marketing', 'category': 'Marketing', 'difficulty_level': 'Beginner',
         'learning_resources': json.dumps(['Google Digital Garage', 'HubSpot Academy', 'Udemy'])},
        {'name': 'Data Structures', 'category': 'Computer Science', 'difficulty_level': 'Intermediate',
         'learning_resources': json.dumps(['GeeksforGeeks', 'LeetCode', 'YouTube - Abdul Bari'])},
        {'name': 'Financial Analysis', 'category': 'Finance', 'difficulty_level': 'Intermediate',
         'learning_resources': json.dumps(['Coursera Finance Courses', 'Khan Academy', 'NSE Academy'])},
        {'name': 'UI Design', 'category': 'Design', 'difficulty_level': 'Intermediate',
         'learning_resources': json.dumps(['Figma YouTube', 'Design+Code', 'Dribbble'])},
        {'name': 'Communication Skills', 'category': 'Soft Skills', 'difficulty_level': 'Beginner',
         'learning_resources': json.dumps(['Coursera', 'LinkedIn Learning', 'Toastmasters'])},
        {'name': 'Project Management', 'category': 'Management', 'difficulty_level': 'Intermediate',
         'learning_resources': json.dumps(['PMI Resources', 'Coursera PM Certificate', 'Scrum.org'])}
    ]
    
    # Insert career paths
    for career in career_paths:
        cursor.execute('''
            INSERT OR IGNORE INTO career_paths 
            (title, description, industry, average_salary_range, growth_potential, 
             required_skills, education_requirements, job_outlook)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(career.values()))
    
    # Insert skills
    for skill in skills:
        cursor.execute('''
            INSERT OR IGNORE INTO skills (name, category, difficulty_level, learning_resources)
            VALUES (?, ?, ?, ?)
        ''', tuple(skill.values()))
    
    conn.commit()
    conn.close()
    print("Sample data added successfully!")

if __name__ == "__main__":
    init_database()
    seed_sample_data()
