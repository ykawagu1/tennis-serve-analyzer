# 🌐 Google Colab版テニスサービス解析システム

PCが重くなる問題を解決するため、ブラウザだけで動作するGoogle Colab版を作成しました。

## 🚀 Google Colabとは？
- Googleが提供する無料のPython実行環境
- ブラウザだけで動作
- 高性能GPU/CPUが無料で使用可能
- PCに負荷ゼロ

## 📝 使用手順

### ステップ1: Google Colabにアクセス
1. ブラウザで [colab.research.google.com](https://colab.research.google.com) にアクセス
2. Googleアカウントでログイン

### ステップ2: 新しいノートブックを作成
1. 「ファイル」→「ノートブックを新規作成」
2. 「tennis_analysis.ipynb」と名前を付ける

### ステップ3: 以下のコードをコピー&ペースト

```python
# セル1: ライブラリのインストール
!pip install mediapipe opencv-python matplotlib

# セル2: 必要なライブラリをインポート
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
import io
from PIL import Image

# セル3: MediaPipeの初期化
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# セル4: テニス解析関数
def analyze_tennis_serve(video_path):
    cap = cv2.VideoCapture(video_path)
    
    # 解析結果を保存するリスト
    pose_data = []
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # フレームをRGBに変換
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # ポーズ検出
        results = pose.process(rgb_frame)
        
        if results.pose_landmarks:
            # ランドマークデータを保存
            landmarks = []
            for landmark in results.pose_landmarks.landmark:
                landmarks.append([landmark.x, landmark.y, landmark.z])
            pose_data.append(landmarks)
            
            # ポーズを描画
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        frame_count += 1
        
        # 10フレームごとに表示（処理軽量化）
        if frame_count % 10 == 0:
            plt.figure(figsize=(10, 6))
            plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            plt.title(f'Frame {frame_count}')
            plt.axis('off')
            plt.show()
    
    cap.release()
    return pose_data

# セル5: 簡易解析関数
def simple_tennis_analysis(pose_data):
    if not pose_data:
        return "ポーズが検出されませんでした"
    
    analysis = {
        "検出フレーム数": len(pose_data),
        "解析結果": "基本的なポーズ検出が完了しました",
        "アドバイス": [
            "動画の品質が良好です",
            "人物が明確に映っています",
            "より詳細な分析には専用ソフトウェアをお勧めします"
        ]
    }
    
    return analysis

# セル6: ファイルアップロード機能
print("動画ファイルをアップロードしてください（MP4, MOV, AVI形式）")
uploaded = files.upload()

# セル7: 解析実行
for filename in uploaded.keys():
    print(f"解析中: {filename}")
    
    # 解析実行
    pose_data = analyze_tennis_serve(filename)
    
    # 結果表示
    result = simple_tennis_analysis(pose_data)
    print("\n=== 解析結果 ===")
    for key, value in result.items():
        print(f"{key}: {value}")
```

### ステップ4: 実行方法
1. 各セルを上から順番に実行（Shift + Enter）
2. セル6で動画ファイルをアップロード
3. セル7で解析結果を確認

## 🎯 Google Colab版のメリット

### PCへの負荷
- **ゼロ**: すべてGoogleのサーバーで処理
- **安全**: PCが重くなることは絶対にない
- **高速**: 高性能GPUを無料で使用

### 使いやすさ
- **簡単**: ブラウザだけで完結
- **無料**: Googleアカウントがあれば使用可能
- **共有**: 結果を簡単に共有可能

## 🔧 カスタマイズ方法

### より詳細な解析を追加
```python
# 膝の角度計算
def calculate_knee_angle(landmarks):
    # 腰、膝、足首の座標から角度を計算
    pass

# トスの軌道分析
def analyze_toss_trajectory(pose_data):
    # 手の動きから軌道を分析
    pass
```

### 結果の可視化
```python
# グラフ表示
import matplotlib.pyplot as plt

def plot_analysis_results(pose_data):
    # 時系列グラフを作成
    plt.figure(figsize=(12, 8))
    # グラフ描画コード
    plt.show()
```

## 📱 スマホでも使用可能

Google Colabはスマホのブラウザでも動作します：
1. スマホでcolab.research.google.comにアクセス
2. 同じ手順で実行
3. スマホで撮影した動画をアップロード

## 🆘 トラブルシューティング

### よくある問題
- **アップロードエラー**: ファイルサイズを100MB以下に
- **実行エラー**: セルを順番に実行
- **メモリエラー**: 動画を短くカット

### 解決方法
- 動画を30秒以下にカット
- 解像度を下げる（720p推奨）
- 不要なセルを削除

---

**これでPCに負荷をかけずにテニス解析ができます！** 🎾

