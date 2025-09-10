// Dashboard JavaScript

// Load user info on page load
document.addEventListener('DOMContentLoaded', function() {
    const userName = localStorage.getItem('userName');
    if (userName) {
        document.getElementById('userName').textContent = userName;
    }
});

// Run career assessment
async function runAssessment() {
    const userId = localStorage.getItem('userId');
    
    if (!userId) {
        alert('Please register first!');
        window.location.href = '/';
        return;
    }
    
    document.getElementById('loadingMessage').textContent = 'Analyzing your profile...';
    
    try {
        const response = await fetch('/api/assess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: parseInt(userId) })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayRecommendations(data);
        } else {
            alert('Assessment failed: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during assessment');
    }
}

// Display recommendations
function displayRecommendations(data) {
    // Hide loading message
    document.getElementById('loadingMessage').style.display = 'none';
    document.getElementById('recommendationsContainer').style.display = 'block';
    
    // Update summary cards
    document.getElementById('careersAnalyzed').textContent = data.assessment_summary.total_careers_analyzed;
    document.getElementById('topMatchScore').textContent = Math.round(data.assessment_summary.top_match_score) + '%';
    document.getElementById('skillsEvaluated').textContent = data.assessment_summary.skills_evaluated;
    
    // Display recommendations
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = data.recommendations.map((rec, index) => `
        <div class="recommendation-card">
            <span class="match-score">${Math.round(rec.match_score)}% Match</span>
            <h3>${index + 1}. ${rec.career_title}</h3>
            <p>${rec.career_details.description}</p>
            <p><strong>Industry:</strong> ${rec.career_details.industry}</p>
            <p><strong>Salary Range:</strong> ${rec.career_details.average_salary_range}</p>
            <p><strong>Growth Potential:</strong> ${rec.career_details.growth_potential}</p>
            <p><strong>Reasoning:</strong> ${rec.reasoning}</p>
            <div>
                <strong>Skills to Learn:</strong>
                ${rec.skill_gaps.map(skill => `<span class="skill-gap">${skill}</span>`).join('')}
            </div>
            <button onclick="getLearningPath(${rec.career_id})" style="margin-top: 1rem;">
                View Learning Path
            </button>
        </div>
    `).join('');
}

// Get learning path for a specific career
async function getLearningPath(careerId) {
    const userId = localStorage.getItem('userId');
    
    try {
        const response = await fetch('/api/learning-path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                career_id: careerId,
                user_id: parseInt(userId)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayLearningPath(data.learning_path);
        } else {
            alert('Failed to get learning path');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching learning path');
    }
}

// Display learning path
function displayLearningPath(learningPath) {
    document.getElementById('learningPathContainer').style.display = 'block';
    
    const learningPathDiv = document.getElementById('learningPath');
    learningPathDiv.innerHTML = `
        <div style="background: #f8f9fa; padding: 2rem; border-radius: 10px; margin-top: 1rem;">
            <h3>Career Goal: ${learningPath.career_goal}</h3>
            <p><strong>Estimated Timeline:</strong> ${learningPath.estimated_timeline}</p>
            
            <h4>Your Current Skills:</h4>
            <p>${learningPath.current_skills.join(', ') || 'None specified'}</p>
            
            <h4>Skills to Learn:</h4>
            <p>${learningPath.skills_to_learn.join(', ') || 'Already have all required skills!'}</p>
            
            <h4>Learning Phases:</h4>
            ${learningPath.steps.map(step => `
                <div style="margin: 1rem 0; padding: 1rem; background: white; border-radius: 5px;">
                    <h5>${step.phase} (${step.duration})</h5>
                    <p><strong>Focus:</strong> ${step.focus}</p>
                    <p><strong>Skills:</strong> ${step.skills.join(', ') || 'N/A'}</p>
                </div>
            `).join('')}
            
            <h4>Learning Resources:</h4>
            ${Object.entries(learningPath.learning_resources).map(([skill, info]) => `
                <div style="margin: 0.5rem 0;">
                    <strong>${skill}:</strong> ${info.resources.join(', ')} 
                    <span style="color: #666;">(${info.difficulty})</span>
                </div>
            `).join('') || '<p>Check our resources section for learning materials</p>'}
        </div>
    `;
    
    // Scroll to learning path
    learningPathDiv.scrollIntoView({ behavior: 'smooth' });
}
