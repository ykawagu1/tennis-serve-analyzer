# 🌐 フロントエンドテストガイド

## 📋 概要

Node.jsインストール後、テニス解析ソフトのフロントエンド（React）が正常に動作するかをテストする手順です。

## 🚀 ステップバイステップテスト

### ステップ1: Node.js環境の確認

```cmd
# 新しいコマンドプロンプトを開く
# プロジェクトディレクトリに移動
cd C:\Users\kumon\Desktop\tennis-serve-analyzer

# Node.js環境をチェック
check_nodejs.bat
```

**期待される結果**:
```
✅ Node.js: Installed (v20.x.x)
✅ npm: Available (10.x.x)
✅ Frontend directory: Found
✅ package.json: Found
```

### ステップ2: 依存関係のインストール

```cmd
# フロントエンドディレクトリに移動
cd frontend

# 依存関係をインストール
npm install
```

**期待される出力**:
```
added 1000+ packages, and audited 1001 packages in 30s

found 0 vulnerabilities
```

**エラーが出る場合**:
```cmd
# キャッシュをクリアして再試行
npm cache clean --force
npm install --legacy-peer-deps
```

### ステップ3: 開発サーバーの起動テスト

```cmd
# 開発サーバーを起動
npm run dev -- --host
```

**期待される出力**:
```
  VITE v5.0.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/
  ➜  press h to show help
```

### ステップ4: ブラウザでの動作確認

1. ブラウザで `http://localhost:5173` にアクセス
2. 以下が表示されることを確認：
   - 「テニスサービス動作解析システム」のタイトル
   - ステップインジケーター（1. 動画選択 → 2. 解析実行 → 3. 結果確認）
   - ファイル選択エリア
   - 美しいUI（青とグリーンのグラデーション）

## 🔧 自動テストスクリプト

### frontend_test.bat

```cmd
@echo off
echo ========================================
echo Frontend Functionality Test
echo ========================================

cd frontend

echo [Test 1] Package installation check...
if exist "node_modules" (
    echo ✅ Dependencies installed
) else (
    echo ❌ Dependencies missing, installing...
    npm install
)

echo.
echo [Test 2] Build test...
npm run build
if errorlevel 1 (
    echo ❌ Build failed
    exit /b 1
) else (
    echo ✅ Build successful
)

echo.
echo [Test 3] Development server test...
echo Starting server for 10 seconds...
timeout /t 10 /nobreak > nul & npm run dev -- --host
```

## 🎯 機能別テスト

### UIコンポーネントテスト

1. **ヘッダー表示**
   - タイトル「テニスサービス動作解析システム」
   - サブタイトル「AIを活用して...」

2. **ステップインジケーター**
   - 3つのステップが表示
   - 現在のステップがハイライト

3. **ファイル選択エリア**
   - ドラッグ&ドロップエリア
   - 「ファイルを選択」ボタン
   - 撮影のコツが表示

### レスポンシブデザインテスト

```cmd
# ブラウザの開発者ツールを開く（F12）
# デバイスツールバーをクリック
# 以下のデバイスでテスト：
# - iPhone 12 Pro (390x844)
# - iPad (768x1024)
# - Desktop (1920x1080)
```

### ファイルアップロードテスト

1. 「ファイルを選択」をクリック
2. 動画ファイル（MP4, AVI, MOV）を選択
3. ファイル情報が表示されることを確認
4. 「解析開始」ボタンが有効になることを確認

## 🚨 よくある問題と解決方法

### 問題1: ブラウザで真っ白な画面

**症状**: `http://localhost:5173` にアクセスしても何も表示されない

**解決方法**:
```cmd
# 開発サーバーを停止（Ctrl+C）
# キャッシュをクリア
npm run build
npm run preview
```

### 問題2: "Module not found" エラー

**症状**: コンソールに赤いエラーメッセージ

**解決方法**:
```cmd
# 依存関係を再インストール
rm -rf node_modules package-lock.json  # Mac/Linux
rmdir /s node_modules & del package-lock.json  # Windows
npm install
```

### 問題3: ポート5173が使用中

**症状**: `Port 5173 is in use`

**解決方法**:
```cmd
# 別のポートで起動
npm run dev -- --port 3000 --host

# または使用中のプロセスを終了
netstat -ano | findstr :5173
taskkill /PID [プロセスID] /F
```

### 問題4: ホットリロードが動作しない

**症状**: ファイルを変更しても自動更新されない

**解決方法**:
```cmd
# 開発サーバーを再起動
# Ctrl+C で停止
npm run dev -- --host
```

## 📱 モバイル対応テスト

### スマートフォンでのテスト

1. 同じWi-Fiネットワークに接続
2. スマートフォンのブラウザで `http://[PCのIPアドレス]:5173` にアクセス
3. タッチ操作が正常に動作することを確認

### IPアドレスの確認方法

```cmd
# Windows
ipconfig | findstr IPv4

# 出力例: 192.168.1.100
# スマートフォンで http://192.168.1.100:5173 にアクセス
```

## 🔍 パフォーマンステスト

### ページ読み込み速度

1. ブラウザの開発者ツール（F12）
2. Networkタブを開く
3. ページをリロード（Ctrl+R）
4. 読み込み時間を確認（目標：3秒以内）

### メモリ使用量

1. 開発者ツールのPerformanceタブ
2. 「Record」をクリック
3. 10秒間操作
4. 「Stop」をクリック
5. メモリリークがないことを確認

## ✅ テスト完了チェックリスト

### 基本機能
- [ ] Node.js環境が正常
- [ ] npm installが成功
- [ ] 開発サーバーが起動
- [ ] ブラウザでUIが表示
- [ ] ファイル選択が動作

### UI/UX
- [ ] レスポンシブデザイン
- [ ] タッチ操作対応
- [ ] 美しいデザイン
- [ ] 直感的な操作
- [ ] エラーメッセージ表示

### パフォーマンス
- [ ] 高速な読み込み（3秒以内）
- [ ] スムーズなアニメーション
- [ ] メモリリークなし
- [ ] モバイルでも快適

## 🎯 次のステップ

フロントエンドテストが完了したら：

1. **バックエンドとの連携テスト**
   - `start_conda.bat` でバックエンド起動
   - 実際の動画ファイルでテスト

2. **統合テスト**
   - ファイルアップロード → 解析 → 結果表示の一連の流れ

3. **本番環境テスト**
   - `npm run build` でビルド
   - 静的ファイルの動作確認

## 📞 サポート

問題が発生した場合は、以下の情報をお知らせください：

1. ブラウザのコンソールエラー（F12 → Console）
2. `npm run dev` の出力
3. `check_nodejs.bat` の結果
4. 使用しているブラウザとバージョン

**これでフロントエンドが確実に動作します！** 🌐

