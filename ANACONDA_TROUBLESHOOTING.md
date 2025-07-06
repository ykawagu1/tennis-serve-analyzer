# 🔧 Anaconda環境 トラブルシューティングガイド

## 📋 概要

Anaconda環境でテニスサービス解析ソフトウェアを動作させる際に発生する可能性のある問題と、その解決方法を包括的にまとめたガイドです。

## 🚨 緊急対応：よくある問題TOP5

### 1. 環境がアクティベートできない

**症状**:
```
CommandNotFoundError: Your shell has not been properly configured to use 'conda activate'.
```

**解決方法**:
```bash
# conda初期化
conda init

# ターミナル/コマンドプロンプトを再起動
# 再度試行
conda activate tennis-analyzer
```

**Windows特有の解決方法**:
```cmd
# Anaconda Promptを管理者として実行
conda init cmd.exe
conda init powershell

# システム再起動後に再試行
```

### 2. MediaPipeインストールエラー

**症状**:
```
ERROR: Could not build wheels for mediapipe
ERROR: Failed building wheel for mediapipe
```

**解決方法A（推奨）**:
```bash
# Visual C++ Build Toolsをインストール
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# その後MediaPipeを再インストール
pip install --upgrade pip
pip install mediapipe==0.10.7
```

**解決方法B（代替）**:
```bash
# conda-forgeから試す
conda install -c conda-forge mediapipe -y
```

**解決方法C（最終手段）**:
```bash
# 事前コンパイル済みwheelを使用
pip install --only-binary=all mediapipe
```

### 3. protobufバージョン競合

**症状**:
```
TypeError: Descriptors cannot not be created directly.
If this call came from a _pb2.py file, your generated code is out of date
```

**解決方法**:
```bash
# protobufを特定バージョンに固定
pip uninstall protobuf -y
pip install protobuf==3.20.3

# 環境を再起動
conda deactivate
conda activate tennis-analyzer
```

### 4. OpenCVとMediaPipeの競合

**症状**:
```
ImportError: libGL.so.1: cannot open shared object file
ImportError: cannot import name 'cv2' from 'cv2'
```

**解決方法**:
```bash
# OpenCVを完全に削除して再インストール
pip uninstall opencv-python opencv-contrib-python opencv-python-headless -y
pip install opencv-python==4.8.1.78

# Linux/Macの場合、追加で必要
sudo apt-get install libgl1-mesa-glx  # Ubuntu/Debian
# brew install mesa  # Mac
```

### 5. 「Running on http://127.0.0.1:5000」が表示されない

**症状**:
- サーバーが起動しない
- エラーメッセージが表示される

**解決方法**:
```bash
# 1. 環境の確認
conda activate tennis-analyzer
python --version

# 2. 依存関係の確認
python -c "import mediapipe, cv2, flask; print('OK')"

# 3. ポートの確認
netstat -an | findstr 5000  # Windows
lsof -i :5000  # Mac/Linux

# 4. 手動でサーバー起動
cd backend/app
python -c "from main import app; app.run(debug=True)"
```

## 🔍 詳細診断と解決方法

### 環境関連の問題

#### 問題: conda環境が見つからない

**症状**:
```
EnvironmentNameNotFound: Could not find conda environment: tennis-analyzer
```

**診断**:
```bash
# 環境一覧を確認
conda env list
conda info --envs
```

**解決方法**:
```bash
# 環境を再作成
conda create -n tennis-analyzer python=3.11 -y
conda activate tennis-analyzer

# setup_conda.batを再実行
setup_conda.bat
```

#### 問題: Pythonバージョンが違う

**症状**:
```
Python 3.9.x (期待値: Python 3.11.x)
```

**解決方法**:
```bash
# 環境を削除して再作成
conda deactivate
conda env remove -n tennis-analyzer
conda create -n tennis-analyzer python=3.11 -y
```

### パッケージ関連の問題

#### 問題: NumPyバージョン競合

**症状**:
```
RuntimeError: module compiled against API version 0x10 but this version of numpy is 0xe
```

**解決方法**:
```bash
# NumPyを特定バージョンで再インストール
pip uninstall numpy -y
pip install numpy==1.24.3

# 他のパッケージも再インストール
pip install mediapipe==0.10.7 --force-reinstall
```

#### 問題: Flask関連エラー

**症状**:
```
ImportError: cannot import name 'Flask' from 'flask'
ModuleNotFoundError: No module named 'flask_cors'
```

**解決方法**:
```bash
# Flaskとその依存関係を再インストール
pip uninstall flask flask-cors -y
pip install flask==2.3.3
pip install flask-cors==4.0.0
```

