# 🔧 簡単！手動でサーバー状況を確認する方法

文字化けが発生した場合は、以下の方法で手動確認してください。

## 🔍 ステップ1: 手動でサーバー状況を確認

### 方法1: タスクマネージャーで確認（Windows）
1. **Ctrl + Shift + Esc** でタスクマネージャーを開く
2. 「詳細」タブをクリック
3. 以下のプロセスがあるか確認：
   - `python.exe` または `python3.exe`
   - `node.exe`

### 方法2: コマンドプロンプトで確認
```cmd
# ポート使用状況を確認
netstat -an | findstr :5000
netstat -an | findstr :5173

# プロセス確認
tasklist | findstr python
tasklist | findstr node
```

## 🚀 ステップ2: サーバーを起動

### 確実な起動方法
1. **すべてのコマンドプロンプトを閉じる**
2. **新しいコマンドプロンプトを開く**
3. プロジェクトフォルダに移動：
   ```cmd
   cd C:\Users\[ユーザー名]\Desktop\tennis-serve-analyzer
   ```

4. **バックエンドサーバーを起動**：
   ```cmd
   cd backend\app
   python main.py
   ```
   
5. **新しいコマンドプロンプトを開く**
6. **フロントエンドサーバーを起動**：
   ```cmd
   cd C:\Users\[ユーザー名]\Desktop\tennis-serve-analyzer\frontend
   npm run dev
   ```

## ✅ 成功の確認

### バックエンドサーバーの成功メッセージ
```
テニスサービス動作解析APIサーバーを起動中...
* Running on http://127.0.0.1:5000
```

### フロントエンドサーバーの成功メッセージ
```
Local:   http://localhost:5173/
```

## 🌐 ブラウザでアクセス
両方のメッセージが表示されたら：
**http://localhost:5173** にアクセス

## 🔧 よくあるエラーと解決方法

### エラー1: 「python は認識されません」
**解決方法**:
- `python` の代わりに `py` を使用
- Python を再インストール（「Add to PATH」にチェック）

### エラー2: 「npm は認識されません」
**解決方法**:
- Node.js を再インストール
- コマンドプロンプトを再起動

### エラー3: 「Address already in use」
**解決方法**:
- タスクマネージャーで `python.exe` と `node.exe` を終了
- パソコンを再起動

## 📞 まだ解決しない場合

以下の情報を教えてください：
1. どの手順でエラーが発生したか
2. 表示されたエラーメッセージ（正確にコピー）
3. タスクマネージャーで `python.exe` や `node.exe` が動いているか

**必ず解決できます！一緒に頑張りましょう！** 🎾

