@echo off
REM Quick start script for Document Q&A Chatbot
REM This script checks setup and runs the Streamlit app

echo ========================================
echo Document Q&A Chatbot - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Checking setup...
echo.

REM Run setup check
python setup_check.py

echo.
echo ========================================
echo.

REM Ask if user wants to continue
set /p continue="Start the application? (Y/N): "
if /i "%continue%" neq "Y" (
    echo Exiting...
    exit /b 0
)

echo.
echo Starting Streamlit app...
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Run Streamlit
streamlit run src/ui/streamlit_app.py

pause
