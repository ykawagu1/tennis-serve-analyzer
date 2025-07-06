@echo off
chcp 65001 >nul
echo ========================================
echo Node.js Setup for Tennis Analyzer
echo ========================================
echo.

echo [Step 1] Checking if Node.js is installed...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed.
    echo.
    echo Please follow these steps:
    echo 1. Go to https://nodejs.org/ja/
    echo 2. Download LTS version (recommended)
    echo 3. Run the installer
    echo 4. Make sure "Add to PATH" is checked
    echo 5. Restart command prompt
    echo 6. Run this script again
    echo.
    echo Opening Node.js download page...
    start https://nodejs.org/ja/
    pause
    exit /b 1
)

echo ✅ Node.js is installed!
echo Node.js version:
node --version
echo npm version:
npm --version

echo.
echo [Step 2] Checking project structure...
if not exist "frontend" (
    echo ❌ Frontend directory not found
    echo Please make sure you are in the tennis-serve-analyzer directory
    pause
    exit /b 1
)

echo ✅ Frontend directory found

echo.
echo [Step 3] Installing frontend dependencies...
cd frontend

if not exist "package.json" (
    echo ❌ package.json not found
    echo Please make sure all frontend files are properly placed
    pause
    exit /b 1
)

echo Installing npm packages...
npm install

if errorlevel 1 (
    echo ⚠️ Installation failed, trying to fix...
    echo Cleaning npm cache...
    npm cache clean --force
    echo Retrying installation...
    npm install
    
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        echo.
        echo Troubleshooting steps:
        echo 1. Check internet connection
        echo 2. Run as administrator
        echo 3. Try: npm install --legacy-peer-deps
        pause
        exit /b 1
    )
)

echo ✅ Dependencies installed successfully!

echo.
echo [Step 4] Testing frontend server...
echo.
echo ========================================
echo Frontend Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: run start_conda.bat
echo 2. Start frontend: npm run dev -- --host
echo 3. Open browser: http://localhost:5173
echo.
echo Starting development server now...
echo Press Ctrl+C to stop the server
echo.

npm run dev -- --host