### システム関連の問題

#### 問題: Windows Defender/ウイルス対策ソフトの干渉

**症状**:
- インストールが途中で止まる
- ファイルアクセスエラー

**解決方法**:
1. Windows Defenderの除外設定
   - 設定 → 更新とセキュリティ → Windows セキュリティ
   - ウイルスと脅威の防止 → 除外
   - `C:\Users\[ユーザー名]\anaconda3` を追加

2. リアルタイム保護を一時的に無効化してインストール

#### 問題: 管理者権限が必要

**症状**:
```
PermissionError: [Errno 13] Permission denied
```

**解決方法**:
```bash
# Anaconda Promptを管理者として実行
# または
sudo conda install パッケージ名  # Mac/Linux
```

### ネットワーク関連の問題

#### 問題: パッケージダウンロードエラー

**症状**:
```
CondaHTTPError: HTTP 000 CONNECTION FAILED
```

**解決方法**:
```bash
# プロキシ設定（企業環境の場合）
conda config --set proxy_servers.http http://proxy.company.com:8080
conda config --set proxy_servers.https https://proxy.company.com:8080

# または、チャンネルを変更
conda config --add channels conda-forge
conda config --set channel_priority strict
```

## 🛠️ 完全リセット手順

すべての方法で解決しない場合の最終手段：

### ステップ1: 環境の完全削除

```bash
# 環境を削除
conda deactivate
conda env remove -n tennis-analyzer

# conda自体のクリーンアップ
conda clean --all -y
```

### ステップ2: Anacondaの再インストール（必要に応じて）

1. Anacondaをアンインストール
2. [Anaconda公式サイト](https://www.anaconda.com/products/distribution)から最新版をダウンロード
3. 再インストール

### ステップ3: 環境の再構築

```bash
# 新しい環境を作成
conda create -n tennis-analyzer python=3.11 -y
conda activate tennis-analyzer

# パッケージを順番にインストール
pip install --upgrade pip
pip install numpy==1.24.3
pip install protobuf==3.20.3
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.7
pip install flask==2.3.3
pip install flask-cors==4.0.0
pip install openai==0.28.1
```

## 🔧 診断ツール

### 自動診断スクリプト

```bash
# 包括的な診断を実行
python test_conda.py

# 特定の問題を診断
python -c "
import sys
import subprocess

print('=== System Information ===')
print(f'Python: {sys.version}')
print(f'Platform: {sys.platform}')

print('\n=== Conda Information ===')
result = subprocess.run(['conda', 'info'], capture_output=True, text=True)
print(result.stdout)

print('\n=== Environment List ===')
result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
print(result.stdout)
"
```

### 手動診断チェックリスト

```bash
# 1. Conda環境の確認
conda --version
conda info
conda env list

# 2. Python環境の確認
which python
python --version
which pip

# 3. パッケージの確認
pip list | grep mediapipe
pip list | grep opencv
pip list | grep flask

# 4. システムの確認
echo $PATH  # Mac/Linux
echo %PATH%  # Windows
```

## 📞 サポートとヘルプ

### 問題報告時に含める情報

1. **システム情報**:
   - OS（Windows 10/11, macOS, Linux）
   - Anacondaバージョン
   - Pythonバージョン

2. **エラー情報**:
   - 完全なエラーメッセージ
   - 実行したコマンド
   - `test_conda.py`の実行結果

3. **環境情報**:
   - `conda list`の出力
   - `conda info`の出力
   - `pip list`の出力

### よくある質問（FAQ）

**Q: MediaPipeのインストールに時間がかかりすぎる**
A: 大きなパッケージのため、10-20分かかることがあります。ネットワーク環境を確認してください。

**Q: 他のPythonプロジェクトに影響しますか？**
A: conda環境を使用しているため、他のプロジェクトには影響しません。

**Q: GPUを使用できますか？**
A: MediaPipeはCPUでも十分高速です。GPU使用は現在サポートしていません。

**Q: Macで動作しますか？**
A: はい、Intel MacとApple Silicon（M1/M2）の両方で動作します。

## 🎯 成功の確認

以下がすべて完了すれば成功です：

- [ ] `conda activate tennis-analyzer`が成功
- [ ] `python --version`でPython 3.11.xが表示
- [ ] `python test_conda.py`ですべてのテストが通過
- [ ] `python backend/app/main.py`でサーバーが起動
- [ ] ブラウザで`http://localhost:5173`にアクセス可能
- [ ] デモ動画の解析が正常に完了

**これで確実にAnaconda環境でテニス解析ソフトが動作します！** 🎾

