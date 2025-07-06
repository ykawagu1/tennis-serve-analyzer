@echo off
chcp 65001 >nul
echo ========================================
echo Tennis Serve Analyzer - Conda Start
echo ========================================
echo.

echo [Step 1] Activating conda environment...
call conda activate tennis-analyzer
if errorlevel 1 (
    echo ERROR: Failed to activate tennis-analyzer environment
    echo Please run 'setup_conda.bat' first
    pause
    exit /b 1
)

echo Environment activated successfully!
echo.

echo [Step 2] Checking Python version...
python --version

echo.
echo [Step 3] Starting backend server...
echo Navigate to backend directory and start server...
cd backend\app

echo Starting Flask server...
echo Server will run on http://127.0.0.1:5000
echo.
echo ========================================
echo Backend Server Starting...
echo ========================================
echo Press Ctrl+C to stop the server
echo.

python main.py

