# 🔧 「Running on http://127.0.0.1:5000」が出ない問題の解決

## 🎯 問題の原因と解決方法

### 原因1: 間違ったフォルダで実行している
**症状**: 何も表示されない、または「ファイルが見つかりません」エラー

**解決方法**:
```cmd
# 現在の場所を確認
dir

# main.py があるか確認
dir backend\app\main.py

# なければ正しいフォルダに移動
cd Desktop
cd tennis-serve-analyzer
```

### 原因2: Pythonライブラリが不足している
**症状**: エラーメッセージが表示される

**解決方法**:
```cmd
# 必要なライブラリをインストール
pip install mediapipe opencv-python flask flask-cors openai python-dotenv requests
```

### 原因3: main.pyファイルが存在しない
**症状**: 「指定されたファイルが見つかりません」エラー

**解決方法**: ファイルを正しい場所に配置する

### 原因4: Pythonのパスが通っていない
**症状**: 「python は認識されません」エラー

**解決方法**:
```cmd
# python の代わりに py を使用
py backend\app\main.py

# または
python3 backend\app\main.py
```

## 🔍 段階的診断方法

### ステップ1: 現在の場所を確認
```cmd
dir
```
**何が表示されますか？**

### ステップ2: 必要なファイルがあるか確認
```cmd
dir backend\app\main.py
```
**「1 個のファイル」と表示されればOK**

### ステップ3: Pythonが動くか確認
```cmd
python --version
```
**バージョンが表示されればOK**

### ステップ4: 手動でサーバーを起動
```cmd
cd backend\app
python main.py
```

## 🚨 よくあるエラーと解決方法

### エラー1: 「python は認識されません」
```cmd
# 解決方法
py main.py
```

### エラー2: 「No module named 'flask'」
```cmd
# 解決方法
pip install flask flask-cors
```

### エラー3: 「No module named 'mediapipe'」
```cmd
# 解決方法
pip install mediapipe opencv-python
```

### エラー4: 「指定されたパスが見つかりません」
```cmd
# 現在の場所を確認
cd
# 正しいフォルダに移動
cd %USERPROFILE%\Desktop\tennis-serve-analyzer
```

## 🎯 確実な起動方法

### 方法1: 一つずつ確認
```cmd
# 1. 正しいフォルダに移動
cd %USERPROFILE%\Desktop\tennis-serve-analyzer

# 2. ファイルがあるか確認
dir backend\app\main.py

# 3. ライブラリをインストール
pip install mediapipe opencv-python flask flask-cors openai python-dotenv requests

# 4. サーバーを起動
cd backend\app
python main.py
```

### 方法2: 別のPythonコマンドを試す
```cmd
cd backend\app
py main.py
```

### 方法3: フルパスで実行
```cmd
python %USERPROFILE%\Desktop\tennis-serve-analyzer\backend\app\main.py
```

## 📋 成功時の表示例

正常に起動すると以下のように表示されます：
```
テニスサービス動作解析APIサーバーを起動中...
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

## 🆘 まだ解決しない場合

以下の情報を教えてください：

1. **`dir` コマンドの結果**
2. **`python --version` の結果**
3. **`dir backend\app\main.py` の結果**
4. **表示されるエラーメッセージ（正確にコピー）**

---

**どのエラーが出ているか、どの段階で止まっているか教えてください！** 🎾

