@echo off
chcp 65001 >nul
echo Checking system status...
echo.

echo ========================================
echo Python Check
echo ========================================
python --version 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    echo Please install Python: https://www.python.org/downloads/
) else (
    echo [OK] Python is available
)
echo.

echo ========================================
echo Node.js Check
echo ========================================
node --version 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found
    echo Please install Node.js: https://nodejs.org/
) else (
    echo [OK] Node.js is available
)
echo.

echo ========================================
echo Port Usage Check
echo ========================================
echo Port 5000 (Backend):
netstat -an | findstr :5000
if %errorlevel% neq 0 (
    echo [ERROR] Port 5000 not in use (Backend server not running)
) else (
    echo [OK] Port 5000 is in use (Backend server running)
)

echo.
echo Port 5173 (Frontend):
netstat -an | findstr :5173
if %errorlevel% neq 0 (
    echo [ERROR] Port 5173 not in use (Frontend server not running)
) else (
    echo [OK] Port 5173 is in use (Frontend server running)
)
echo.

echo ========================================
echo Process Check
echo ========================================
echo Python processes:
tasklist | findstr python
echo.
echo Node processes:
tasklist | findstr node
echo.

echo ========================================
echo File Check
echo ========================================
if exist "backend\app\main.py" (
    echo [OK] Backend files exist
) else (
    echo [ERROR] Backend files not found
)

if exist "frontend\package.json" (
    echo [OK] Frontend files exist
) else (
    echo [ERROR] Frontend files not found
)

if exist "frontend\node_modules" (
    echo [OK] Frontend dependencies installed
) else (
    echo [ERROR] Frontend dependencies not installed
    echo Run 'npm install' in frontend folder
)
echo.

echo ========================================
echo Recommended Actions
echo ========================================
echo 1. If both servers are not running:
echo    - Run start_system.bat
echo    - Run start_frontend.bat
echo.
echo 2. If ports are in use:
echo    - Close other applications
echo    - Restart computer
echo.
echo 3. If dependencies are missing:
echo    - Run setup.bat
echo.

pause

