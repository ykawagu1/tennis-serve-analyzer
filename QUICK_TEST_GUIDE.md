# 🎾 テニス解析ソフト動作確認ガイド

## 📋 概要

Anaconda環境でテニスサービス解析ソフトウェアが正常に動作するかを確認するためのガイドです。

## 🚀 クイックテスト（5分で完了）

### ステップ1: 環境の確認

```bash
# Anaconda Promptを開く
conda activate tennis-analyzer

# Pythonバージョンを確認
python --version
# 期待値: Python 3.11.x

# 必要なパッケージを確認
python -c "import mediapipe, cv2, flask, numpy; print('✅ All packages imported successfully')"
```

### ステップ2: 自動テストスクリプトの実行

```bash
# プロジェクトディレクトリに移動
cd tennis-serve-analyzer

# テストスクリプトを実行
python test_conda.py
```

**期待される出力**:
```
🎾 Tennis Serve Analyzer - Anaconda Environment Test
============================================================
✅ Python Version: PASS
✅ Package Imports: PASS
✅ MediaPipe Functionality: PASS
✅ Project Structure: PASS
✅ Backend Imports: PASS

Total: 5/5 tests passed
🎉 All tests passed! Your environment is ready.
```

### ステップ3: バックエンドサーバーの起動テスト

```bash
# バックエンドを起動
start_conda.bat

# または手動で
conda activate tennis-analyzer
cd backend/app
python main.py
```

**期待される出力**:
```
🎾 Tennis Serve Analyzer Backend Server
========================================
✅ MediaPipe initialized successfully
✅ Flask server starting...
 * Running on http://127.0.0.1:5000
```

### ステップ4: フロントエンドの起動テスト

**新しいAnaconda Promptを開く**:

```bash
# プロジェクトディレクトリに移動
cd tennis-serve-analyzer/frontend

# Node.jsの依存関係をインストール（初回のみ）
npm install

# 開発サーバーを起動
npm run dev -- --host
```

**期待される出力**:
```
  VITE v5.0.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/
```

### ステップ5: ブラウザでの動作確認

1. ブラウザで `http://localhost:5173` にアクセス
2. 「テニスサービス動作解析システム」のページが表示されることを確認
3. ファイル選択ボタンが正常に動作することを確認

## 🎬 デモ動画を使った完全テスト

### デモ動画の作成

```bash
# デモ動画作成スクリプトを実行
python create_demo_video.py
```

これにより `demo_tennis_serve.mp4` が作成されます。

### 解析テストの実行

1. ブラウザで `http://localhost:5173` にアクセス
2. 「ファイルを選択」をクリック
3. `demo_tennis_serve.mp4` を選択
4. 「解析開始」をクリック
5. 解析結果が表示されることを確認

**期待される結果**:
- 総合スコア: 6.0-8.0点
- 各フェーズのスコア表示
- アドバイス文の表示

## 🔧 統合テストスクリプト

### integration_test.py の実行

```bash
# 統合テストを実行
python integration_test.py
```

**期待される出力**:
```
🎾 Tennis Serve Analyzer - Integration Test
==========================================
✅ Backend server: Running
✅ Video processing: OK
✅ Pose detection: OK
✅ Motion analysis: OK
✅ Advice generation: OK
✅ API response: Valid JSON

Integration test completed successfully!
```

## ⚡ パフォーマンステスト

### 処理時間の計測

```python
# performance_test.py
import time
import requests

def test_analysis_performance():
    start_time = time.time()
    
    # デモ動画をAPIに送信
    with open('demo_tennis_serve.mp4', 'rb') as f:
        files = {'video': f}
        response = requests.post('http://localhost:5000/api/analyze', files=files)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"Processing time: {processing_time:.2f} seconds")
    
    if processing_time < 30:
        print("✅ Performance: Good")
    elif processing_time < 60:
        print("⚠️ Performance: Acceptable")
    else:
        print("❌ Performance: Slow")

if __name__ == "__main__":
    test_analysis_performance()
```

## 🚨 よくある問題と解決方法

### 問題1: サーバーが起動しない

**症状**: `python main.py` でエラーが発生

**解決方法**:
```bash
# 環境を確認
conda activate tennis-analyzer
which python

# 依存関係を再インストール
pip install -r requirements.txt
```

### 問題2: MediaPipeエラー

**症状**: `ImportError: No module named 'mediapipe'`

**解決方法**:
```bash
# MediaPipeを再インストール
pip uninstall mediapipe -y
pip install mediapipe==0.10.7
```

### 問題3: フロントエンドが起動しない

**症状**: `npm run dev` でエラー

**解決方法**:
```bash
# Node.jsのバージョンを確認
node --version

# 依存関係を再インストール
rm -rf node_modules package-lock.json
npm install
```

### 問題4: ブラウザでアクセスできない

**症状**: `ERR_CONNECTION_REFUSED`

**解決方法**:
1. バックエンドとフロントエンドの両方が起動していることを確認
2. ポート5000と5173が使用されていないことを確認
3. ファイアウォールの設定を確認

## 📊 動作確認チェックリスト

### 基本動作
- [ ] Python 3.11環境がアクティブ
- [ ] 必要なパッケージがすべてインストール済み
- [ ] バックエンドサーバーが起動
- [ ] フロントエンドサーバーが起動
- [ ] ブラウザでUIが表示

### 解析機能
- [ ] 動画ファイルのアップロード
- [ ] 動画の解析処理
- [ ] 結果の表示
- [ ] スコアの計算
- [ ] アドバイスの生成

### パフォーマンス
- [ ] 解析時間が60秒以内
- [ ] メモリ使用量が適切
- [ ] CPUの負荷が適切
- [ ] エラーが発生しない

## 🎯 次のステップ

動作確認が完了したら：

1. **実際の動画でテスト**: 自分のテニス動画で解析
2. **ChatGPT API設定**: より詳細なアドバイス機能
3. **カスタマイズ**: 解析パラメータの調整
4. **デプロイ**: 本番環境への展開

## 📞 サポート

問題が発生した場合は、以下の情報と一緒にお知らせください：

1. `test_conda.py` の実行結果
2. エラーメッセージの全文
3. `conda list` の出力
4. 実行環境の詳細（OS、Anacondaバージョンなど）

**これで確実にテニス解析ソフトが動作します！** 🚀

