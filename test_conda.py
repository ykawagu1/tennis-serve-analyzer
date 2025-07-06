#!/usr/bin/env python3
"""
Anaconda環境でのテニス解析システムテストスクリプト
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Pythonバージョンのテスト"""
    print("🐍 Python Version Test")
    print(f"Python version: {sys.version}")
    
    version_info = sys.version_info
    if version_info.major == 3 and version_info.minor == 11:
        print("✅ Python 3.11 - OK")
        return True
    else:
        print(f"❌ Expected Python 3.11, got {version_info.major}.{version_info.minor}")
        return False

def test_imports():
    """必要なライブラリのインポートテスト"""
    print("\n📦 Import Test")
    
    imports = [
        ('mediapipe', 'mp'),
        ('cv2', 'cv2'),
        ('flask', 'flask'),
        ('numpy', 'np'),
        ('flask_cors', 'CORS'),
    ]
    
    results = {}
    
    for module_name, import_as in imports:
        try:
            if import_as:
                exec(f"import {module_name} as {import_as}")
            else:
                exec(f"import {module_name}")
            
            # バージョン情報を取得
            try:
                version = eval(f"{import_as}.__version__")
                print(f"✅ {module_name}: OK (v{version})")
            except:
                print(f"✅ {module_name}: OK")
            
            results[module_name] = True
            
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            results[module_name] = False
    
    return results

def test_mediapipe_functionality():
    """MediaPipeの基本機能テスト"""
    print("\n🎾 MediaPipe Functionality Test")
    
    try:
        import mediapipe as mp
        import numpy as np
        
        # ポーズ検出の初期化テスト
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # ダミー画像でのテスト
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
        results = pose.process(dummy_image)
        
        print("✅ MediaPipe Pose initialization: OK")
        print("✅ MediaPipe processing: OK")
        
        pose.close()
        return True
        
    except Exception as e:
        print(f"❌ MediaPipe functionality test failed: {e}")
        return False

def test_project_structure():
    """プロジェクト構造のテスト"""
    print("\n📁 Project Structure Test")
    
    required_files = [
        'backend/app/main.py',
        'backend/app/services/pose_detector.py',
        'backend/app/services/motion_analyzer.py',
        'backend/app/services/video_processor.py',
        'backend/app/services/advice_generator.py',
        'frontend/package.json',
        'frontend/src/App.jsx',
        'README.md'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: Found")
        else:
            print(f"❌ {file_path}: Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files")
        return False
    else:
        print("\n✅ All required files found")
        return True

def test_backend_import():
    """バックエンドモジュールのインポートテスト"""
    print("\n🔧 Backend Import Test")
    
    # backend/appをパスに追加
    backend_path = Path('backend/app')
    if backend_path.exists():
        sys.path.insert(0, str(backend_path.absolute()))
    
    try:
        from services.pose_detector import PoseDetector
        print("✅ PoseDetector: OK")
        
        from services.motion_analyzer import MotionAnalyzer
        print("✅ MotionAnalyzer: OK")
        
        from services.video_processor import VideoProcessor
        print("✅ VideoProcessor: OK")
        
        from services.advice_generator import AdviceGenerator
        print("✅ AdviceGenerator: OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Backend import failed: {e}")
        return False

def main():
    """メインテスト関数"""
    print("🎾 Tennis Serve Analyzer - Anaconda Environment Test")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("MediaPipe Functionality", test_mediapipe_functionality),
        ("Project Structure", test_project_structure),
        ("Backend Imports", test_backend_import),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your environment is ready.")
        print("\nNext steps:")
        print("1. Run 'start_conda.bat' to start the backend")
        print("2. Run 'npm run dev' in the frontend directory")
        print("3. Open http://localhost:5173 in your browser")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the setup.")
        print("\nTroubleshooting:")
        print("1. Run 'setup_conda.bat' to reinstall dependencies")
        print("2. Check ANACONDA_SETUP_GUIDE.md for detailed instructions")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

