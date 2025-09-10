@echo off
REM Quick Save Script for Career Advisor MVP
REM Usage: Just double-click or run: save.bat

echo ================================================================================
echo                     SAVING YOUR PROJECT TO GIT                                
echo ================================================================================
echo.

REM Check if we're in a git repository
git status >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not a Git repository!
    echo Please run 'git init' first.
    pause
    exit /b 1
)

REM Show current status
echo Current changes:
echo --------------------------------------------------------------------------------
git status --short
echo --------------------------------------------------------------------------------
echo.

REM Add all changes
echo Adding all changes...
git add -A

REM Create commit with timestamp
set TIMESTAMP=%date:~-4%-%date:~4,2%-%date:~7,2% %time:~0,2%:%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%

REM Ask for commit message or use default
set /p COMMIT_MSG="Enter commit message (or press Enter for auto-message): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Save: %TIMESTAMP%

REM Commit changes
echo.
echo Committing changes...
git commit -m "%COMMIT_MSG%"

REM Check if remote exists
git remote -v | find "origin" >nul 2>&1
if errorlevel 1 (
    echo.
    echo --------------------------------------------------------------------------------
    echo NOTE: No remote repository configured yet.
    echo To push to GitHub, first create a repository on GitHub, then run:
    echo   git remote add origin https://github.com/YOUR_USERNAME/career-advisor-mvp.git
    echo   git push -u origin main
    echo --------------------------------------------------------------------------------
) else (
    echo.
    echo Pushing to GitHub...
    git push
    echo.
    echo ================================================================================
    echo                     PROJECT SAVED SUCCESSFULLY!                               
    echo ================================================================================
    echo.
    echo Your changes have been:
    echo   - Committed locally
    echo   - Pushed to GitHub
)

echo.
echo Press any key to close...
pause >nul
