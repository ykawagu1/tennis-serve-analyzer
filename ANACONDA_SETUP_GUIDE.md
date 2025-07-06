# 🐍 Anaconda環境でPython 3.11セットアップガイド

## 📋 概要

Anaconda環境でPython 3.11を設定し、MediaPipeを使ったテニスサービス解析ソフトウェアを動作させるための完全ガイドです。

## 🚀 ステップ1: Python 3.11環境の作成

### 1.1 Anaconda Promptを開く

**Windows**:
1. スタートメニューで「Anaconda Prompt」を検索
2. 「Anaconda Prompt (anaconda3)」をクリック

**Mac**:
1. Launchpadで「Terminal」を開く
2. または「Anaconda Navigator」→「Environments」→「Open Terminal」

### 1.2 新しい環境を作成

```bash
# Python 3.11の新しい環境を作成
conda create -n tennis-analyzer python=3.11 -y

# 環境をアクティベート
conda activate tennis-analyzer

# 現在のPythonバージョンを確認
python --version
```

**✅ 確認ポイント**: `Python 3.11.x` と表示されればOK

## 🔧 ステップ2: 基本パッケージのインストール

### 2.1 condaでインストール可能なパッケージ

```bash
# 基本的なパッケージをcondaでインストール
conda install -c conda-forge numpy opencv flask -y
```

### 2.2 pipでMediaPipeをインストール

```bash
# MediaPipeとその他の依存関係をpipでインストール
pip install mediapipe
pip install flask-cors
pip install openai
```

## 🎯 ステップ3: 依存関係の確認

### 3.1 インストール確認スクリプト

```bash
# Pythonで依存関係を確認
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    import mediapipe as mp
    print('✅ MediaPipe: OK')
except ImportError as e:
    print(f'❌ MediaPipe: {e}')

try:
    import cv2
    print('✅ OpenCV: OK')
except ImportError as e:
    print(f'❌ OpenCV: {e}')

try:
    import flask
    print('✅ Flask: OK')
except ImportError as e:
    print(f'❌ Flask: {e}')

try:
    import numpy as np
    print('✅ NumPy: OK')
except ImportError as e:
    print(f'❌ NumPy: {e}')
"
```

## 🚨 よくある問題と解決方法

### 問題1: MediaPipeのインストールエラー

**エラー例**:
```
ERROR: Could not build wheels for mediapipe
```

**解決方法**:
```bash
# Visual C++ Build Toolsが必要な場合
# https://visualstudio.microsoft.com/visual-cpp-build-tools/ からダウンロード

# または、conda-forgeから試す
conda install -c conda-forge mediapipe -y
```

### 問題2: OpenCVの競合

**エラー例**:
```
ImportError: cannot import name 'cv2' from 'cv2'
```

**解決方法**:
```bash
# OpenCVを再インストール
pip uninstall opencv-python opencv-contrib-python -y
pip install opencv-python==4.8.1.78
```

### 問題3: protobufバージョン競合

**エラー例**:
```
TypeError: Descriptors cannot not be created directly.
```

**解決方法**:
```bash
# protobufのバージョンを固定
pip install protobuf==3.20.3
```

## 📦 完全なパッケージリスト

### requirements.txtの作成

```bash
# 現在の環境のパッケージリストを出力
pip freeze > requirements.txt
```

### 推奨パッケージバージョン

```
mediapipe==0.10.7
opencv-python==4.8.1.78
flask==2.3.3
flask-cors==4.0.0
numpy==1.24.3
protobuf==3.20.3
openai==0.28.1
```

## 🎾 ステップ4: テニス解析ソフトの準備

### 4.1 プロジェクトディレクトリに移動

```bash
# プロジェクトディレクトリに移動
cd /path/to/tennis-serve-analyzer

# または Windowsの場合
cd C:\Users\kumon\Desktop\tennis-serve-analyzer
```

### 4.2 環境の確認

```bash
# 現在の環境を確認
conda info --envs

# アクティブな環境を確認
conda info

# Pythonパスを確認
which python
```

## 🚀 ステップ5: ソフトウェアの起動

### 5.1 バックエンドの起動

```bash
# tennis-analyzer環境がアクティブか確認
conda activate tennis-analyzer

# バックエンドディレクトリに移動
cd backend/app

# サーバーを起動
python main.py
```

**✅ 成功メッセージ**: `Running on http://127.0.0.1:5000` が表示されればOK

### 5.2 フロントエンドの起動（新しいターミナル）

```bash
# 新しいAnaconda Promptを開く
conda activate tennis-analyzer

# フロントエンドディレクトリに移動
cd frontend

# Node.jsの依存関係をインストール
npm install

# 開発サーバーを起動
npm run dev -- --host
```

**✅ 成功メッセージ**: `Local: http://localhost:5173/` が表示されればOK

## 🔍 トラブルシューティング

### 環境がアクティベートできない場合

