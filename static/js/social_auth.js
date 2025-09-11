/**
 * Social Authentication Module
 * Handles Google and LinkedIn OAuth login
 */

// Google Sign-In Configuration
const GOOGLE_CLIENT_ID = '973526458923-your-google-client-id.apps.googleusercontent.com'; // Replace with your actual Google Client ID
const LINKEDIN_CLIENT_ID = 'your-linkedin-client-id'; // Replace with your LinkedIn Client ID

// Initialize Google Sign-In
function initializeGoogleSignIn() {
    google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleGoogleSignIn,
        auto_select: false,
        cancel_on_tap_outside: true,
    });

    // Render Google One Tap
    google.accounts.id.prompt((notification) => {
        if (notification.isNotDisplayed()) {
            console.log('Google One Tap not displayed:', notification.getNotDisplayedReason());
        } else if (notification.isSkippedMoment()) {
            console.log('Google One Tap skipped:', notification.getSkippedReason());
        }
    });
}

// Handle Google Sign-In
function handleGoogleSignIn(response) {
    // The response contains the JWT credential
    const credential = response.credential;
    
    // Decode the JWT to get user info
    const userInfo = parseJwt(credential);
    
    // Process the login
    processGoogleLogin({
        email: userInfo.email,
        name: userInfo.name,
        picture: userInfo.picture,
        sub: userInfo.sub, // Google user ID
        token: credential
    });
}

// Manual Google Sign-In trigger
function signInWithGoogle() {
    // Create a temporary div for the Google button
    const buttonDiv = document.createElement('div');
    buttonDiv.id = 'googleSignInButton';
    buttonDiv.style.display = 'none';
    document.body.appendChild(buttonDiv);

    google.accounts.id.renderButton(
        document.getElementById('googleSignInButton'),
        { 
            theme: 'outline', 
            size: 'large',
            type: 'standard',
            shape: 'rectangular',
            text: 'continue_with',
            logo_alignment: 'left'
        }
    );

    // Programmatically click the button
    const googleButton = document.querySelector('#googleSignInButton > div[role="button"]');
    if (googleButton) {
        googleButton.click();
    }

    // Clean up
    setTimeout(() => {
        document.body.removeChild(buttonDiv);
    }, 100);
}

// Process Google Login
async function processGoogleLogin(userData) {
    try {
        // Show loading state
        Utils.showToast('Signing in with Google...', 'info');
        
        // Send to backend API
        const response = await Utils.apiRequest('/auth/google', {
            method: 'POST',
            body: {
                token: userData.token,
                email: userData.email,
                name: userData.name,
                picture: userData.picture,
                google_id: userData.sub
            }
        });
        
        if (response.success) {
            // Save user data
            AppState.user = response.user;
            AppState.isAuthenticated = true;
            Utils.saveToStorage('user', response.user);
            Utils.saveToStorage('authMethod', 'google');
            
            // Close any open modals
            closeAllModals();
            
            // Show success message
            Utils.showToast(`Welcome, ${userData.name}!`, 'success');
            
            // Redirect based on user status
            if (response.isNewUser) {
                // New user - go to assessment
                setTimeout(() => {
                    window.location.href = '/assessment';
                }, 1000);
            } else {
                // Existing user - go to dashboard
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            }
        } else {
            Utils.showToast(response.message || 'Google sign-in failed', 'error');
        }
    } catch (error) {
        console.error('Google login error:', error);
        Utils.showToast('An error occurred during Google sign-in', 'error');
    }
}

