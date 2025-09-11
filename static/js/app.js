/**
 * CareerCompass AI - Main Application JavaScript
 * Version: 2.0
 * Author: Senior Development Team
 */

// ==========================================
// Global Configuration
// ==========================================
const APP_CONFIG = {
    API_BASE_URL: window.location.origin + '/api',
    ANIMATION_DURATION: 300,
    DEBOUNCE_DELAY: 500,
    SESSION_TIMEOUT: 30 * 60 * 1000, // 30 minutes
};

// ==========================================
// State Management
// ==========================================
const AppState = {
    user: null,
    isAuthenticated: false,
    currentModal: null,
    assessmentData: {},
    careerRecommendations: [],
};

// ==========================================
// Utility Functions
// ==========================================
const Utils = {
    // Debounce function for performance
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Form validation
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    validatePassword(password) {
        // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
        const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/;
        return re.test(password);
    },

    validatePhone(phone) {
        const re = /^[0-9]{10}$/;
        return re.test(phone);
    },

    // Show toast notification
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    },

    // Format currency
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    },

    // Store data in localStorage
    saveToStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (e) {
            console.error('Failed to save to localStorage:', e);
        }
    },

    // Get data from localStorage
    getFromStorage(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Failed to get from localStorage:', e);
            return null;
        }
    },

    // API request helper
    async apiRequest(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        };

        const config = { ...defaultOptions, ...options };
        
        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(`${APP_CONFIG.API_BASE_URL}${endpoint}`, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
};

// ==========================================
// Modal Management
// ==========================================
function showRegisterModal() {
    closeAllModals();
    const modal = document.getElementById('registerModal');
    if (modal) {
        modal.classList.add('active');
        AppState.currentModal = 'registerModal';
    }
}

function showLoginModal() {
    closeAllModals();
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.classList.add('active');
        AppState.currentModal = 'loginModal';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        if (AppState.currentModal === modalId) {
            AppState.currentModal = null;
        }
    }
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('active');
    });
    AppState.currentModal = null;
}

function switchToLogin() {
    closeModal('registerModal');
    setTimeout(() => showLoginModal(), 300);
}

function switchToRegister() {
    closeModal('loginModal');
    setTimeout(() => showRegisterModal(), 300);
}

// ==========================================
// Authentication
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    // Register form submission
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(registerForm);
            const data = {
                name: `${formData.get('firstName')} ${formData.get('lastName')}`,
                email: formData.get('email'),
                password: formData.get('password'),
                phone: formData.get('phone')
            };
            
            // Validation
            if (!Utils.validateEmail(data.email)) {
                Utils.showToast('Please enter a valid email address', 'error');
                return;
            }
            
            if (!Utils.validatePassword(data.password)) {
                Utils.showToast('Password must be at least 8 characters with uppercase, lowercase, and numbers', 'error');
                return;
            }
            
            if (!Utils.validatePhone(data.phone)) {
                Utils.showToast('Please enter a valid 10-digit phone number', 'error');
                return;
            }
            
            try {
                // Show loading
                const submitBtn = registerForm.querySelector('.btn-submit');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
                submitBtn.disabled = true;
                
                const response = await Utils.apiRequest('/register', {
                    method: 'POST',
                    body: data
                });
                
                if (response.success) {
                    Utils.showToast('Account created successfully!', 'success');
                    AppState.user = response.user;
                    AppState.isAuthenticated = true;
                    Utils.saveToStorage('user', response.user);
                    
                    // Close modal and redirect
                    closeModal('registerModal');
                    setTimeout(() => {
                        window.location.href = '/assessment';
                    }, 1000);
                } else {
                    Utils.showToast(response.message || 'Registration failed', 'error');
                }
                
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            } catch (error) {
                Utils.showToast('An error occurred. Please try again.', 'error');
                console.error('Registration error:', error);
            }
        });
    }
    
    // Login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(loginForm);
            const data = {
                email: formData.get('email'),
                password: formData.get('password'),
                remember: formData.get('remember') ? true : false
            };
            
            // Validation
            if (!Utils.validateEmail(data.email)) {
                Utils.showToast('Please enter a valid email address', 'error');
                return;
            }
            
            try {
                // Show loading
                const submitBtn = loginForm.querySelector('.btn-submit');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing In...';
                submitBtn.disabled = true;
                
                const response = await Utils.apiRequest('/login', {
                    method: 'POST',
                    body: data
                });
                
                if (response.success) {
                    Utils.showToast('Welcome back!', 'success');
                    AppState.user = response.user;
                    AppState.isAuthenticated = true;
                    Utils.saveToStorage('user', response.user);
                    
                    // Close modal and redirect
                    closeModal('loginModal');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1000);
                } else {
                    Utils.showToast(response.message || 'Invalid credentials', 'error');
                }
                
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            } catch (error) {
                Utils.showToast('An error occurred. Please try again.', 'error');
                console.error('Login error:', error);
            }
        });
    }
});

