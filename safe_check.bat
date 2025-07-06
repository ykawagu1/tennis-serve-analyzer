@echo off
echo ========================================
echo SAFE Tennis Server Checker
echo ========================================
echo This is a lightweight, safe version
echo.

echo [SAFE CHECK 1] Current location
echo %CD%
echo.

echo [SAFE CHECK 2] Python availability
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python not found - trying 'py' command
    py --version 2>nul
    if %errorlevel% neq 0 (
        echo ERROR: Python not installed
        echo Please install Python from: https://www.python.org/downloads/
        echo.
        echo Press any key to exit safely...
        pause >nul
        exit /b 1
    ) else (
        echo OK: Python found (py command)
    )
) else (
    echo OK: Python found (python command)
)
echo.

echo [SAFE CHECK 3] Project files
if exist "backend\app\main.py" (
    echo OK: Backend files found
) else (
    echo ERROR: Backend files not found
    echo You may need to download the project files
)

if exist "frontend\package.json" (
    echo OK: Frontend files found
) else (
    echo ERROR: Frontend files not found
    echo You may need to download the project files
)
echo.

echo [SAFE CHECK 4] Node.js availability
node --version 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found
    echo Please install Node.js from: https://nodejs.org/
) else (
    echo OK: Node.js found
)
echo.

echo ========================================
echo SAFETY RECOMMENDATIONS
echo ========================================
echo 1. If all checks show OK, you can proceed
echo 2. If errors found, fix them first
echo 3. Do NOT run heavy installation scripts
echo 4. Install packages one by one manually
echo.
echo Manual installation commands:
echo   pip install flask
echo   pip install mediapipe
echo   pip install opencv-python
echo.
echo Press any key to exit...
pause >nul

