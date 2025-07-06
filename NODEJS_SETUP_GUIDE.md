# 🟢 Node.js インストールガイド

## 📋 概要

テニス解析ソフトのフロントエンド（React）を動作させるために、Node.jsをインストールする手順です。

## 🚀 最短インストール手順（Windows）

### ステップ1: Node.jsのダウンロード

1. **[Node.js公式サイト](https://nodejs.org/ja/)** にアクセス
2. **「LTS（推奨版）」** をクリックしてダウンロード
   - 現在の推奨版：Node.js 20.x.x LTS
   - ファイル名：`node-v20.x.x-x64.msi`

### ステップ2: インストール実行

1. ダウンロードした `.msi` ファイルをダブルクリック
2. インストーラーの指示に従って進む
3. **重要**: 「Add to PATH」にチェックが入っていることを確認
4. 「Install」をクリック
5. インストール完了まで待つ（3-5分）

### ステップ3: インストール確認

**新しいコマンドプロンプトを開いて**以下を実行：

```cmd
node --version
npm --version
```

**期待される出力**:
```
v20.x.x
10.x.x
```

## ⚡ 即座に使える自動インストールスクリプト

### Windows用自動インストーラー

```cmd
# PowerShellを管理者として実行
# Chocolateyをインストール（パッケージマネージャー）
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Node.jsをインストール
choco install nodejs -y

# インストール確認
node --version
npm --version
```

## 🔧 Anaconda環境での統合セットアップ

### conda-forgeからのインストール

```bash
# Anaconda Promptで実行
conda activate tennis-analyzer
conda install -c conda-forge nodejs npm -y

# インストール確認
node --version
npm --version
```

## 🚨 よくある問題と解決方法

### 問題1: 'npm' は認識されていません

**症状**:
```
'npm' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```

**解決方法A（推奨）**:
1. **コマンドプロンプトを完全に閉じる**
2. **新しいコマンドプロンプトを開く**
3. `node --version` と `npm --version` を確認

**解決方法B（PATH設定）**:
```cmd
# 環境変数PATHを確認
echo %PATH%

# Node.jsのパスが含まれているか確認
# 通常: C:\Program Files\nodejs\
```

**解決方法C（手動PATH追加）**:
1. 「システムのプロパティ」→「環境変数」
2. 「Path」を編集
3. `C:\Program Files\nodejs\` を追加
4. システム再起動

### 問題2: 古いバージョンがインストールされている

**症状**:
```
node --version
v14.x.x (古いバージョン)
```

**解決方法**:
```cmd
# 現在のNode.jsをアンインストール
# コントロールパネル → プログラムと機能 → Node.js をアンインストール

# 最新版を再インストール
# https://nodejs.org/ja/ から最新LTS版をダウンロード
```

### 問題3: 管理者権限エラー

**症状**:
```
EACCES: permission denied
```

**解決方法**:
```cmd
# コマンドプロンプトを管理者として実行
# または
npm config set prefix %APPDATA%\npm
```

## 🎯 フロントエンドセットアップ

Node.jsのインストールが完了したら：

### ステップ1: プロジェクトディレクトリに移動

```cmd
cd C:\Users\kumon\Desktop\tennis-serve-analyzer\frontend
```

### ステップ2: 依存関係のインストール

```cmd
npm install
```

**期待される出力**:
```
added 1000+ packages in 30s
```

### ステップ3: 開発サーバーの起動

```cmd
npm run dev -- --host
```

**期待される出力**:
```
  VITE v5.0.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/
```

## 🔍 トラブルシューティング

### npm installが失敗する場合

```cmd
# キャッシュをクリア
npm cache clean --force

# node_modulesを削除して再インストール
rmdir /s node_modules
del package-lock.json
npm install
```

### ポート5173が使用中の場合

```cmd
# 別のポートで起動
npm run dev -- --port 3000 --host

# または使用中のプロセスを終了
netstat -ano | findstr :5173
taskkill /PID [プロセスID] /F
```

## 📦 完全自動セットアップスクリプト

### setup_nodejs.bat

```cmd
@echo off
echo ========================================
echo Node.js Setup for Tennis Analyzer
echo ========================================

echo [Step 1] Checking if Node.js is installed...
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed.
    echo Please download and install from: https://nodejs.org/ja/
    echo After installation, restart command prompt and run this script again.
    pause
    exit /b 1
)

echo Node.js is installed!
node --version
npm --version

echo.
echo [Step 2] Installing frontend dependencies...
cd frontend
npm install

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Trying to fix...
    npm cache clean --force
    npm install
)

echo.
echo [Step 3] Testing frontend server...
echo Starting development server...
echo Open http://localhost:5173 in your browser
echo Press Ctrl+C to stop the server

npm run dev -- --host
```

## ✅ 成功確認チェックリスト

- [ ] `node --version` でv20.x.x以上が表示
- [ ] `npm --version` で10.x.x以上が表示
- [ ] `cd frontend` でディレクトリ移動成功
- [ ] `npm install` で依存関係インストール成功
- [ ] `npm run dev -- --host` でサーバー起動成功
- [ ] ブラウザで `http://localhost:5173` にアクセス可能

## 🎯 次のステップ

Node.jsのセットアップが完了したら：

1. **バックエンドを起動**: `start_conda.bat`
2. **フロントエンドを起動**: `npm run dev -- --host`
3. **ブラウザでアクセス**: `http://localhost:5173`
4. **テニス動画をアップロード**して解析テスト

## 📞 サポート

問題が発生した場合は、以下の情報をお知らせください：

1. `node --version` の結果
2. `npm --version` の結果
3. エラーメッセージの全文
4. 実行したコマンドの履歴

**これでフロントエンドが確実に動作します！** 🚀

