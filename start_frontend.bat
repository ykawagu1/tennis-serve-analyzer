@echo off
echo 🌐 フロントエンドサーバーを起動しています...
echo.

REM フロントエンドディレクトリに移動
cd frontend

echo フロントエンドサーバーを起動中...
echo ブラウザで http://localhost:5173 にアクセスしてください
echo.
echo ⚠️ このウィンドウを閉じるとフロントエンドサーバーが停止します
echo.

npm run dev

