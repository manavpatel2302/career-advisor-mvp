# 🎯 Career Advisor MVP - Personalized AI Career Guidance for Indian Students

## Overview
A personalized AI-powered career advisor that helps Indian students discover suitable career paths based on their skills, interests, and the evolving job market. The platform uses Google's Gemini AI to provide intelligent recommendations and personalized learning paths.

## Features
- **User Profile Creation**: Students can register with their educational background, skills, and interests
- **AI-Powered Assessment**: Intelligent career matching using Google's Gemini AI
- **Career Recommendations**: Personalized career suggestions with match scores
- **Skill Gap Analysis**: Identifies skills needed for desired career paths
- **Learning Roadmap**: Customized learning paths with resources and timelines
- **Indian Market Focus**: Career paths and salary ranges specific to the Indian job market

## Tech Stack
- **Backend**: Python Flask
- **AI**: Google Gemini API
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with gradient themes

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key (free tier available)

### 2. Installation

```bash
# Clone or navigate to the project directory
cd career-advisor-mvp

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the `.env.example` file to `.env`:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
```

2. Edit `.env` and add your Google Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your free API key from: https://makersuite.google.com/app/apikey

### 4. Initialize Database

```bash
python database/init_db.py
```

This will create the database and populate it with sample career paths and skills.

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage Guide

### For Students:

1. **Register**: Click "Get Started" and create your profile with:
   - Basic information (name, email, age)
   - Education level
   - Interests (Technology, Design, Business, etc.)
   - Current skills (Python, Communication, Excel, etc.)

2. **Assessment**: Navigate to the Assessment page to:
   - Select your technical skills
   - Rate your soft skills
   - Choose work environment preferences
   - Describe your career goals

3. **View Recommendations**: Go to Dashboard to:
   - See your top career matches with percentage scores
   - Understand why each career is recommended
   - Identify skill gaps

4. **Learning Path**: For each recommended career:
   - View personalized learning roadmap
   - See estimated timeline
   - Access learning resources
   - Track progress through phases

## Sample Careers Included

The MVP includes 8 popular career paths in India:
- Software Engineer (₹4-15 LPA)
- Data Scientist (₹6-20 LPA)
- Digital Marketing Manager (₹4-12 LPA)
- Product Manager (₹8-25 LPA)
- Chartered Accountant (₹6-15 LPA)
- UI/UX Designer (₹4-12 LPA)
- Civil Engineer (₹3-10 LPA)
- Content Creator (₹2-10 LPA)

## API Endpoints

- `POST /api/register` - Register new user
- `GET /api/careers` - Get all career paths
- `GET /api/skills` - Get all skills
- `POST /api/assess` - Run career assessment
- `POST /api/learning-path` - Get personalized learning path

## Project Structure

```
career-advisor-mvp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── database/
│   ├── init_db.py        # Database initialization
│   └── career_advisor.db # SQLite database (created on init)
├── templates/
│   ├── index.html        # Landing page
│   ├── dashboard.html    # User dashboard
│   └── assessment.html   # Skills assessment
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       ├── app.js        # Main JavaScript
│       ├── dashboard.js  # Dashboard functionality
│       └── assessment.js # Assessment functionality
└── README.md            # This file
```

## Future Enhancements

- Add more career paths and emerging roles
- Integrate with job portals for real-time market data
- Add progress tracking and gamification
- Include mentor matching feature
- Add regional language support
- Implement advanced AI features with Vertex AI
- Add certification recommendations
- Include interview preparation module

## Troubleshooting

1. **No AI recommendations**: Ensure your Gemini API key is correctly set in `.env`
2. **Database errors**: Run `python database/init_db.py` to reinitialize
3. **Port already in use**: Change port in `app.py` last line
4. **Module not found**: Ensure virtual environment is activated and dependencies installed

## Contributing

This is an MVP version. Feel free to:
- Add more career paths
- Improve AI prompts
- Enhance UI/UX
- Add new features
- Fix bugs

## License

MIT License - Feel free to use and modify for educational purposes.

## Contact

For questions or suggestions, please open an issue in the repository.

---

**Note**: This is an MVP (Minimum Viable Product) designed for demonstration and can be extended with additional features for production use.
