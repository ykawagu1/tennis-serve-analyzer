@echo off
echo ========================================
echo Creating Tennis Analyzer Project Structure
echo ========================================
echo.

echo Current directory: %CD%
echo.

echo [1] Creating backend directories...
mkdir backend 2>nul
mkdir backend\app 2>nul
mkdir backend\app\services 2>nul
mkdir backend\app\uploads 2>nul
mkdir backend\app\outputs 2>nul
echo ✅ Backend directories created

echo.
echo [2] Creating frontend directories...
mkdir frontend 2>nul
mkdir frontend\src 2>nul
mkdir frontend\public 2>nul
echo ✅ Frontend directories created

echo.
echo [3] Verifying structure...
echo Project structure:
tree /f 2>nul || (
    echo tennis-serve-analyzer/
    echo ├── backend/
    echo │   └── app/
    echo │       ├── services/
    echo │       ├── uploads/
    echo │       └── outputs/
    echo └── frontend/
    echo     ├── src/
    echo     └── public/
)

echo.
echo ========================================
echo Structure Created Successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Download the project files
echo 2. Place Python files in backend\app\ and backend\app\services\
echo 3. Place React files in frontend\ and frontend\src\
echo 4. Run setup_conda.bat
echo.
pause

