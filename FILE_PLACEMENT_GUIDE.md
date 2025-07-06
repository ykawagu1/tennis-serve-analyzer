# 📁 プロジェクトファイルの配置確認ガイド

## 🎯 現在の状況確認

### まず、どこにファイルがあるかを確認しましょう

#### 方法1: エクスプローラーで確認（Windows）
1. **Windowsキー + E** でエクスプローラーを開く
2. 以下の場所を確認：
   - デスクトップ
   - ダウンロードフォルダ
   - ドキュメントフォルダ

#### 方法2: コマンドで確認
```cmd
# 現在の場所を確認
cd

# デスクトップを確認
dir %USERPROFILE%\Desktop

# ダウンロードフォルダを確認
dir %USERPROFILE%\Downloads

# tennis-serve-analyzer フォルダを探す
dir /s tennis-serve-analyzer
```

## 📋 必要なファイル一覧

### 私が作成したファイル（提供済み）
```
tennis-serve-analyzer/
├── backend/
│   └── app/
│       ├── main.py                    ← Flask APIサーバー
│       └── services/
│           ├── pose_detector.py       ← ポーズ検出
│           ├── motion_analyzer.py     ← 動作解析
│           ├── video_processor.py     ← 動画処理
│           └── advice_generator.py    ← アドバイス生成
├── frontend/
│   ├── package.json                   ← フロントエンド設定
│   └── src/
│       └── App.jsx                    ← メインUI
├── setup_conda.bat                    ← 環境セットアップ
├── start_conda.bat                    ← システム起動
├── test_conda.py                      ← 動作確認
└── README.md                          ← 説明書
```

## 🔍 ファイル配置の確認方法

### ステップ1: プロジェクトフォルダの場所を特定

#### Anaconda Promptで確認
```bash
# Anaconda Promptを開く
# 現在の場所を確認
pwd
# または
cd

# tennis-serve-analyzer フォルダを探す
dir | findstr tennis
# または
ls | grep tennis
```

#### 見つからない場合の検索
```cmd
# Cドライブ全体から検索
dir /s C:\tennis-serve-analyzer

# ユーザーフォルダから検索
dir /s %USERPROFILE%\tennis-serve-analyzer
```

### ステップ2: 正しいフォルダ構造の確認

#### 理想的な配置場所
```
推奨場所: C:\Users\[ユーザー名]\Desktop\tennis-serve-analyzer\
または: C:\Users\[ユーザー名]\Documents\tennis-serve-analyzer\
```

#### フォルダ構造確認コマンド
```cmd
# プロジェクトフォルダに移動
cd C:\Users\[ユーザー名]\Desktop\tennis-serve-analyzer

# 構造を確認
tree /f
# または
dir /s
```

### ステップ3: 必須ファイルの存在確認

#### 重要ファイルの確認
```cmd
# バックエンドファイル確認
dir backend\app\main.py
dir backend\app\services\pose_detector.py
dir backend\app\services\motion_analyzer.py
dir backend\app\services\video_processor.py
dir backend\app\services\advice_generator.py

# フロントエンドファイル確認
dir frontend\package.json
dir frontend\src\App.jsx

# セットアップファイル確認
dir setup_conda.bat
dir start_conda.bat
dir test_conda.py
```

## 🚀 ファイルが見つからない場合の対処法

### 対処法1: ファイルを再ダウンロード
1. 提供されたファイルを再度ダウンロード
2. 適切な場所に配置

### 対処法2: 正しい場所に移動
```cmd
# 新しいプロジェクトフォルダを作成
mkdir C:\Users\%USERNAME%\Desktop\tennis-serve-analyzer
cd C:\Users\%USERNAME%\Desktop\tennis-serve-analyzer

# 必要なサブフォルダを作成
mkdir backend\app\services
mkdir backend\app\uploads
mkdir backend\app\outputs
mkdir frontend\src
mkdir frontend\public
```

