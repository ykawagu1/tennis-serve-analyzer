@echo off
echo Creating complete tennis-serve-analyzer project...
echo.

REM Create main project directory
if not exist "tennis-serve-analyzer" mkdir tennis-serve-analyzer
cd tennis-serve-analyzer

REM Create backend structure
mkdir backend\app\services 2>nul
mkdir backend\app\uploads 2>nul
mkdir backend\app\outputs 2>nul

REM Create frontend structure  
mkdir frontend\src 2>nul
mkdir frontend\public 2>nul

echo Project structure created successfully!
echo.
echo Please copy all the provided files to this folder:
echo %CD%
echo.
echo Required files:
echo - backend\app\main.py
echo - backend\app\services\*.py
echo - frontend\package.json
echo - frontend\src\*.jsx
echo - start_system.bat
echo - start_frontend.bat
echo - setup.sh
echo - README.md
echo.
echo After copying files, run:
echo 1. setup.sh (to install dependencies)
echo 2. start_system.bat (to start backend)
echo 3. start_frontend.bat (to start frontend)
echo.
pause

