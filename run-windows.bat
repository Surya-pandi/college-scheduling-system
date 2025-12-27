@echo off
echo College Management System - Starting...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -q -r requirements.txt

REM Initialize database and admin
echo.
echo Setting up database and admin account (if needed)...
python setup_admin.py

REM Start the application
echo.
echo Starting application...
echo Opening http://localhost:5000 in your browser...
timeout /t 2 /nobreak
python app.py
