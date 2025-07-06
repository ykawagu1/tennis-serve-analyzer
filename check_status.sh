#!/bin/bash

echo "🔍 システム状況を確認しています..."
echo

echo "========================================"
echo "Python の確認"
echo "========================================"
if command -v python3 &> /dev/null; then
    echo "✅ Python が利用可能です"
    python3 --version
else
    echo "❌ Python が見つかりません"
    echo "   Python をインストールしてください: https://www.python.org/downloads/"
fi
echo

echo "========================================"
echo "Node.js の確認"
echo "========================================"
if command -v node &> /dev/null; then
    echo "✅ Node.js が利用可能です"
    node --version
else
    echo "❌ Node.js が見つかりません"
    echo "   Node.js をインストールしてください: https://nodejs.org/"
fi
echo

echo "========================================"
echo "ポート使用状況の確認"
echo "========================================"
echo "ポート 5000 (バックエンド):"
if lsof -i :5000 &> /dev/null; then
    echo "✅ ポート 5000 が使用されています（バックエンドサーバーが起動中）"
    lsof -i :5000
else
    echo "❌ ポート 5000 は使用されていません（バックエンドサーバーが起動していない）"
fi

echo
echo "ポート 5173 (フロントエンド):"
if lsof -i :5173 &> /dev/null; then
    echo "✅ ポート 5173 が使用されています（フロントエンドサーバーが起動中）"
    lsof -i :5173
else
    echo "❌ ポート 5173 は使用されていません（フロントエンドサーバーが起動していない）"
fi
echo

echo "========================================"
echo "プロセス確認"
echo "========================================"
echo "Python プロセス:"
ps aux | grep python3 | grep -v grep || echo "Python プロセスが見つかりません"
echo
echo "Node プロセス:"
ps aux | grep node | grep -v grep || echo "Node プロセスが見つかりません"
echo

echo "========================================"
echo "ファイル確認"
echo "========================================"
if [ -f "backend/app/main.py" ]; then
    echo "✅ バックエンドファイルが存在します"
else
    echo "❌ バックエンドファイルが見つかりません"
fi

if [ -f "frontend/package.json" ]; then
    echo "✅ フロントエンドファイルが存在します"
else
    echo "❌ フロントエンドファイルが見つかりません"
fi

if [ -d "frontend/node_modules" ]; then
    echo "✅ フロントエンド依存関係がインストール済みです"
else
    echo "❌ フロントエンド依存関係がインストールされていません"
    echo "   frontend フォルダで 'npm install' を実行してください"
fi
echo

echo "========================================"
echo "推奨アクション"
echo "========================================"
echo "1. 両方のサーバーが起動していない場合:"
echo "   - ./start_system.sh を実行"
echo "   - ./start_frontend.sh を実行"
echo
echo "2. ポートが使用中の場合:"
echo "   - 他のアプリケーションを終了"
echo "   - パソコンを再起動"
echo
echo "3. 依存関係が不足している場合:"
echo "   - ./setup.sh を実行"
echo

read -p "Enterキーを押して終了..."

