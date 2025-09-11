# Social Authentication Setup Guide

## Overview
This guide will help you set up Google and LinkedIn authentication for your Career Advisor MVP.

## Google Sign-In Setup

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API for your project

### 2. Configure OAuth 2.0
1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Configure the OAuth consent screen if prompted
4. Select **Web application** as the application type
5. Add your domains to **Authorized JavaScript origins**:
   - `http://localhost:5000` (for local development)
   - `https://your-domain.vercel.app` (for production)
6. Add **Authorized redirect URIs** (not needed for Google Sign-In JavaScript SDK)
7. Copy your **Client ID**

### 3. Update Your Application
1. Replace the placeholder in `static/js/social_auth.js`:
   ```javascript
   const GOOGLE_CLIENT_ID = 'YOUR_ACTUAL_GOOGLE_CLIENT_ID';
   ```

## LinkedIn Sign-In Setup

### 1. Create a LinkedIn App
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Click **Create app**
3. Fill in the required information
4. After creation, go to the **Auth** tab

### 2. Configure OAuth 2.0 Settings
1. Add **Authorized redirect URLs**:
   - `http://localhost:5000/auth/linkedin/callback` (for local development)
   - `https://your-domain.vercel.app/auth/linkedin/callback` (for production)
2. Copy your **Client ID** and **Client Secret**

### 3. Request Products
1. Go to the **Products** tab
2. Request access to **Sign In with LinkedIn using OpenID Connect**
3. Wait for approval (usually instant for Sign In)

### 4. Update Your Application
1. Replace the placeholders in `static/js/social_auth.js`:
   ```javascript
   const LINKEDIN_CLIENT_ID = 'YOUR_ACTUAL_LINKEDIN_CLIENT_ID';
   ```
2. Set environment variables in `.env`:
   ```
   LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
   ```

## Environment Variables

Create a `.env` file in your project root with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_SECRET_KEY=your-flask-secret-key

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id

# LinkedIn OAuth
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret

# JWT Configuration
JWT_SECRET=your-jwt-secret-key

# Existing Gemini AI
GEMINI_API_KEY=your-gemini-api-key
```

## Deployment to Vercel

### 1. Add Environment Variables
1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add all the environment variables from your `.env` file

### 2. Update vercel.json
Ensure your `vercel.json` includes the social auth routes:

```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/auth/(.*)",
      "dest": "/app.py"
    },
    {
      "src": "/(.*)",
      "dest": "/app.py"
    }
  ]
}
```

## Testing Social Authentication

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Navigate to `http://localhost:5000`

4. Click "Sign In" and test both Google and LinkedIn authentication

### Production Testing
1. Deploy to Vercel:
   ```bash
   vercel --prod
   ```

2. Test authentication on your live URL

## Security Considerations

1. **Never commit credentials**: Always use environment variables
2. **Use HTTPS in production**: OAuth requires secure connections
3. **Validate tokens server-side**: Always verify tokens on your backend
4. **Implement rate limiting**: Protect against abuse
5. **Log authentication attempts**: Monitor for suspicious activity

## Troubleshooting

### Google Sign-In Issues
- **Error: "popup_closed_by_user"**: User closed the popup window
- **Error: "invalid_client"**: Check your Client ID
- **One Tap not showing**: Check browser settings and third-party cookies

### LinkedIn Sign-In Issues
- **Error: "invalid_request"**: Check redirect URI configuration
- **Error: "access_denied"**: User denied permission
- **Popup blocked**: Enable popups for your domain

### General Issues
- **CORS errors**: Check CORS configuration in Flask
- **Session not persisting**: Check cookie settings and domain configuration
- **User data not saving**: Check database connection and schema

## Features Implemented

✅ Google Sign-In with One Tap
✅ LinkedIn OAuth authentication
✅ Session management
✅ User profile display
✅ Automatic redirection after login
✅ Sign out functionality
✅ Remember me option
✅ Social login buttons in modals
✅ User menu dropdown
✅ Toast notifications
✅ Loading states
✅ Error handling

## Next Steps

1. **Database Integration**: Replace the mock database with your actual database
2. **Profile Completion**: Add a profile completion flow for social login users
3. **Email Verification**: Add email verification for non-social registrations
4. **Two-Factor Authentication**: Enhance security with 2FA
5. **Account Linking**: Allow users to link multiple social accounts

## Support

For issues or questions:
1. Check the browser console for errors
2. Review server logs
3. Verify all environment variables are set correctly
4. Ensure all URLs are properly configured in OAuth providers

## License

This implementation is part of the Career Advisor MVP project.
