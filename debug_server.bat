@echo off
echo ========================================
echo Tennis Server Debug Tool
echo ========================================
echo.

echo [1] Checking current directory...
echo Current directory: %CD%
echo.

echo [2] Checking for project files...
if exist "backend\app\main.py" (
    echo [OK] main.py found
) else (
    echo [ERROR] main.py NOT found
    echo You need to be in the tennis-serve-analyzer folder
    echo.
    echo Searching for tennis-serve-analyzer folder...
    for /d %%i in ("%USERPROFILE%\Desktop\tennis*") do (
        echo Found: %%i
    )
    echo.
    echo Please navigate to the correct folder and try again
    pause
    exit /b 1
)

echo [3] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found, trying 'py' command...
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python not installed or not in PATH
        echo Please install Python from: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        echo [OK] Python found (using 'py' command)
        set PYTHON_CMD=py
    )
) else (
    echo [OK] Python found (using 'python' command)
    set PYTHON_CMD=python
)

echo [4] Installing required packages...
echo Installing Flask...
%PYTHON_CMD% -m pip install flask flask-cors
echo Installing MediaPipe...
%PYTHON_CMD% -m pip install mediapipe opencv-python
echo Installing other dependencies...
%PYTHON_CMD% -m pip install openai python-dotenv requests

echo [5] Starting server...
echo Changing to backend directory...
cd backend\app

echo Starting Python server...
echo If successful, you should see: "Running on http://127.0.0.1:5000"
echo.
%PYTHON_CMD% main.py

pause

