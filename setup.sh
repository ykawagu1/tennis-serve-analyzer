#!/bin/bash

# テニスサービス動作解析システム - セットアップスクリプト
# このスクリプトは必要な依存関係をインストールし、システムを起動します

set -e

echo "🎾 テニスサービス動作解析システム - セットアップ開始"
echo "=================================================="

# 現在のディレクトリを確認
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ エラー: プロジェクトのルートディレクトリで実行してください"
    exit 1
fi

# Python環境の確認
echo "🐍 Python環境を確認中..."
if ! command -v python3 &> /dev/null; then
    echo "❌ エラー: Python 3が見つかりません"
    echo "   Python 3.11以上をインストールしてください"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "   Python バージョン: $PYTHON_VERSION"

# Node.js環境の確認
echo "📦 Node.js環境を確認中..."
if ! command -v node &> /dev/null; then
    echo "❌ エラー: Node.jsが見つかりません"
    echo "   Node.js 20以上をインストールしてください"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "   Node.js バージョン: $NODE_VERSION"

# Pythonライブラリのインストール
echo "📚 Pythonライブラリをインストール中..."
pip3 install --user mediapipe opencv-python flask flask-cors openai python-dotenv requests

# フロントエンドの依存関係確認
echo "🌐 フロントエンドの依存関係を確認中..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   依存関係をインストール中..."
    npm install
else
    echo "   依存関係は既にインストール済みです"
fi

cd ..

# デモ動画の作成
echo "🎬 デモ動画を作成中..."
if [ ! -f "demo_tennis_serve.mp4" ]; then
    python3 create_demo_video.py
else
    echo "   デモ動画は既に存在します"
fi

# 必要なディレクトリの作成
echo "📁 必要なディレクトリを作成中..."
mkdir -p backend/app/uploads
mkdir -p backend/app/outputs

echo ""
echo "✅ セットアップが完了しました！"
echo ""
echo "🚀 システムを起動するには:"
echo "   1. バックエンドサーバーを起動:"
echo "      cd backend/app && python3 main.py"
echo ""
echo "   2. 新しいターミナルでフロントエンドサーバーを起動:"
echo "      cd frontend && npm run dev --host"
echo ""
echo "   3. ブラウザでアクセス:"
echo "      http://localhost:5173"
echo ""
echo "💡 ヒント:"
echo "   - アドバイス機能を使用するには OpenAI API キーが必要です"
echo "   - 統合テストを実行するには: python3 integration_test.py"
echo "   - 詳細な使用方法は README.md を参照してください"
echo ""
echo "🎾 テニスの上達を応援します！"