// LinkedIn Sign-In
function signInWithLinkedIn() {
    // LinkedIn OAuth URL
    const linkedInAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?` +
        `response_type=code&` +
        `client_id=${LINKEDIN_CLIENT_ID}&` +
        `redirect_uri=${encodeURIComponent(window.location.origin + '/auth/linkedin/callback')}&` +
        `scope=${encodeURIComponent('r_liteprofile r_emailaddress')}&` +
        `state=${generateRandomState()}`;
    
    // Save state for verification
    const state = generateRandomState();
    Utils.saveToStorage('linkedin_oauth_state', state);
    
    // Open LinkedIn OAuth in popup
    const width = 500;
    const height = 600;
    const left = (window.screen.width - width) / 2;
    const top = (window.screen.height - height) / 2;
    
    const popup = window.open(
        linkedInAuthUrl,
        'LinkedIn Login',
        `width=${width},height=${height},left=${left},top=${top},toolbar=no,menubar=no`
    );
    
    // Check for popup close
    const checkPopup = setInterval(() => {
        if (popup && popup.closed) {
            clearInterval(checkPopup);
            // Check if login was successful
            const linkedInUser = Utils.getFromStorage('linkedInUser');
            if (linkedInUser) {
                processLinkedInLogin(linkedInUser);
                Utils.saveToStorage('linkedInUser', null); // Clear the data
            }
        }
    }, 1000);
}

// Process LinkedIn Login
async function processLinkedInLogin(userData) {
    try {
        // Show loading state
        Utils.showToast('Signing in with LinkedIn...', 'info');
        
        // Send to backend API
        const response = await Utils.apiRequest('/auth/linkedin', {
            method: 'POST',
            body: {
                email: userData.email,
                name: userData.name,
                linkedin_id: userData.id,
                picture: userData.picture
            }
        });
        
        if (response.success) {
            // Save user data
            AppState.user = response.user;
            AppState.isAuthenticated = true;
            Utils.saveToStorage('user', response.user);
            Utils.saveToStorage('authMethod', 'linkedin');
            
            // Close any open modals
            closeAllModals();
            
            // Show success message
            Utils.showToast(`Welcome, ${userData.name}!`, 'success');
            
            // Redirect based on user status
            if (response.isNewUser) {
                // New user - go to assessment
                setTimeout(() => {
                    window.location.href = '/assessment';
                }, 1000);
            } else {
                // Existing user - go to dashboard
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            }
        } else {
            Utils.showToast(response.message || 'LinkedIn sign-in failed', 'error');
        }
    } catch (error) {
        console.error('LinkedIn login error:', error);
        Utils.showToast('An error occurred during LinkedIn sign-in', 'error');
    }
}

// Helper function to parse JWT
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (error) {
        console.error('Error parsing JWT:', error);
        return null;
    }
}

// Generate random state for OAuth
function generateRandomState() {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
}

// Handle OAuth callback (for LinkedIn)
function handleOAuthCallback() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state');
    const error = urlParams.get('error');
    
    if (error) {
        console.error('OAuth error:', error);
        if (window.opener) {
            window.close();
        }
        return;
    }
    
    if (code && state) {
        // Verify state
        const savedState = Utils.getFromStorage('linkedin_oauth_state');
        if (state === savedState) {
            // Exchange code for token (this would be done on backend)
            exchangeLinkedInCode(code);
        } else {
            console.error('State mismatch in OAuth callback');
        }
    }
}

// Exchange LinkedIn authorization code for access token
async function exchangeLinkedInCode(code) {
    try {
        const response = await Utils.apiRequest('/auth/linkedin/exchange', {
            method: 'POST',
            body: { code }
        });
        
        if (response.success) {
            // Save user data for the parent window
            Utils.saveToStorage('linkedInUser', response.user);
            // Close the popup
            if (window.opener) {
                window.close();
            }
        }
    } catch (error) {
        console.error('Error exchanging LinkedIn code:', error);
        if (window.opener) {
            window.close();
        }
    }
}

// Sign out function
function signOut() {
    // Clear local storage
    Utils.saveToStorage('user', null);
    Utils.saveToStorage('authMethod', null);
    
    // Clear app state
    AppState.user = null;
    AppState.isAuthenticated = false;
    
    // Sign out from Google if applicable
    const authMethod = Utils.getFromStorage('authMethod');
    if (authMethod === 'google') {
        google.accounts.id.disableAutoSelect();
    }
    
    // Show message
    Utils.showToast('You have been signed out', 'info');
    
    // Redirect to home
    setTimeout(() => {
        window.location.href = '/';
    }, 1000);
}

// Initialize on page load
window.addEventListener('load', () => {
    // Initialize Google Sign-In if the library is loaded
    if (typeof google !== 'undefined' && google.accounts) {
        initializeGoogleSignIn();
    }
    
    // Check if this is an OAuth callback
    if (window.location.pathname === '/auth/linkedin/callback') {
        handleOAuthCallback();
    }
    
    // Check for existing session
    const savedUser = Utils.getFromStorage('user');
    const authMethod = Utils.getFromStorage('authMethod');
    
    if (savedUser && authMethod) {
        AppState.user = savedUser;
        AppState.isAuthenticated = true;
        
        // Update UI to show logged-in state
        updateAuthUI(savedUser);
    }
});

// Update UI based on authentication state
function updateAuthUI(user) {
    const navActions = document.querySelector('.nav-actions');
    
    if (user && navActions) {
        // Replace sign in/register buttons with user menu
        navActions.innerHTML = `
            <div class="user-menu">
                <button class="user-menu-toggle" onclick="toggleUserMenu()">
                    ${user.picture ? `<img src="${user.picture}" alt="${user.name}">` : '<i class="fas fa-user-circle"></i>'}
                    <span>${user.name || user.email}</span>
                    <i class="fas fa-chevron-down"></i>
                </button>
                <div class="user-menu-dropdown" id="userMenuDropdown">
                    <a href="/dashboard"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
                    <a href="/profile"><i class="fas fa-user"></i> Profile</a>
                    <a href="/settings"><i class="fas fa-cog"></i> Settings</a>
                    <hr>
                    <a href="#" onclick="signOut()"><i class="fas fa-sign-out-alt"></i> Sign Out</a>
                </div>
            </div>
        `;
    }
}

// Toggle user menu dropdown
function toggleUserMenu() {
    const dropdown = document.getElementById('userMenuDropdown');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.user-menu')) {
        const dropdown = document.getElementById('userMenuDropdown');
        if (dropdown) {
            dropdown.classList.remove('show');
        }
    }
});

// Export functions for global use
window.signInWithGoogle = signInWithGoogle;
window.signInWithLinkedIn = signInWithLinkedIn;
window.handleGoogleSignIn = handleGoogleSignIn;
window.signOut = signOut;
window.toggleUserMenu = toggleUserMenu;