// ==========================================
// Assessment Functions
// ==========================================
function startAssessment() {
    if (!AppState.isAuthenticated) {
        Utils.showToast('Please sign in to start the assessment', 'info');
        showLoginModal();
        return;
    }
    
    window.location.href = '/assessment';
}

// ==========================================
// Demo Video
// ==========================================
function watchDemo() {
    // Create video modal
    const videoModal = document.createElement('div');
    videoModal.className = 'modal active';
    videoModal.innerHTML = `
        <div class="modal-content video-modal">
            <span class="modal-close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <h2>How CareerCompass AI Works</h2>
            <div class="video-container">
                <iframe 
                    width="100%" 
                    height="400" 
                    src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
                    frameborder="0" 
                    allowfullscreen
                ></iframe>
            </div>
        </div>
    `;
    document.body.appendChild(videoModal);
}

// ==========================================
// Pricing Plans
// ==========================================
function selectPlan(planType) {
    if (!AppState.isAuthenticated) {
        Utils.showToast('Please sign in to select a plan', 'info');
        showLoginModal();
        return;
    }
    
    // Handle plan selection
    switch(planType) {
        case 'starter':
            window.location.href = '/assessment';
            break;
        case 'professional':
            window.location.href = '/checkout?plan=professional';
            break;
        case 'enterprise':
            window.location.href = '/contact?type=enterprise';
            break;
    }
}

// ==========================================
// Initialize Charts
// ==========================================
function initializeCharts() {
    const chartCanvas = document.getElementById('careerChart');
    if (chartCanvas) {
        const ctx = chartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Technical', 'Creative', 'Leadership', 'Analytical', 'Communication'],
                datasets: [{
                    label: 'Your Skills',
                    data: [85, 72, 90, 78, 88],
                    backgroundColor: 'rgba(99, 102, 241, 0.2)',
                    borderColor: 'rgba(99, 102, 241, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// ==========================================
// Smooth Scroll
// ==========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ==========================================
// Initialize on Load
// ==========================================
window.addEventListener('load', () => {
    // Check for saved user
    const savedUser = Utils.getFromStorage('user');
    if (savedUser) {
        AppState.user = savedUser;
        AppState.isAuthenticated = true;
    }
    
    // Initialize charts
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }
    
    // Close modals on outside click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal.id);
            }
        });
    });
    
    // Close modals on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && AppState.currentModal) {
            closeModal(AppState.currentModal);
        }
    });
});

// ==========================================
// Add CSS for Toast Notifications
// ==========================================
const toastStyles = document.createElement('style');
toastStyles.innerHTML = `
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        padding: 1rem 1.5rem;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        z-index: 9999;
    }
    
    .toast.show {
        transform: translateX(0);
    }
    
    .toast-content {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .toast-success .fa-check-circle {
        color: #10b981;
    }
    
    .toast-error .fa-exclamation-circle {
        color: #ef4444;
    }
    
    .toast-info .fa-info-circle {
        color: #3b82f6;
    }
    
    .video-modal .modal-content {
        max-width: 800px;
    }
    
    .video-container {
        position: relative;
        padding-bottom: 56.25%;
        height: 0;
        overflow: hidden;
    }
    
    .video-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
`;
document.head.appendChild(toastStyles);
