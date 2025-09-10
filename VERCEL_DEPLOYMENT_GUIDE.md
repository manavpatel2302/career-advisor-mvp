# 🚀 Vercel Deployment Guide for Career Advisor MVP

## ✅ Pre-Deployment Checklist

Your project is now **100% ready** for Vercel deployment! Here's what's been configured:

- ✅ `vercel.json` - Deployment configuration
- ✅ `api/index.py` - Serverless function handler
- ✅ `requirements.txt` - Python dependencies
- ✅ Static files structure
- ✅ Environment variables template

## 📋 Step-by-Step Deployment Instructions

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

Or if you don't have npm, download from: https://vercel.com/download

### Step 2: Create Vercel Account

1. Go to https://vercel.com/signup
2. Sign up with GitHub, GitLab, or Email
3. Verify your email

### Step 3: Deploy Your Application

#### Option A: Quick Deploy (Recommended)

Run the deployment script:
```bash
deploy-vercel.bat
```

#### Option B: Manual Deploy

```bash
# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Step 4: Configure Environment Variables

**IMPORTANT:** You must set these environment variables in Vercel for the app to work properly.

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Navigate to **Settings** → **Environment Variables**
4. Add these variables:

| Variable Name | Description | Example Value |
|--------------|-------------|---------------|
| `GEMINI_API_KEY` | Your Google Gemini API key | `AIza...` |
| `SECRET_KEY` | Flask session secret key | `your-very-secret-key-change-this` |
| `FLASK_ENV` | Flask environment | `production` |

#### How to get a Gemini API Key:
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key and add it to Vercel

### Step 5: Custom Domain (Optional)

1. In Vercel Dashboard → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

## 🔗 Your Deployment URLs

After deployment, you'll get:

- **Production URL**: `https://your-project.vercel.app`
- **Preview URLs**: `https://your-project-git-branch.vercel.app`
- **Custom Domain**: `https://yourdomain.com` (if configured)

## 📁 Project Structure for Vercel

```
career-advisor-mvp/
├── api/
│   └── index.py          # Serverless function entry point
├── static/               # Static assets (CSS, JS)
│   ├── css/
│   └── js/
├── templates/            # HTML templates
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
└── .env.vercel.example # Environment variables template
```

## 🛠️ Common Deployment Commands

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# List all deployments
vercel list

# View logs
vercel logs

# Remove deployment
vercel remove [deployment-url]

# Pull environment variables
vercel env pull

# Add environment variable
vercel env add VARIABLE_NAME
```

## 🐛 Troubleshooting

### Issue: "Module not found" Error
**Solution**: Ensure all imports are in `requirements.txt`

### Issue: "Template not found" Error
**Solution**: Check `vercel.json` includes templates:
```json
"functions": {
  "api/index.py": {
    "includeFiles": "templates/**"
  }
}
```

### Issue: API Key not working
**Solution**: 
1. Check environment variables in Vercel dashboard
2. Ensure no spaces in the API key
3. Verify the key is active in Google Cloud Console

### Issue: Static files not loading
**Solution**: Verify static files path in `vercel.json`:
```json
{
  "src": "/static/(.*)",
  "dest": "/static/$1"
}
```

## 🔄 Updating Your Deployment

### Method 1: Automatic (with Git)
```bash
git add .
git commit -m "Update message"
git push
# Vercel auto-deploys from GitHub
```

### Method 2: Manual
```bash
vercel --prod
```

## 📊 Monitoring Your App

1. **Vercel Dashboard**: https://vercel.com/dashboard
   - View deployments
   - Check function logs
   - Monitor usage

2. **Analytics**: Enable in Vercel Dashboard → Analytics

3. **Error Tracking**: View in Functions → Logs

## 🎯 Post-Deployment Checklist

- [ ] Test the live URL
- [ ] Verify API integration works
- [ ] Check all pages load correctly
- [ ] Test on mobile devices
- [ ] Set up custom domain (optional)
- [ ] Enable analytics
- [ ] Set up error notifications

## 💡 Pro Tips

1. **Preview Deployments**: Every git branch gets its own preview URL
2. **Rollback**: Easy one-click rollback to previous versions
3. **Environment Variables**: Use different values for production/development
4. **Custom Headers**: Add security headers in `vercel.json`
5. **Caching**: Configure caching for better performance

## 🔒 Security Best Practices

1. **Never commit** `.env` files
2. **Use strong** SECRET_KEY values
3. **Enable** HTTPS (automatic on Vercel)
4. **Set up** rate limiting for API routes
5. **Monitor** function logs for suspicious activity

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Python on Vercel](https://vercel.com/docs/runtimes/python)
- [Environment Variables Guide](https://vercel.com/docs/environment-variables)
- [Custom Domains](https://vercel.com/docs/custom-domains)

## 🆘 Need Help?

- Check Vercel Status: https://www.vercel-status.com/
- Vercel Support: https://vercel.com/support
- Community Forum: https://github.com/vercel/vercel/discussions

---

## 🎉 Quick Start Command

Just run this single command to deploy:

```bash
npx vercel
```

Follow the prompts, and your app will be live in minutes!

---

**Your app is now ready for Vercel deployment! 🚀**
