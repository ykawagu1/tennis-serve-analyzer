# 🔧 ファイルが見つからない問題の解決方法

診断結果から、**プロジェクトファイルが正しく配置されていない** ことが分かりました。

## 🎯 問題の原因
- Backend files not found → バックエンドファイルが見つからない
- Frontend files not found → フロントエンドファイルが見つからない
- Frontend dependencies not installed → 依存関係がインストールされていない

## 📁 正しいファイル構成

プロジェクトフォルダは以下のような構成になっている必要があります：

```
tennis-serve-analyzer/
├── backend/
│   └── app/
│       ├── main.py
│       ├── services/
│       ├── uploads/
│       └── outputs/
├── frontend/
│   ├── package.json
│   ├── src/
│   └── public/
├── start_system.bat
├── start_frontend.bat
├── setup.sh
└── README.md
```

## 🚀 解決方法

### ステップ1: 現在の場所を確認
1. コマンドプロンプトを開く
2. 以下を実行：
```cmd
dir
```
3. 表示されるファイル一覧を確認

### ステップ2: 正しいフォルダに移動
もし `backend` や `frontend` フォルダが見えない場合：

```cmd
# デスクトップに移動
cd %USERPROFILE%\Desktop

# tennis-serve-analyzer フォルダを探す
dir | findstr tennis

# 見つかったら移動
cd tennis-serve-analyzer

# 再度確認
dir
```

### ステップ3: ファイルが不足している場合
必要なファイルをダウンロードし直してください。

## 🔄 完全セットアップ手順

### 1. 新しいフォルダを作成
```cmd
cd %USERPROFILE%\Desktop
mkdir tennis-serve-analyzer
cd tennis-serve-analyzer
```

### 2. 必要なフォルダ構造を作成
```cmd
mkdir backend\app\services
mkdir backend\app\uploads
mkdir backend\app\outputs
mkdir frontend\src
mkdir frontend\public
```

### 3. ファイルを配置
提供されたすべてのファイルを正しいフォルダに配置してください。

### 4. 依存関係をインストール
```cmd
# Python ライブラリ
pip install mediapipe opencv-python flask flask-cors openai python-dotenv requests

# フロントエンド依存関係
cd frontend
npm install
cd ..
```

## 🎯 簡単な確認方法

正しく配置されているか確認：

```cmd
# バックエンドファイルの確認
dir backend\app\main.py

# フロントエンドファイルの確認
dir frontend\package.json

# 起動スクリプトの確認
dir start_system.bat
dir start_frontend.bat
```

すべて「見つかりました」と表示されればOKです。

## 📞 次のステップ

ファイル配置が完了したら：

1. `check_status_en.bat` を再実行
2. すべて [OK] になることを確認
3. `start_system.bat` でサーバー起動
4. `start_frontend.bat` でフロントエンド起動
5. http://localhost:5173 にアクセス

---

**現在どのフォルダにいるか、どんなファイルが見えるか教えてください！**

