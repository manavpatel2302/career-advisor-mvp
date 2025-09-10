@echo off
echo ========================================
echo   Career Advisor MVP - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/Updating dependencies...
pip install -r requirements.txt > nul 2>&1

echo.
echo Initializing database...
python database\init_db.py

echo.
echo ========================================
echo   Starting Flask application...
echo ========================================
echo.
echo The application will be available at:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py