```bash
# conda初期化
conda init

# ターミナルを再起動後
conda activate tennis-analyzer
```

### パッケージが見つからない場合

```bash
# conda環境内でpipを使用
conda activate tennis-analyzer
which pip  # conda環境のpipを使用していることを確認
pip install パッケージ名
```

### MediaPipeが動作しない場合

```bash
# 完全にクリーンインストール
pip uninstall mediapipe -y
pip cache purge
pip install mediapipe --no-cache-dir
```

## 📱 動作確認

### テスト用スクリプト

```python
# test_setup.py
import mediapipe as mp
import cv2
import numpy as np

print("🎾 テニス解析環境テスト")
print(f"MediaPipe version: {mp.__version__}")
print(f"OpenCV version: {cv2.__version__}")
print(f"NumPy version: {np.__version__}")

# MediaPipeポーズ検出のテスト
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

print("✅ すべての依存関係が正常にインストールされています！")
```

```bash
# テスト実行
python test_setup.py
```

## 🎯 次のステップ

1. **環境の保存**: `conda env export > tennis-analyzer.yml`
2. **ソフトウェアのテスト**: デモ動画での動作確認
3. **ChatGPT API設定**: より詳細なアドバイス機能の有効化

## 📞 サポート

問題が発生した場合は、以下の情報と一緒にお知らせください：

1. エラーメッセージの全文
2. `conda list` の出力
3. `python --version` の結果
4. 実行したコマンドの履歴

**これで確実にAnaconda環境でMediaPipeが動作します！** 🚀



## 🔧 MediaPipe依存関係の詳細解決

### MediaPipeの依存関係地獄を完全回避

MediaPipeは多くの依存関係を持つため、バージョン競合が発生しやすいです。以下の手順で確実にインストールできます。

### 推奨インストール手順

```bash
# 1. 環境をアクティベート
conda activate tennis-analyzer

# 2. 基本パッケージを特定バージョンでインストール
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
pip install protobuf==3.20.3

# 3. MediaPipeをインストール
pip install mediapipe==0.10.7

# 4. その他の依存関係
pip install flask==2.3.3
pip install flask-cors==4.0.0
```

### よくある依存関係エラーと解決方法

#### エラー1: protobufバージョン競合

**エラーメッセージ**:
```
TypeError: Descriptors cannot not be created directly.
If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
```

**解決方法**:
```bash
# protobufを特定バージョンに固定
pip uninstall protobuf -y
pip install protobuf==3.20.3
```

#### エラー2: NumPyバージョン競合

**エラーメッセージ**:
```
RuntimeError: module compiled against API version 0x10 but this version of numpy is 0xe
```

**解決方法**:
```bash
# NumPyを再インストール
pip uninstall numpy -y
pip install numpy==1.24.3
```

#### エラー3: OpenCVとMediaPipeの競合

**エラーメッセージ**:
```
ImportError: libGL.so.1: cannot open shared object file
```

**解決方法**:
```bash
# OpenCVを特定バージョンで再インストール
pip uninstall opencv-python opencv-contrib-python -y
pip install opencv-python==4.8.1.78
```

### 完全クリーンインストール手順

問題が解決しない場合の最終手段：

```bash
# 1. 環境を完全削除
conda deactivate
conda env remove -n tennis-analyzer

# 2. 新しい環境を作成
conda create -n tennis-analyzer python=3.11 -y
conda activate tennis-analyzer

# 3. 依存関係を順番にインストール
pip install --upgrade pip
pip install numpy==1.24.3
pip install protobuf==3.20.3
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.7
pip install flask==2.3.3
pip install flask-cors==4.0.0
pip install openai==0.28.1
```

### 環境の保存と復元

```bash
# 環境をYAMLファイルに保存
conda env export > tennis-analyzer.yml

# 他のマシンで環境を復元
conda env create -f tennis-analyzer.yml
```

### MediaPipe動作確認スクリプト

```python
# mediapipe_test.py
import mediapipe as mp
import cv2
import numpy as np

def test_mediapipe():
    print("MediaPipe動作テスト開始...")
    
    # ポーズ検出の初期化
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    
    # テスト用ダミー画像
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 処理実行
    results = pose.process(test_image)
    
    print("✅ MediaPipe正常動作確認")
    pose.close()

if __name__ == "__main__":
    test_mediapipe()
```

### パフォーマンス最適化

```bash
# CPUのみでMediaPipeを使用する場合
export MEDIAPIPE_DISABLE_GPU=1

# または環境変数を永続化
echo 'export MEDIAPIPE_DISABLE_GPU=1' >> ~/.bashrc
```

### Windows特有の問題

#### Visual C++ Redistributableが必要な場合

1. [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)をダウンロード
2. インストール実行
3. システム再起動
4. MediaPipeを再インストール

#### PATH環境変数の問題

```cmd
# Anaconda Promptで確認
where python
where pip

# 正しいパスが表示されることを確認
```

