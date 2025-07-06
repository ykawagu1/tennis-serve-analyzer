@echo off
chcp 65001 >nul
echo ========================================
echo Tennis Serve Analyzer - Anaconda Setup
echo ========================================
echo.

echo [Step 1] Creating Python 3.11 environment...
call conda create -n tennis-analyzer python=3.11 -y
if errorlevel 1 (
    echo ERROR: Failed to create conda environment
    pause
    exit /b 1
)

echo.
echo [Step 2] Activating environment...
call conda activate tennis-analyzer
if errorlevel 1 (
    echo ERROR: Failed to activate environment
    pause
    exit /b 1
)

echo.
echo [Step 3] Installing basic packages with conda...
call conda install -c conda-forge numpy opencv flask -y
if errorlevel 1 (
    echo WARNING: Some conda packages failed to install
)

echo.
echo [Step 4] Installing MediaPipe and other packages with pip...
call pip install mediapipe
call pip install flask-cors
call pip install openai
call pip install protobuf==3.20.3

echo.
echo [Step 5] Verifying installation...
python -c "
import sys
print(f'Python version: {sys.version}')
print('Testing imports...')

try:
    import mediapipe as mp
    print('✓ MediaPipe: OK')
except ImportError as e:
    print(f'✗ MediaPipe: {e}')

try:
    import cv2
    print('✓ OpenCV: OK')
except ImportError as e:
    print(f'✗ OpenCV: {e}')

try:
    import flask
    print('✓ Flask: OK')
except ImportError as e:
    print(f'✗ Flask: {e}')

try:
    import numpy as np
    print('✓ NumPy: OK')
except ImportError as e:
    print(f'✗ NumPy: {e}')
"

echo.
echo ========================================
echo Setup completed!
echo ========================================
echo.
echo Next steps:
echo 1. Run 'start_conda.bat' to start the application
echo 2. Or manually activate: conda activate tennis-analyzer
echo.
pause

