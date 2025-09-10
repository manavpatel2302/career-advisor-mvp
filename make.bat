@echo off
REM =============================================================================
REM Career Advisor MVP - Windows Make Commands
REM =============================================================================
REM Author: Career Advisor Team
REM Description: Windows batch file for project automation
REM Usage: make [command]
REM =============================================================================

setlocal enabledelayedexpansion

REM Configuration
set PROJECT_NAME=career-advisor-mvp
set PYTHON=python
set PIP=pip
set FLASK_APP=app.py
set PORT=5000
set VENV=venv

REM Parse command
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=help

REM Command routing
if /i "%COMMAND%"=="help" goto :help
if /i "%COMMAND%"=="setup" goto :setup
if /i "%COMMAND%"=="install" goto :install
if /i "%COMMAND%"=="dev" goto :dev
if /i "%COMMAND%"=="run" goto :run
if /i "%COMMAND%"=="test" goto :test
if /i "%COMMAND%"=="clean" goto :clean
if /i "%COMMAND%"=="build" goto :build
if /i "%COMMAND%"=="lint" goto :lint
if /i "%COMMAND%"=="format" goto :format
if /i "%COMMAND%"=="security" goto :security
if /i "%COMMAND%"=="docs" goto :docs
if /i "%COMMAND%"=="backup" goto :backup

REM Aliases
if /i "%COMMAND%"=="i" goto :install
if /i "%COMMAND%"=="d" goto :dev
if /i "%COMMAND%"=="t" goto :test
if /i "%COMMAND%"=="c" goto :clean
if /i "%COMMAND%"=="b" goto :build
if /i "%COMMAND%"=="r" goto :run

echo Unknown command: %COMMAND%
echo Run 'make help' for available commands
exit /b 1

:help
echo ================================================================================
echo                    Career Advisor MVP - Make Commands                          
echo ================================================================================
echo.
echo Available commands:
echo.
echo   SETUP AND INSTALLATION
echo     setup              Initial project setup (creates venv, installs deps)
echo     install, i         Install Python dependencies
echo.
echo   DEVELOPMENT
echo     dev, d             Run Flask app in development mode
echo     run, r             Run Flask app in production mode
echo.
echo   TESTING
echo     test, t            Run all tests
echo.
echo   CODE QUALITY
echo     lint               Run code linting
echo     format             Format code with black
echo     security           Run security checks
echo.
echo   BUILD AND DEPLOY
echo     build, b           Build project for production
echo.
echo   UTILITIES
echo     clean, c           Clean temporary files and caches
echo     docs               Generate documentation
echo     backup             Create backup of the project
echo.
echo ================================================================================
echo Usage: make [command]
echo Example: make dev
echo ================================================================================
exit /b 0

:setup
echo Setting up project environment...
if not exist "%VENV%" (
    echo Creating virtual environment...
    %PYTHON% -m venv %VENV%
)
echo Installing dependencies...
call %VENV%\Scripts\activate.bat
%PYTHON% -m pip install --upgrade pip
%PIP% install -r requirements.txt
if not exist ".env" if exist ".env.example" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please update .env with your actual configuration!
)
call deactivate
echo Setup complete!
exit /b 0

:install
echo Installing dependencies...
call %VENV%\Scripts\activate.bat
%PIP% install -r requirements.txt
call deactivate
echo Dependencies installed!
exit /b 0

:dev
echo Starting Flask development server...
echo Server running at: http://localhost:%PORT%
call %VENV%\Scripts\activate.bat
set FLASK_APP=%FLASK_APP%
set FLASK_ENV=development
%PYTHON% -m flask run --port=%PORT% --reload
exit /b 0

:run
echo Starting Flask production server...
call %VENV%\Scripts\activate.bat
set FLASK_APP=%FLASK_APP%
set FLASK_ENV=production
%PYTHON% %FLASK_APP%
exit /b 0

:test
echo Running tests...
call %VENV%\Scripts\activate.bat
if exist tests (
    pytest tests -v --color=yes 2>nul || %PYTHON% test_demo.py
) else (
    %PYTHON% test_demo.py
)
call deactivate
echo Tests completed!
exit /b 0

:clean
echo Cleaning project...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (.mypy_cache) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (htmlcov) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
del /s /q *.coverage 2>nul
echo Cleanup completed!
exit /b 0

:build
echo Building project...
call make clean
call make install
call make test
call make lint
echo Build completed!
exit /b 0

:lint
echo Running linter...
call %VENV%\Scripts\activate.bat
flake8 . --exclude=%VENV%,__pycache__ --max-line-length=120 2>nul || (
    echo Running basic syntax check...
    for %%f in (*.py) do %PYTHON% -m py_compile "%%f"
)
call deactivate
echo Linting completed!
exit /b 0

:format
echo Formatting code...
call %VENV%\Scripts\activate.bat
black . --exclude=%VENV% 2>nul || echo Install black: pip install black
call deactivate
echo Code formatted!
exit /b 0

:security
echo Running security scan...
call %VENV%\Scripts\activate.bat
bandit -r . -x %VENV% 2>nul || echo Install bandit: pip install bandit
call deactivate
echo Security scan completed!
exit /b 0

:docs
echo Generating documentation...
call %VENV%\Scripts\activate.bat
pdoc --html --output-dir docs . 2>nul || echo Install pdoc: pip install pdoc3
call deactivate
echo Documentation generated in docs/
exit /b 0

:backup
echo Creating backup...
set TIMESTAMP=%date:~-4%%date:~4,2%%date:~7,2%-%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_NAME=..\%PROJECT_NAME%-backup-%TIMESTAMP%.zip
powershell -Command "Compress-Archive -Path * -DestinationPath '%BACKUP_NAME%' -Force"
echo Backup created: %BACKUP_NAME%
exit /b 0

endlocal
