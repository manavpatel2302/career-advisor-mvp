"""
Demo script to test all features of the Career Advisor MVP
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_section(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print('='*50)

def test_api():
    """Test all API endpoints"""
    
    print_section("🧪 TESTING CAREER ADVISOR MVP")
    
    # 1. Test careers endpoint
    print("\n1️⃣ Fetching available careers...")
    response = requests.get(f"{BASE_URL}/api/careers")
    if response.status_code == 200:
        careers = response.json()
        print(f"✅ Found {len(careers)} career paths:")
        for career in careers[:3]:  # Show first 3
            print(f"   - {career['title']}: {career['average_salary_range']}")
    
    # 2. Test skills endpoint
    print("\n2️⃣ Fetching available skills...")
    response = requests.get(f"{BASE_URL}/api/skills")
    if response.status_code == 200:
        skills = response.json()
        print(f"✅ Found {len(skills)} skills available")
        for skill in skills[:3]:  # Show first 3
            print(f"   - {skill['name']} ({skill['difficulty_level']})")
    
    # 3. Register a test user
    print("\n3️⃣ Registering a test student...")
    test_user = {
        "name": "Rahul Sharma",
        "email": f"rahul.test{int(time.time())}@student.com",
        "age": 21,
        "education_level": "Bachelor",
        "interests": ["Technology", "Startups", "AI"],
        "current_skills": ["Python", "Data Structures", "Excel"]
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=test_user)
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data['user_id']
        print(f"✅ User registered successfully! ID: {user_id}")
        print(f"   Name: {test_user['name']}")
        print(f"   Skills: {', '.join(test_user['current_skills'])}")
    else:
        print(f"❌ Registration failed: {response.text}")
        return
    
    # 4. Run assessment
    print("\n4️⃣ Running career assessment...")
    assessment_data = {"user_id": user_id}
    
    response = requests.post(f"{BASE_URL}/api/assess", json=assessment_data)
    if response.status_code == 200:
        results = response.json()
        print("✅ Assessment completed!")
        print(f"\n📊 Assessment Summary:")
        print(f"   - Careers analyzed: {results['assessment_summary']['total_careers_analyzed']}")
        print(f"   - Top match score: {results['assessment_summary']['top_match_score']:.1f}%")
        print(f"   - Skills evaluated: {results['assessment_summary']['skills_evaluated']}")
        
        print(f"\n🎯 Top 3 Career Recommendations:")
        for i, rec in enumerate(results['recommendations'][:3], 1):
            print(f"\n   {i}. {rec['career_title']}")
            print(f"      Match Score: {rec['match_score']:.1f}%")
            print(f"      Industry: {rec['career_details']['industry']}")
            print(f"      Salary: {rec['career_details']['average_salary_range']}")
            print(f"      Reasoning: {rec['reasoning']}")
            if rec['skill_gaps']:
                print(f"      Skills to learn: {', '.join(rec['skill_gaps'][:3])}")
    
    # 5. Get learning path for top recommendation
    if results['recommendations']:
        print("\n5️⃣ Getting learning path for top recommendation...")
        top_career_id = results['recommendations'][0]['career_id']
        
        learning_path_data = {
            "career_id": top_career_id,
            "user_id": user_id
        }
        
        response = requests.post(f"{BASE_URL}/api/learning-path", json=learning_path_data)
        if response.status_code == 200:
            path_data = response.json()
            learning_path = path_data['learning_path']
            
            print(f"✅ Learning Path for: {learning_path['career_goal']}")
            print(f"   Estimated Timeline: {learning_path['estimated_timeline']}")
            print(f"\n   📚 Learning Phases:")
            for phase in learning_path['steps']:
                if phase['skills']:
                    print(f"      • {phase['phase']} ({phase['duration']})")
                    print(f"        Focus: {phase['focus']}")
                    print(f"        Skills: {', '.join(phase['skills'])}")
            
            print(f"\n   📖 Learning Resources Available:")
            for skill, info in list(learning_path['learning_resources'].items())[:3]:
                print(f"      • {skill} ({info['difficulty']})")
                print(f"        Resources: {', '.join(info['resources'][:2])}")

def test_different_profiles():
    """Test with different student profiles"""
    print_section("🎭 TESTING DIFFERENT STUDENT PROFILES")
    
    profiles = [
        {
            "name": "Priya - Business Enthusiast",
            "email": f"priya{int(time.time())}@test.com",
            "age": 22,
            "education_level": "Master",
            "interests": ["Business", "Management", "Corporate"],
            "current_skills": ["Communication Skills", "Excel", "Leadership"]
        },
        {
            "name": "Amit - Creative Designer",
            "email": f"amit{int(time.time())}@test.com", 
            "age": 20,
            "education_level": "Bachelor",
            "interests": ["Design", "Art", "Freelance"],
            "current_skills": ["UI Design", "Figma", "Photoshop"]
        },
        {
            "name": "Sneha - Data Enthusiast",
            "email": f"sneha{int(time.time())}@test.com",
            "age": 23,
            "education_level": "Bachelor",
            "interests": ["Analytics", "AI", "Research"],
            "current_skills": ["Python", "Machine Learning", "Statistics"]
        }
    ]
    
    for profile in profiles:
        print(f"\n\n🧑 Testing: {profile['name']}")
        print(f"   Skills: {', '.join(profile['current_skills'])}")
        
        # Register user
        response = requests.post(f"{BASE_URL}/api/register", json=profile)
        if response.status_code == 200:
            user_id = response.json()['user_id']
            
            # Run assessment
            response = requests.post(f"{BASE_URL}/api/assess", json={"user_id": user_id})
            if response.status_code == 200:
                results = response.json()
                top_rec = results['recommendations'][0]
                print(f"   ✅ Top Match: {top_rec['career_title']} ({top_rec['match_score']:.1f}%)")
                print(f"   💰 Salary Range: {top_rec['career_details']['average_salary_range']}")

if __name__ == "__main__":
    try:
        # Check if server is running
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Server is running at http://localhost:5000")
            
            # Run tests
            test_api()
            test_different_profiles()
            
            print_section("✨ ALL TESTS COMPLETED SUCCESSFULLY!")
            print("\n📌 You can now:")
            print("   1. Open http://localhost:5000 in your browser")
            print("   2. Register as a student")
            print("   3. Take the assessment")
            print("   4. View your personalized recommendations")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("Please run: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
