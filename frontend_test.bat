@echo off
chcp 65001 >nul
echo ========================================
echo Frontend Functionality Test
echo ========================================
echo.

echo [Step 1] Checking Node.js environment...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found
    echo Please install Node.js first
    pause
    exit /b 1
)

echo ✅ Node.js: 
node --version
echo ✅ npm: 
npm --version

echo.
echo [Step 2] Checking project structure...
if not exist "frontend" (
    echo ❌ Frontend directory not found
    echo Please make sure you are in the tennis-serve-analyzer directory
    pause
    exit /b 1
)

cd frontend

if not exist "package.json" (
    echo ❌ package.json not found
    pause
    exit /b 1
)

echo ✅ Frontend directory and package.json found

echo.
echo [Step 3] Checking dependencies...
if exist "node_modules" (
    echo ✅ Dependencies already installed
) else (
    echo ⚠️ Dependencies not installed, installing now...
    npm install
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed successfully
)

echo.
echo [Step 4] Running build test...
echo Building project...
npm run build >nul 2>&1
if errorlevel 1 (
    echo ❌ Build failed
    echo Running detailed build...
    npm run build
    pause
    exit /b 1
) else (
    echo ✅ Build successful
)

echo.
echo [Step 5] Testing development server...
echo.
echo ========================================
echo Frontend Test Results
echo ========================================
echo ✅ Node.js environment: OK
echo ✅ Project structure: OK
echo ✅ Dependencies: OK
echo ✅ Build process: OK
echo.
echo Starting development server...
echo.
echo Open your browser and go to:
echo http://localhost:5173
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

npm run dev -- --host

