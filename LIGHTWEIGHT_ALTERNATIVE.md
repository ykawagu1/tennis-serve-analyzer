# 🎾 MediaPipeなし！軽量テニス解析システム

MediaPipeの依存問題を完全回避した、シンプルで軽量なテニス解析システムです。

## 🚀 MediaPipeを使わない理由

### 依存問題の実態
```
MediaPipe → protobuf (バージョン競合)
MediaPipe → numpy (バージョン競合)  
MediaPipe → OpenCV (バージョン競合)
MediaPipe → tensorflow (重すぎる)
```

### よくあるエラー
- `ImportError: cannot import name '_message'`
- `protobuf version conflict`
- `numpy version incompatible`
- メモリ不足エラー

## 💡 軽量代替案：OpenCV + 基本画像処理

### 必要なライブラリ（最小構成）
```python
# 軽量で安定したライブラリのみ
import cv2          # 画像処理（安定版）
import numpy as np  # 数値計算
import matplotlib.pyplot as plt  # グラフ表示
```

### インストール（問題なし）
```bash
pip install opencv-python matplotlib numpy
```

## 🔧 軽量テニス解析システム

### 基本的な動作解析
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

class SimpleTennisAnalyzer:
    def __init__(self):
        # 軽量な背景差分検出器
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()
        
    def analyze_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        
        results = {
            'total_frames': 0,
            'motion_frames': 0,
            'motion_intensity': [],
            'serve_phases': []
        }
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # 動作検出（MediaPipeなし）
            motion_mask = self.bg_subtractor.apply(frame)
            motion_pixels = cv2.countNonZero(motion_mask)
            
            results['total_frames'] += 1
            results['motion_intensity'].append(motion_pixels)
            
            if motion_pixels > 1000:  # 閾値
                results['motion_frames'] += 1
                
        cap.release()
        return results
    
    def analyze_serve_phases(self, motion_data):
        # 動作の強度から サービスフェーズを推定
        phases = []
        
        # 準備フェーズ: 動作が少ない
        # トス フェーズ: 動作が増加
        # インパクト: 動作が最大
        # フォロースルー: 動作が減少
        
        max_motion = max(motion_data)
        for i, motion in enumerate(motion_data):
            if motion < max_motion * 0.2:
                phases.append('準備')
            elif motion < max_motion * 0.6:
                phases.append('トス')
            elif motion < max_motion * 0.9:
                phases.append('加速')
            else:
                phases.append('インパクト')
                
        return phases
    
    def generate_advice(self, results):
        advice = []
        
        motion_ratio = results['motion_frames'] / results['total_frames']
        
        if motion_ratio < 0.3:
            advice.append("動作が小さすぎる可能性があります")
        elif motion_ratio > 0.8:
            advice.append("動作が大きすぎる可能性があります")
        else:
            advice.append("動作のバランスが良好です")
            
        avg_intensity = np.mean(results['motion_intensity'])
        if avg_intensity < 500:
            advice.append("もう少し大きな動作を心がけましょう")
        elif avg_intensity > 5000:
            advice.append("動作を少し抑えてみましょう")
        else:
            advice.append("動作の強度が適切です")
            
        return advice

# 使用例
def analyze_tennis_video(video_path):
    analyzer = SimpleTennisAnalyzer()
    
    print("動画を解析中...")
    results = analyzer.analyze_video(video_path)
    
    print("フェーズを分析中...")
    phases = analyzer.analyze_serve_phases(results['motion_intensity'])
    
    print("アドバイスを生成中...")
    advice = analyzer.generate_advice(results)
    
    # 結果表示
    print("\n=== 解析結果 ===")
    print(f"総フレーム数: {results['total_frames']}")
    print(f"動作フレーム数: {results['motion_frames']}")
    print(f"動作率: {results['motion_frames']/results['total_frames']*100:.1f}%")
    
    print("\n=== アドバイス ===")
    for i, tip in enumerate(advice, 1):
        print(f"{i}. {tip}")
    
    # グラフ表示
    plt.figure(figsize=(12, 6))
    plt.plot(results['motion_intensity'])
    plt.title('テニスサービス動作の強度変化')
    plt.xlabel('フレーム番号')
    plt.ylabel('動作強度')
    plt.grid(True)
    plt.show()
    
    return results, phases, advice
```

## 🎯 さらに軽量な手動解析版

### 完全手動版（依存関係ゼロ）
```python
# 標準ライブラリのみ使用
import json
import time

