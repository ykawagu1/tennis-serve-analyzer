@echo off
echo 🎾 テニスサービス解析システムを起動しています...
echo.

REM 現在のディレクトリを確認
if not exist "backend" (
    echo ❌ エラー: プロジェクトフォルダで実行してください
    pause
    exit /b 1
)

REM 必要なディレクトリを作成
if not exist "backend\app\uploads" mkdir backend\app\uploads
if not exist "backend\app\outputs" mkdir backend\app\outputs

echo 📚 Pythonライブラリを確認中...
pip install mediapipe opencv-python flask flask-cors openai python-dotenv requests

echo.
echo 🌐 フロントエンドの依存関係を確認中...
cd frontend
if not exist "node_modules" (
    echo 依存関係をインストール中...
    npm install
)
cd ..

echo.
echo 🎬 デモ動画を作成中...
if not exist "demo_tennis_serve.mp4" (
    python create_demo_video.py
)

echo.
echo ✅ 準備完了！
echo.
echo 🚀 システムを起動します...
echo   - バックエンドサーバー: http://localhost:5000
echo   - フロントエンド: http://localhost:5173
echo.
echo ⚠️  重要: 
echo   1. バックエンドサーバーが起動したら、新しいコマンドプロンプトを開いて
echo   2. 「start_frontend.bat」を実行してください
echo.
echo 📝 ログを確認するには、このウィンドウを開いたままにしてください
echo.

REM バックエンドサーバーを起動
cd backend\app
echo バックエンドサーバーを起動中...
python main.py

