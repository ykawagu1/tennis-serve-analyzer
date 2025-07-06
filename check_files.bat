@echo off
echo ========================================
echo Tennis Analyzer - File Placement Check
echo ========================================
echo.

echo Current directory: %CD%
echo.

REM カウンター初期化
set BACKEND_COUNT=0
set FRONTEND_COUNT=0
set SETUP_COUNT=0

echo [1] Checking backend files...
echo ----------------------------------------
if exist "backend\app\main.py" (
    echo ✅ backend\app\main.py found
    set /a BACKEND_COUNT+=1
) else (
    echo ❌ backend\app\main.py NOT found
)

if exist "backend\app\services\pose_detector.py" (
    echo ✅ backend\app\services\pose_detector.py found
    set /a BACKEND_COUNT+=1
) else (
    echo ❌ backend\app\services\pose_detector.py NOT found
)

if exist "backend\app\services\motion_analyzer.py" (
    echo ✅ backend\app\services\motion_analyzer.py found
    set /a BACKEND_COUNT+=1
) else (
    echo ❌ backend\app\services\motion_analyzer.py NOT found
)

if exist "backend\app\services\video_processor.py" (
    echo ✅ backend\app\services\video_processor.py found
    set /a BACKEND_COUNT+=1
) else (
    echo ❌ backend\app\services\video_processor.py NOT found
)

if exist "backend\app\services\advice_generator.py" (
    echo ✅ backend\app\services\advice_generator.py found
    set /a BACKEND_COUNT+=1
) else (
    echo ❌ backend\app\services\advice_generator.py NOT found
)

echo Backend files: %BACKEND_COUNT%/5
echo.

echo [2] Checking frontend files...
echo ----------------------------------------
if exist "frontend\package.json" (
    echo ✅ frontend\package.json found
    set /a FRONTEND_COUNT+=1
) else (
    echo ❌ frontend\package.json NOT found
)

if exist "frontend\src\App.jsx" (
    echo ✅ frontend\src\App.jsx found
    set /a FRONTEND_COUNT+=1
) else (
    echo ❌ frontend\src\App.jsx NOT found
)

echo Frontend files: %FRONTEND_COUNT%/2
echo.

echo [3] Checking setup files...
echo ----------------------------------------
if exist "setup_conda.bat" (
    echo ✅ setup_conda.bat found
    set /a SETUP_COUNT+=1
) else (
    echo ❌ setup_conda.bat NOT found
)

if exist "start_conda.bat" (
    echo ✅ start_conda.bat found
    set /a SETUP_COUNT+=1
) else (
    echo ❌ start_conda.bat NOT found
)

if exist "test_conda.py" (
    echo ✅ test_conda.py found
    set /a SETUP_COUNT+=1
) else (
    echo ❌ test_conda.py NOT found
)

echo Setup files: %SETUP_COUNT%/3
echo.

echo [4] Checking directory structure...
echo ----------------------------------------
if exist "backend" (
    echo ✅ backend directory exists
) else (
    echo ❌ backend directory missing
)

if exist "backend\app" (
    echo ✅ backend\app directory exists
) else (
    echo ❌ backend\app directory missing
)

if exist "backend\app\services" (
    echo ✅ backend\app\services directory exists
) else (
    echo ❌ backend\app\services directory missing
)

if exist "frontend" (
    echo ✅ frontend directory exists
) else (
    echo ❌ frontend directory missing
)

if exist "frontend\src" (
    echo ✅ frontend\src directory exists
) else (
    echo ❌ frontend\src directory missing
)

echo.
echo ========================================
echo SUMMARY
echo ========================================

REM 総合判定
set /a TOTAL_FOUND=%BACKEND_COUNT%+%FRONTEND_COUNT%+%SETUP_COUNT%
set TOTAL_REQUIRED=10

echo Backend files: %BACKEND_COUNT%/5
echo Frontend files: %FRONTEND_COUNT%/2
echo Setup files: %SETUP_COUNT%/3
echo Total: %TOTAL_FOUND%/%TOTAL_REQUIRED%
echo.

if %BACKEND_COUNT%==5 if %FRONTEND_COUNT%==2 if %SETUP_COUNT%==3 (
    echo 🎉 ALL FILES FOUND! Ready to proceed!
    echo.
    echo Next steps:
    echo 1. Run setup_conda.bat to setup environment
    echo 2. Run test_conda.py to verify installation
    echo 3. Run start_conda.bat to start the system
) else (
    echo ⚠️ SOME FILES ARE MISSING
    echo.
    echo What to do:
    if %BACKEND_COUNT% LSS 5 (
        echo - Download backend Python files
        echo - Place them in backend\app\ and backend\app\services\
    )
    if %FRONTEND_COUNT% LSS 2 (
        echo - Download frontend files
        echo - Place them in frontend\ and frontend\src\
    )
    if %SETUP_COUNT% LSS 3 (
        echo - Download setup files
        echo - Place them in the root directory
    )
    echo.
    echo Missing files need to be downloaded and placed correctly.
)

echo.
echo ========================================
echo CURRENT DIRECTORY CONTENTS
echo ========================================
dir /b
echo.

echo ========================================
echo HELP
echo ========================================
echo If files are missing:
echo 1. Make sure you downloaded all project files
echo 2. Check your Downloads folder
echo 3. Copy files to the correct locations
echo 4. Run this check again
echo.
echo Current location: %CD%
echo.
pause