class ManualTennisAnalyzer:
    def __init__(self):
        self.analysis_data = {}
    
    def manual_input_analysis(self):
        print("=== 手動テニスサービス解析 ===")
        
        # ユーザーからの入力で解析
        serve_time = float(input("サービス全体の時間（秒）: "))
        toss_height = input("トスの高さ（低/中/高）: ")
        knee_bend = input("膝の曲がり（少/中/多）: ")
        elbow_position = input("肘の位置（低/中/高）: ")
        
        # 簡単なスコア計算
        score = self.calculate_simple_score(toss_height, knee_bend, elbow_position)
        advice = self.generate_manual_advice(serve_time, toss_height, knee_bend, elbow_position)
        
        return {
            'score': score,
            'advice': advice,
            'details': {
                'serve_time': serve_time,
                'toss_height': toss_height,
                'knee_bend': knee_bend,
                'elbow_position': elbow_position
            }
        }
    
    def calculate_simple_score(self, toss, knee, elbow):
        score = 0
        if toss == '中': score += 3
        elif toss in ['低', '高']: score += 2
        
        if knee == '中': score += 3
        elif knee in ['少', '多']: score += 2
        
        if elbow == '中': score += 3
        elif elbow in ['低', '高']: score += 2
        
        return min(score, 10)  # 10点満点
    
    def generate_manual_advice(self, time, toss, knee, elbow):
        advice = []
        
        if time < 1.0:
            advice.append("サービスが早すぎます。もう少しゆっくりと")
        elif time > 3.0:
            advice.append("サービスが遅すぎます。もう少しテンポよく")
        
        if toss == '低':
            advice.append("トスをもう少し高く上げましょう")
        elif toss == '高':
            advice.append("トスを少し低めにしてみましょう")
        
        if knee == '少':
            advice.append("膝をもう少し曲げてパワーを蓄えましょう")
        elif knee == '多':
            advice.append("膝の曲げすぎに注意しましょう")
        
        if elbow == '低':
            advice.append("肘をもう少し高い位置に保ちましょう")
        elif elbow == '高':
            advice.append("肘の位置を少し下げてみましょう")
        
        if not advice:
            advice.append("フォームが良好です！この調子で練習を続けましょう")
        
        return advice

# 使用例
analyzer = ManualTennisAnalyzer()
result = analyzer.manual_input_analysis()

print(f"\n=== 解析結果 ===")
print(f"総合スコア: {result['score']}/10")
print("\n=== アドバイス ===")
for i, tip in enumerate(result['advice'], 1):
    print(f"{i}. {tip}")
```

## 📱 スマホアプリ代替案

### 既存の軽量アプリ
```
1. Coach's Eye (iOS/Android)
   - 動画スロー再生
   - 簡単な線画ツール
   - 比較機能

2. Hudl Technique (無料)
   - 基本的な動作解析
   - フォーム比較
   - 簡単な測定

3. MyLift (無料)
   - 角度測定
   - 軌道描画
   - タイミング分析
```

## 🔧 Webベース軽量版

### HTML + JavaScript版
```html
<!DOCTYPE html>
<html>
<head>
    <title>簡単テニス解析</title>
</head>
<body>
    <h1>テニスサービス解析（軽量版）</h1>
    
    <div>
        <h3>フォーム評価</h3>
        <label>トスの高さ:</label>
        <select id="toss">
            <option value="low">低い</option>
            <option value="medium">適切</option>
            <option value="high">高い</option>
        </select><br><br>
        
        <label>膝の曲がり:</label>
        <select id="knee">
            <option value="little">少ない</option>
            <option value="medium">適切</option>
            <option value="much">多い</option>
        </select><br><br>
        
        <button onclick="analyze()">解析実行</button>
    </div>
    
    <div id="result"></div>
    
    <script>
        function analyze() {
            const toss = document.getElementById('toss').value;
            const knee = document.getElementById('knee').value;
            
            let score = 0;
            let advice = [];
            
            if (toss === 'medium') score += 5;
            else if (toss === 'low') advice.push('トスをもう少し高く');
            else advice.push('トスを少し低めに');
            
            if (knee === 'medium') score += 5;
            else if (knee === 'little') advice.push('膝をもう少し曲げて');
            else advice.push('膝の曲げすぎに注意');
            
            document.getElementById('result').innerHTML = 
                `<h3>結果</h3><p>スコア: ${score}/10</p><p>アドバイス: ${advice.join(', ')}</p>`;
        }
    </script>
</body>
</html>
```

## 💡 推奨する軽量アプローチ

### 1. 手動解析 + 既存アプリ
- 複雑な依存関係なし
- 確実に動作
- 学習効果も高い

### 2. 簡単なWebツール
- ブラウザだけで動作
- インストール不要
- 軽量で高速

### 3. スマホアプリの活用
- 専用設計で安定
- 使いやすいUI
- 追加機能も豊富

---

**MediaPipeの依存地獄を完全回避！どのアプローチがお好みですか？** 🎾

