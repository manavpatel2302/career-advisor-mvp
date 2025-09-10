// Assessment JavaScript

// Load skills on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSkills();
    setupRangeSliders();
});

// Load available skills
async function loadSkills() {
    try {
        const response = await fetch('/api/skills');
        const skills = await response.json();
        
        const technicalSkillsDiv = document.getElementById('technicalSkills');
        technicalSkillsDiv.innerHTML = skills.map(skill => `
            <div class="skill-checkbox" onclick="toggleSkill(this, '${skill.name}')">
                ${skill.name}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading skills:', error);
    }
}

// Toggle skill selection
function toggleSkill(element, skillName) {
    element.classList.toggle('selected');
}

// Setup range sliders
function setupRangeSliders() {
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        slider.addEventListener('input', function() {
            this.nextElementSibling.textContent = this.value;
        });
    });
}

// Submit assessment
async function submitAssessment() {
    const userId = localStorage.getItem('userId');
    
    if (!userId) {
        alert('Please register first!');
        window.location.href = '/';
        return;
    }
    
    // Collect selected skills
    const selectedSkills = Array.from(document.querySelectorAll('.skill-checkbox.selected'))
        .map(el => el.textContent.trim());
    
    // Collect soft skills ratings
    const softSkills = {
        communication: document.getElementById('communication').value,
        leadership: document.getElementById('leadership').value,
        problemSolving: document.getElementById('problemSolving').value,
        teamwork: document.getElementById('teamwork').value
    };
    
    // Collect interests
    const interests = Array.from(document.querySelectorAll('.interest-options input:checked'))
        .map(el => el.value);
    
    // Get future goals
    const futureGoals = document.getElementById('futureGoals').value;
    
    // Add high-rated soft skills to skills list
    Object.entries(softSkills).forEach(([skill, rating]) => {
        if (parseInt(rating) >= 4) {
            selectedSkills.push('Communication Skills');
        }
    });
    
    // Update user profile with new skills
    try {
        // First, run the assessment
        const response = await fetch('/api/assess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: parseInt(userId),
                skills: selectedSkills,
                interests: interests,
                future_goals: futureGoals
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Assessment complete! Redirecting to your results...');
            window.location.href = '/dashboard';
        } else {
            alert('Assessment failed: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during assessment');
    }
}
