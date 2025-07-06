@echo off
chcp 65001 >nul
echo ========================================
echo Node.js Environment Check
echo ========================================
echo.

echo [Check 1] Node.js Installation
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js: Not installed
    echo Download from: https://nodejs.org/ja/
) else (
    echo ✅ Node.js: Installed
    node --version
)

echo.
echo [Check 2] npm Installation
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm: Not available
) else (
    echo ✅ npm: Available
    npm --version
)

echo.
echo [Check 3] Project Structure
if exist "frontend" (
    echo ✅ Frontend directory: Found
    if exist "frontend\package.json" (
        echo ✅ package.json: Found
    ) else (
        echo ❌ package.json: Missing
    )
    if exist "frontend\src" (
        echo ✅ src directory: Found
    ) else (
        echo ❌ src directory: Missing
    )
    if exist "frontend\src\App.jsx" (
        echo ✅ App.jsx: Found
    ) else (
        echo ❌ App.jsx: Missing
    )
) else (
    echo ❌ Frontend directory: Not found
)

echo.
echo [Check 4] Dependencies
if exist "frontend\node_modules" (
    echo ✅ node_modules: Installed
) else (
    echo ❌ node_modules: Not installed
    echo Run: npm install
)

echo.
echo [Check 5] PATH Environment
echo Current PATH includes:
echo %PATH% | findstr /i node
if errorlevel 1 (
    echo ❌ Node.js not found in PATH
) else (
    echo ✅ Node.js found in PATH
)

echo.
echo ========================================
echo Recommendations
echo ========================================

node --version >nul 2>&1
if errorlevel 1 (
    echo 1. Install Node.js from https://nodejs.org/ja/
    echo 2. Choose LTS version
    echo 3. Make sure "Add to PATH" is checked
    echo 4. Restart command prompt
)

if not exist "frontend\node_modules" (
    echo 5. Run: cd frontend
    echo 6. Run: npm install
)

echo.
pause

