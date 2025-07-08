import os
import cv2
import numpy as np
from pathlib import Path
import sys

# PoseDetector を正しいパスからインポート
sys.path.append(str(Path(__file__).resolve().parent / "backend" / "app" / "services"))
from pose_detector import PoseDetector

# 入出力パス設定
VIDEO_PATH = r"C:\Users\kumon\OneDrive\デスクトップ\IMG_1820.MOV"  # 🎥 入力動画
OUTPUT_DIR = Path(r"C:\Users\kumon\tennis-serve-analyzer\temp\pose_images")  # 🖼️ 出力画像フォルダ
POSE_JSON_PATH = Path(r"C:\Users\kumon\tennis-serve-analyzer\temp\pose_results.json")  # 📝 一時保存JSON

# フォルダ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# PoseDetector 初期化
detector = PoseDetector()

# 動画からポーズ検出してJSON保存
print("🎯 動画からポーズ検出を開始します...")
pose_results = detector.process_video(VIDEO_PATH)
detector.save_pose_data(pose_results, str(POSE_JSON_PATH))

# -------------------------------
# ✋ 利き手自動判定
# -------------------------------
right_hand_raised = 0
left_hand_raised = 0

for result in pose_results:
    if result["has_pose"]:
        rw = result["landmarks"].get("right_wrist", {})
        lw = result["landmarks"].get("left_wrist", {})
        rs = result["landmarks"].get("right_shoulder", {})
        ls = result["landmarks"].get("left_shoulder", {})

        if all([rw, rs]) and rw["y"] < rs["y"]:
            right_hand_raised += 1
        if all([lw, ls]) and lw["y"] < ls["y"]:
            left_hand_raised += 1

# 利き手判定
if right_hand_raised >= left_hand_raised:
    dominant_hand = "right"
    print("🟢 利き手判定: **右利き**")
else:
    dominant_hand = "left"
    print("🟢 利き手判定: **左利き**")

# -------------------------------
# 🎾 トロフィーポーズ検出
# -------------------------------
candidate_frames = []
for result in pose_results:
    if result["has_pose"]:
        # 利き手に応じたランドマーク選択
        wrist = result["landmarks"].get(f"{dominant_hand}_wrist", {})
        elbow = result["landmarks"].get(f"{dominant_hand}_elbow", {})
        shoulder = result["landmarks"].get(f"{dominant_hand}_shoulder", {})
        if all([wrist, elbow, shoulder]):
            # トロフィーポーズの特徴: 肘・手首が肩より高い
            if (elbow["y"] < shoulder["y"]) and (wrist["y"] < shoulder["y"]):
                candidate_frames.append((result["frame_number"], wrist["y"]))

if candidate_frames:
    # 手首が最も高いフレームをトロフィーポーズとする
    candidate_frames.sort(key=lambda x: x[1])
    trophy_frame = candidate_frames[0][0]
    print(f"🏆 トロフィーポーズ検出: フレーム {trophy_frame}")

    # 前後で3枚選択
    start_frame = max(trophy_frame - 15, 0)
    end_frame = min(trophy_frame + 30, len(pose_results) - 1)
    frame_indices = [start_frame, trophy_frame, end_frame]
else:
    print("⚠️ トロフィーポーズ検出失敗: 均等3枚を使用")
    # 保険として均等3枚
    frame_indices = np.linspace(0, len(pose_results) - 1, num=3, dtype=int)

# -------------------------------
# 🎨 画像保存処理
# -------------------------------
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise IOError(f"動画を開けません: {VIDEO_PATH}")

saved_images = []
for idx, frame_no in enumerate(frame_indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret:
        print(f"❌ フレーム読み込み失敗: フレーム番号 {frame_no}")
        continue

    # オーバーレイ描画
    pose_data = pose_results[frame_no]
    annotated_frame = detector._draw_pose_landmarks(frame, pose_data)

    # 画像保存
    filename = f"pose_{idx:03d}.jpg"
    save_path = OUTPUT_DIR / filename
    success = cv2.imwrite(str(save_path), annotated_frame)
    if success:
        print(f"✅ 保存成功: {save_path}")
        saved_images.append(save_path)
    else:
        print(f"❌ 保存失敗: {save_path}")

cap.release()

print(f"\n🎉 完了: 合計 {len(saved_images)} 枚のオーバーレイ画像を保存しました。")
print(f"📂 保存フォルダ: {OUTPUT_DIR}")
