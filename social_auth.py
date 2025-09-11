"""
Social Authentication Routes
Handles Google and LinkedIn OAuth integration
"""

from flask import Blueprint, request, jsonify, session, redirect, url_for
import os
import json
import requests
from datetime import datetime, timedelta
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Create blueprint
social_auth_bp = Blueprint('social_auth', __name__)

# Configuration - These should be in environment variables
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '973526458923-your-google-client-id.apps.googleusercontent.com')
LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID', 'your-linkedin-client-id')
LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET', 'your-linkedin-client-secret')
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-jwt-secret-key')

# Mock database - Replace with your actual database
users_db = {}

def generate_user_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

@social_auth_bp.route('/auth/google', methods=['POST'])
def google_auth():
    """Handle Google Sign-In"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        # Verify the Google ID token
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            # Token is valid, extract user info
            google_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            picture = idinfo.get('picture', '')
            
            # Check if user exists
            user = users_db.get(f'google_{google_id}')
            is_new_user = False
            
            if not user:
                # Create new user
                is_new_user = True
                user = {
                    'id': f'google_{google_id}',
                    'email': email,
                    'name': name,
                    'picture': picture,
                    'auth_method': 'google',
                    'created_at': datetime.utcnow().isoformat(),
                    'profile_complete': False
                }
                users_db[f'google_{google_id}'] = user
            else:
                # Update existing user info
                user['last_login'] = datetime.utcnow().isoformat()
                user['picture'] = picture  # Update picture in case it changed
            
            # Generate session token
            session_token = generate_user_token(user['id'])
            session['user_id'] = user['id']
            session['auth_token'] = session_token
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'picture': user['picture']
                },
                'token': session_token,
                'isNewUser': is_new_user
            })
            
        except ValueError as e:
            # Invalid token
            return jsonify({
                'success': False,
                'message': 'Invalid Google token'
            }), 401
            
    except Exception as e:
        print(f"Google auth error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Authentication failed'
        }), 500

@social_auth_bp.route('/auth/linkedin', methods=['POST'])
def linkedin_auth():
    """Handle LinkedIn Sign-In"""
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        linkedin_id = data.get('linkedin_id')
        picture = data.get('picture')
        
        # Check if user exists
        user = users_db.get(f'linkedin_{linkedin_id}')
        is_new_user = False
        
        if not user:
            # Create new user
            is_new_user = True
            user = {
                'id': f'linkedin_{linkedin_id}',
                'email': email,
                'name': name,
                'picture': picture,
                'auth_method': 'linkedin',
                'created_at': datetime.utcnow().isoformat(),
                'profile_complete': False
            }
            users_db[f'linkedin_{linkedin_id}'] = user
        else:
            # Update existing user info
            user['last_login'] = datetime.utcnow().isoformat()
            user['picture'] = picture  # Update picture in case it changed
        
        # Generate session token
        session_token = generate_user_token(user['id'])
        session['user_id'] = user['id']
        session['auth_token'] = session_token
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'picture': user['picture']
            },
            'token': session_token,
            'isNewUser': is_new_user
        })
        
    except Exception as e:
        print(f"LinkedIn auth error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Authentication failed'
        }), 500

@social_auth_bp.route('/auth/linkedin/exchange', methods=['POST'])
def linkedin_exchange_code():
    """Exchange LinkedIn authorization code for access token"""
    try:
        data = request.get_json()
        code = data.get('code')
        
        # Exchange code for access token
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': LINKEDIN_CLIENT_ID,
            'client_secret': LINKEDIN_CLIENT_SECRET,
            'redirect_uri': request.host_url + 'auth/linkedin/callback'
        }
        
        token_response = requests.post(token_url, data=token_data)
        
        if token_response.status_code != 200:
            return jsonify({
                'success': False,
                'message': 'Failed to exchange code for token'
            }), 400
        
        access_token = token_response.json().get('access_token')
        
        # Get user profile
        profile_url = 'https://api.linkedin.com/v2/me'
        profile_headers = {
            'Authorization': f'Bearer {access_token}'
        }
        profile_response = requests.get(profile_url, headers=profile_headers)
        
        if profile_response.status_code != 200:
            return jsonify({
                'success': False,
                'message': 'Failed to get user profile'
            }), 400
        
        profile_data = profile_response.json()
        
        # Get email address
        email_url = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'
        email_response = requests.get(email_url, headers=profile_headers)
        
        email = ''
        if email_response.status_code == 200:
            email_data = email_response.json()
            if email_data.get('elements'):
                email = email_data['elements'][0]['handle~']['emailAddress']
        
        # Extract user info
        first_name = profile_data.get('localizedFirstName', '')
        last_name = profile_data.get('localizedLastName', '')
        linkedin_id = profile_data.get('id', '')
        
        # Get profile picture
        picture = ''
        picture_url = 'https://api.linkedin.com/v2/me?projection=(profilePicture(displayImage~:playableStreams))'
        picture_response = requests.get(picture_url, headers=profile_headers)
        
        if picture_response.status_code == 200:
            picture_data = picture_response.json()
            if picture_data.get('profilePicture'):
                display_image = picture_data['profilePicture'].get('displayImage~')
                if display_image and display_image.get('elements'):
                    # Get the largest image
                    picture = display_image['elements'][-1]['identifiers'][0]['identifier']
        
        user_data = {
            'id': linkedin_id,
            'email': email,
            'name': f'{first_name} {last_name}',
            'picture': picture
        }
        
        return jsonify({
            'success': True,
            'user': user_data
        })
        
    except Exception as e:
        print(f"LinkedIn exchange error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to exchange code'
        }), 500

@social_auth_bp.route('/auth/linkedin/callback')
def linkedin_callback():
    """LinkedIn OAuth callback"""
    # This route handles the redirect from LinkedIn
    # In a real app, you'd process the code here and redirect to your app
    return """
    <html>
        <body>
            <script>
                // Close the popup window
                window.close();
            </script>
        </body>
    </html>
    """

@social_auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@social_auth_bp.route('/auth/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    user_id = session.get('user_id')
    if user_id:
        user = users_db.get(user_id)
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'picture': user.get('picture', '')
                }
            })
    
    return jsonify({
        'authenticated': False
    })
