#!/bin/bash

echo "🎾 テニスサービス解析システムを起動しています..."
echo

# 現在のディレクトリを確認
if [ ! -d "backend" ]; then
    echo "❌ エラー: プロジェクトフォルダで実行してください"
    exit 1
fi

# 必要なディレクトリを作成
mkdir -p backend/app/uploads
mkdir -p backend/app/outputs

echo "📚 Pythonライブラリを確認中..."
pip3 install mediapipe opencv-python flask flask-cors openai python-dotenv requests

echo
echo "🌐 フロントエンドの依存関係を確認中..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "依存関係をインストール中..."
    npm install
fi
cd ..

echo
echo "🎬 デモ動画を作成中..."
if [ ! -f "demo_tennis_serve.mp4" ]; then
    python3 create_demo_video.py
fi

echo
echo "✅ 準備完了！"
echo
echo "🚀 システムを起動します..."
echo "  - バックエンドサーバー: http://localhost:5000"
echo "  - フロントエンド: http://localhost:5173"
echo
echo "⚠️  重要: "
echo "  1. バックエンドサーバーが起動したら、新しいターミナルを開いて"
echo "  2. 「./start_frontend.sh」を実行してください"
echo
echo "📝 ログを確認するには、このウィンドウを開いたままにしてください"
echo

# バックエンドサーバーを起動
cd backend/app
echo "バックエンドサーバーを起動中..."
python3 main.py