### 対処法3: ファイル配置確認スクリプト

#### check_files.bat を作成
```batch
@echo off
echo ========================================
echo Project Files Check
echo ========================================
echo.

echo Current directory: %CD%
echo.

echo [1] Checking backend files...
if exist "backend\app\main.py" (
    echo ✅ main.py found
) else (
    echo ❌ main.py NOT found
)

if exist "backend\app\services\pose_detector.py" (
    echo ✅ pose_detector.py found
) else (
    echo ❌ pose_detector.py NOT found
)

if exist "backend\app\services\motion_analyzer.py" (
    echo ✅ motion_analyzer.py found
) else (
    echo ❌ motion_analyzer.py NOT found
)

if exist "backend\app\services\video_processor.py" (
    echo ✅ video_processor.py found
) else (
    echo ❌ video_processor.py NOT found
)

if exist "backend\app\services\advice_generator.py" (
    echo ✅ advice_generator.py found
) else (
    echo ❌ advice_generator.py NOT found
)

echo.
echo [2] Checking frontend files...
if exist "frontend\package.json" (
    echo ✅ package.json found
) else (
    echo ❌ package.json NOT found
)

if exist "frontend\src\App.jsx" (
    echo ✅ App.jsx found
) else (
    echo ❌ App.jsx NOT found
)

echo.
echo [3] Checking setup files...
if exist "setup_conda.bat" (
    echo ✅ setup_conda.bat found
) else (
    echo ❌ setup_conda.bat NOT found
)

if exist "start_conda.bat" (
    echo ✅ start_conda.bat found
) else (
    echo ❌ start_conda.bat NOT found
)

if exist "test_conda.py" (
    echo ✅ test_conda.py found
) else (
    echo ❌ test_conda.py NOT found
)

echo.
echo ========================================
echo File Check Complete
echo ========================================
echo.
echo If files are missing:
echo 1. Download the project files again
echo 2. Place them in the correct location
echo 3. Run this check again
echo.
pause
```

## 📂 正しい配置手順

### ステップ1: プロジェクトフォルダを作成
```cmd
# デスクトップにプロジェクトフォルダを作成
cd %USERPROFILE%\Desktop
mkdir tennis-serve-analyzer
cd tennis-serve-analyzer
```

### ステップ2: サブフォルダを作成
```cmd
# 必要なフォルダ構造を作成
mkdir backend\app\services
mkdir backend\app\uploads
mkdir backend\app\outputs
mkdir frontend\src
mkdir frontend\public
```

### ステップ3: ファイルを配置
1. **backend/app/main.py** を配置
2. **backend/app/services/** に4つのPythonファイルを配置
3. **frontend/package.json** と **frontend/src/App.jsx** を配置
4. **setup_conda.bat**, **start_conda.bat**, **test_conda.py** をルートに配置

### ステップ4: 配置確認
```cmd
# 最終確認
tree /f
```

## 🎯 簡単確認方法

### 1行コマンドで確認
```cmd
# 重要ファイルが全部あるかチェック
if exist "backend\app\main.py" if exist "frontend\package.json" if exist "setup_conda.bat" echo "✅ 主要ファイル確認OK" else echo "❌ ファイル不足"
```

### エクスプローラーで視覚確認
1. プロジェクトフォルダを開く
2. 以下が見えるか確認：
   - **backend** フォルダ
   - **frontend** フォルダ
   - **setup_conda.bat** ファイル
   - **start_conda.bat** ファイル

## 🆘 まだ分からない場合

### 教えてください：
1. **現在どのフォルダにいますか？**
   - `cd` コマンドの結果
2. **どんなファイルが見えますか？**
   - `dir` コマンドの結果
3. **ファイルはどこにダウンロードしましたか？**
   - デスクトップ？ダウンロードフォルダ？

---

**具体的な状況を教えてください！一緒に解決しましょう！** 🎾

