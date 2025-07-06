# 🔧 トラブルシューティングガイド

## ❌ ERR_CONNECTION_REFUSED エラーの解決方法

このエラーは **サーバーが起動していない** ことが原因です。以下の手順で確実に解決できます。

## 🔍 ステップ1: 現在の状況を確認

### Windows の場合
1. **Ctrl + Shift + Esc** でタスクマネージャーを開く
2. 「詳細」タブで以下のプロセスがあるか確認：
   - `python.exe` または `python3.exe`
   - `node.exe`

### Mac の場合
1. **アクティビティモニタ** を開く
2. 以下のプロセスがあるか確認：
   - `python3`
   - `node`

## 🚀 ステップ2: サーバーを正しく起動

### 方法1: バッチファイル/スクリプトを使用（推奨）

#### Windows
1. **すべてのコマンドプロンプトを閉じる**
2. プロジェクトフォルダで **`start_system.bat`** をダブルクリック
3. 以下の表示が出るまで待つ：
   ```
   * Running on http://127.0.0.1:5000
   ```
4. **新しい** コマンドプロンプトで **`start_frontend.bat`** をダブルクリック
5. 以下の表示が出るまで待つ：
   ```
   Local:   http://localhost:5173/
   ```

#### Mac
1. **すべてのターミナルを閉じる**
2. 新しいターミナルでプロジェクトフォルダに移動
3. `./start_system.sh` を実行
4. 以下の表示が出るまで待つ：
   ```
   * Running on http://127.0.0.1:5000
   ```
5. **新しい** ターミナルで `./start_frontend.sh` を実行
6. 以下の表示が出るまで待つ：
   ```
   Local:   http://localhost:5173/
   ```

### 方法2: 手動で起動

#### バックエンドサーバーの起動
```bash
# Windows
cd backend\app
python main.py

# Mac
cd backend/app
python3 main.py
```

#### フロントエンドサーバーの起動（新しいターミナル/コマンドプロンプト）
```bash
cd frontend
npm run dev
```

## ⏰ ステップ3: 起動完了を確認

### バックエンドサーバーの確認
以下の表示が出れば成功：
```
テニスサービス動作解析APIサーバーを起動中...
* Serving Flask app 'main'
* Debug mode: on
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://169.254.0.21:5000
```

### フロントエンドサーバーの確認
以下の表示が出れば成功：
```
VITE v4.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: http://192.168.x.x:5173/
```

## 🌐 ステップ4: ブラウザでアクセス

1. **両方のサーバーが起動完了** してから
2. ブラウザで **http://localhost:5173** にアクセス
3. テニスサービス解析システムの画面が表示される

## 🔧 よくある問題と解決方法

### 問題1: 「python は認識されません」
**Windows の場合:**
- `python` の代わりに `py` を使用
- または Python を再インストール（「Add to PATH」にチェック）

### 問題2: 「npm は認識されません」
**解決方法:**
- Node.js を再インストール
- コマンドプロンプト/ターミナルを再起動

### 問題3: ポート5000が使用中
**解決方法:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [プロセスID] /F

# Mac
lsof -ti:5000 | xargs kill -9
```

### 問題4: ポート5173が使用中
**解決方法:**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID [プロセスID] /F

# Mac
lsof -ti:5173 | xargs kill -9
```

### 問題5: 依存関係エラー
**解決方法:**
```bash
# Python ライブラリを再インストール
pip install --upgrade mediapipe opencv-python flask flask-cors openai python-dotenv requests

# Node.js 依存関係を再インストール
cd frontend
rm -rf node_modules
npm install
```

## 🔄 完全リセット手順

すべてがうまくいかない場合：

### Windows
1. すべてのコマンドプロンプトを閉じる
2. タスクマネージャーで `python.exe` と `node.exe` を終了
3. パソコンを再起動
4. `start_system.bat` から再実行

### Mac
1. すべてのターミナルを閉じる
2. アクティビティモニタで `python3` と `node` を終了
3. パソコンを再起動
4. `./start_system.sh` から再実行

## 📞 それでも解決しない場合

以下の情報を教えてください：

1. **使用OS**: Windows 10/11 または macOS
2. **エラーメッセージ**: 正確なエラー文をコピー
3. **実行したコマンド**: どの手順で問題が発生したか
4. **画面の状況**: スクリーンショットがあれば

## ✅ 成功確認チェックリスト

- [ ] バックエンドサーバーが起動している（ポート5000）
- [ ] フロントエンドサーバーが起動している（ポート5173）
- [ ] 両方のターミナル/コマンドプロンプトが開いたまま
- [ ] ブラウザで http://localhost:5173 にアクセス
- [ ] テニスサービス解析システムの画面が表示される

---

**必ず解決できます！一緒に頑張りましょう！** 🎾

