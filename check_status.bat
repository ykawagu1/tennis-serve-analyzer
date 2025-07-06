@echo off
echo 🔍 システム状況を確認しています...
echo.

echo ========================================
echo Python の確認
echo ========================================
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python が見つかりません
    echo    Python をインストールしてください: https://www.python.org/downloads/
) else (
    echo ✅ Python が利用可能です
)
echo.

echo ========================================
echo Node.js の確認
echo ========================================
node --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js が見つかりません
    echo    Node.js をインストールしてください: https://nodejs.org/
) else (
    echo ✅ Node.js が利用可能です
)
echo.

echo ========================================
echo ポート使用状況の確認
echo ========================================
echo ポート 5000 (バックエンド):
netstat -an | findstr :5000
if %errorlevel% neq 0 (
    echo ❌ ポート 5000 は使用されていません（バックエンドサーバーが起動していない）
) else (
    echo ✅ ポート 5000 が使用されています（バックエンドサーバーが起動中）
)

echo.
echo ポート 5173 (フロントエンド):
netstat -an | findstr :5173
if %errorlevel% neq 0 (
    echo ❌ ポート 5173 は使用されていません（フロントエンドサーバーが起動していない）
) else (
    echo ✅ ポート 5173 が使用されています（フロントエンドサーバーが起動中）
)
echo.

echo ========================================
echo プロセス確認
echo ========================================
echo Python プロセス:
tasklist | findstr python
echo.
echo Node プロセス:
tasklist | findstr node
echo.

echo ========================================
echo ファイル確認
echo ========================================
if exist "backend\app\main.py" (
    echo ✅ バックエンドファイルが存在します
) else (
    echo ❌ バックエンドファイルが見つかりません
)

if exist "frontend\package.json" (
    echo ✅ フロントエンドファイルが存在します
) else (
    echo ❌ フロントエンドファイルが見つかりません
)

if exist "frontend\node_modules" (
    echo ✅ フロントエンド依存関係がインストール済みです
) else (
    echo ❌ フロントエンド依存関係がインストールされていません
    echo    frontend フォルダで 'npm install' を実行してください
)
echo.

echo ========================================
echo 推奨アクション
echo ========================================
echo 1. 両方のサーバーが起動していない場合:
echo    - start_system.bat を実行
echo    - start_frontend.bat を実行
echo.
echo 2. ポートが使用中の場合:
echo    - 他のアプリケーションを終了
echo    - パソコンを再起動
echo.
echo 3. 依存関係が不足している場合:
echo    - setup.sh を実行
echo.

pause

