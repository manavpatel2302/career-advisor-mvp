// Main JavaScript for Career Advisor

// Load careers on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCareers();
});

// Show registration modal
function showRegistrationForm() {
    document.getElementById('registrationModal').style.display = 'block';
}

// Close modal
function closeModal() {
    document.getElementById('registrationModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('registrationModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Handle registration form submission
document.getElementById('registrationForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        age: parseInt(document.getElementById('age').value) || null,
        education_level: document.getElementById('educationLevel').value,
        interests: document.getElementById('interests').value.split(',').map(s => s.trim()).filter(s => s),
        current_skills: document.getElementById('skills').value.split(',').map(s => s.trim()).filter(s => s)
    };
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Registration successful! Redirecting to dashboard...');
            localStorage.setItem('userId', data.user_id);
            localStorage.setItem('userName', formData.name);
            window.location.href = '/dashboard';
        } else {
            alert('Registration failed: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during registration');
    }
});

// Load and display careers
async function loadCareers() {
    try {
        const response = await fetch('/api/careers');
        const careers = await response.json();
        
        const careerList = document.getElementById('careerList');
        if (careerList) {
            careerList.innerHTML = careers.map(career => `
                <div class="career-item">
                    <h3>${career.title}</h3>
                    <p>${career.description}</p>
                    <p class="salary">Salary: ${career.average_salary_range}</p>
                    <span class="industry">${career.industry}</span>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading careers:', error);
    }
}
