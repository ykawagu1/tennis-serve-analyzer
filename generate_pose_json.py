"""
動画からポーズ検出結果(JSON)を生成
"""

import os
import sys
import json
from pathlib import Path

# === PoseDetectorをインポート ===
# pose_detector.py が backend/app/services にある場合
services_path = Path(__file__).resolve().parent / "backend/app/services"
sys.path.append(str(services_path))

from pose_detector import PoseDetector

# === 入力と出力のパス ===
input_video = r"C:\Users\kumon\OneDrive\デスクトップ\IMG_1820.MOV"
output_json = r"C:\Users\kumon\OneDrive\デスクトップ\pose_results.json"

# === PoseDetector初期化 ===
detector = PoseDetector()

print(f"✅ 動画解析を開始: {input_video}")

# === 動画からポーズ検出 ===
pose_results = detector.process_video(input_video)

# === 人が検出されなかったフレームを除外 ===
filtered_results = [frame for frame in pose_results if frame.get("has_pose")]

print(f"📄 総フレーム数: {len(pose_results)}")
print(f"🙋 人が検出されたフレーム数: {len(filtered_results)}")

# === JSONに保存 ===
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(filtered_results, f, indent=2, ensure_ascii=False)

print(f"✅ ポーズ検出結果を保存: {output_json}")
