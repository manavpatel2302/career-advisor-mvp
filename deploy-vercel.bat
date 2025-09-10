@echo off
REM =============================================================================
REM Vercel Deployment Script for Career Advisor MVP
REM =============================================================================

echo ================================================================================
echo                    DEPLOYING TO VERCEL                                        
echo ================================================================================
echo.

REM Check if Vercel CLI is installed
where vercel >nul 2>&1
if errorlevel 1 (
    echo Vercel CLI not found. Installing...
    npm install -g vercel
)

REM Check if logged in to Vercel
echo Checking Vercel authentication...
vercel whoami >nul 2>&1
if errorlevel 1 (
    echo Please login to Vercel:
    vercel login
)

echo.
echo Deployment Options:
echo 1. Deploy to Production
echo 2. Deploy to Preview
echo 3. Setup Environment Variables
echo 4. View Deployment Status
echo.

set /p CHOICE="Enter your choice (1-4): "

if "%CHOICE%"=="1" goto :deploy_prod
if "%CHOICE%"=="2" goto :deploy_preview
if "%CHOICE%"=="3" goto :setup_env
if "%CHOICE%"=="4" goto :status

echo Invalid choice!
pause
exit /b 1

:deploy_prod
echo.
echo Deploying to Production...
vercel --prod
echo.
echo ================================================================================
echo Production deployment complete!
echo Your app should be live at your Vercel URL
echo ================================================================================
pause
exit /b 0

:deploy_preview
echo.
echo Deploying to Preview...
vercel
echo.
echo ================================================================================
echo Preview deployment complete!
echo Check the URL above to view your preview deployment
echo ================================================================================
pause
exit /b 0

:setup_env
echo.
echo ================================================================================
echo ENVIRONMENT VARIABLES SETUP
echo ================================================================================
echo.
echo You need to set the following environment variables in Vercel:
echo.
echo 1. GEMINI_API_KEY - Your Google Gemini API key
echo 2. SECRET_KEY - A secure secret key for Flask sessions
echo 3. FLASK_ENV - Set to 'production'
echo.
echo To set these:
echo 1. Go to your Vercel dashboard
echo 2. Select your project
echo 3. Go to Settings -^> Environment Variables
echo 4. Add each variable listed above
echo.
echo Press any key to open Vercel dashboard...
pause >nul
start https://vercel.com/dashboard
exit /b 0

:status
echo.
echo Checking deployment status...
vercel list
echo.
pause
exit /b 0
