#!/usr/bin/env python3
"""
デモ用テニスサービス動画作成スクリプト
より現実的な人体シルエットでMediaPipeが検出可能な動画を作成
"""

import cv2
import numpy as np
import math

def create_realistic_tennis_serve_video():
    """より現実的なテニスサービス動画を作成"""
    
    # 動画パラメータ
    width, height = 1280, 720
    fps = 30
    duration = 6  # 6秒
    total_frames = fps * duration
    
    output_path = "demo_tennis_serve.mp4"
    
    # 動画ライター設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"デモ用テニス動画作成中: {output_path}")
    
    # 背景色（テニスコート風）
    court_color = (34, 139, 34)  # 緑
    line_color = (255, 255, 255)  # 白
    
    try:
        for frame_num in range(total_frames):
            # 背景作成
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame[:] = court_color
            
            # コートライン描画
            cv2.line(frame, (0, height//2), (width, height//2), line_color, 3)
            cv2.line(frame, (width//2, 0), (width//2, height), line_color, 2)
            
            # サーブ動作の進行度
            progress = frame_num / total_frames
            
            # プレイヤーの基本位置
            player_x = width // 4
            player_y = height // 2 + 100
            
            # サーブフェーズの定義
            if progress < 0.15:  # 準備フェーズ
                phase = "preparation"
                arm_angle = -30
                knee_bend = 0
                toss_height = 0
                body_lean = 0
            elif progress < 0.35:  # トスフェーズ
                phase = "toss"
                phase_progress = (progress - 0.15) / 0.2
                arm_angle = -30 + phase_progress * 60
                knee_bend = phase_progress * 15
                toss_height = phase_progress * 120
                body_lean = phase_progress * 10
            elif progress < 0.5:  # トロフィーポジション
                phase = "trophy"
                phase_progress = (progress - 0.35) / 0.15
                arm_angle = 30 + phase_progress * 60
                knee_bend = 15 + phase_progress * 25
                toss_height = 120 - phase_progress * 20
                body_lean = 10 + phase_progress * 15
            elif progress < 0.7:  # 加速フェーズ
                phase = "acceleration"
                phase_progress = (progress - 0.5) / 0.2
                arm_angle = 90 + phase_progress * 90
                knee_bend = 40 - phase_progress * 30
                toss_height = 100 - phase_progress * 80
                body_lean = 25 + phase_progress * 10
            elif progress < 0.85:  # インパクト
                phase = "contact"
                phase_progress = (progress - 0.7) / 0.15
                arm_angle = 180 + phase_progress * 30
                knee_bend = 10 - phase_progress * 5
                toss_height = 20 - phase_progress * 20
                body_lean = 35 - phase_progress * 5
            else:  # フォロースルー
                phase = "follow_through"
                phase_progress = (progress - 0.85) / 0.15
                arm_angle = 210 + phase_progress * 60
                knee_bend = 5 - phase_progress * 5
                toss_height = 0
                body_lean = 30 - phase_progress * 20
            
            # 人体の描画（より詳細で現実的）
            draw_realistic_player(frame, player_x, player_y, arm_angle, knee_bend, body_lean, toss_height)
            
            # フェーズ情報表示
            cv2.putText(frame, f"Phase: {phase}", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Frame: {frame_num}/{total_frames}", (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            out.write(frame)
            
            # 進捗表示
            if frame_num % 30 == 0:
                print(f"進捗: {(frame_num / total_frames) * 100:.1f}%")
    
    finally:
        out.release()
    
    print(f"デモ動画作成完了: {output_path}")
    return output_path


def draw_realistic_player(frame, center_x, center_y, arm_angle, knee_bend, body_lean, toss_height):
    """より現実的な人体を描画"""
    
    # 色設定
    body_color = (200, 180, 160)  # 肌色
    clothes_color = (100, 100, 255)  # 青いウェア
    hair_color = (50, 50, 50)  # 髪
    
    # 体の傾き調整
    lean_offset_x = int(body_lean * 2)
    lean_offset_y = int(body_lean * 0.5)
    
    # 頭部
    head_x = center_x + lean_offset_x
    head_y = center_y - 120 + lean_offset_y
    cv2.circle(frame, (head_x, head_y), 25, body_color, -1)
    cv2.circle(frame, (head_x, head_y), 25, (0, 0, 0), 2)
    
    # 髪
    cv2.ellipse(frame, (head_x, head_y - 10), (30, 20), 0, 180, 360, hair_color, -1)
    
    # 顔の特徴
    cv2.circle(frame, (head_x - 8, head_y - 5), 3, (0, 0, 0), -1)  # 左目
    cv2.circle(frame, (head_x + 8, head_y - 5), 3, (0, 0, 0), -1)  # 右目
    cv2.ellipse(frame, (head_x, head_y + 5), (8, 5), 0, 0, 180, (0, 0, 0), 2)  # 口
    
    # 首
    neck_x = center_x + lean_offset_x
    neck_y = center_y - 95 + lean_offset_y
    cv2.line(frame, (head_x, head_y + 25), (neck_x, neck_y), body_color, 8)
    
    # 胴体
    torso_x = center_x + lean_offset_x
    torso_y = center_y - 20 + lean_offset_y
    cv2.ellipse(frame, (torso_x, (neck_y + torso_y) // 2), (35, 40), 0, 0, 360, clothes_color, -1)
    cv2.ellipse(frame, (torso_x, (neck_y + torso_y) // 2), (35, 40), 0, 0, 360, (0, 0, 0), 2)
    
    # 腰
    hip_x = center_x + lean_offset_x // 2
    hip_y = center_y + 20
    cv2.ellipse(frame, (hip_x, hip_y), (30, 20), 0, 0, 360, clothes_color, -1)
    
    # 右腕（サーブ腕）
    shoulder_x = torso_x + 25
    shoulder_y = neck_y + 20
    
    # 上腕
    arm_length = 50
    elbow_x = shoulder_x + int(arm_length * 0.6 * math.cos(math.radians(arm_angle)))
    elbow_y = shoulder_y + int(arm_length * 0.6 * math.sin(math.radians(arm_angle)))
    cv2.line(frame, (shoulder_x, shoulder_y), (elbow_x, elbow_y), body_color, 12)
    cv2.circle(frame, (shoulder_x, shoulder_y), 8, body_color, -1)
    cv2.circle(frame, (elbow_x, elbow_y), 6, body_color, -1)
    
    # 前腕
    forearm_angle = arm_angle + 30 if arm_angle < 90 else arm_angle - 30
    hand_x = elbow_x + int(arm_length * 0.7 * math.cos(math.radians(forearm_angle)))
    hand_y = elbow_y + int(arm_length * 0.7 * math.sin(math.radians(forearm_angle)))
    cv2.line(frame, (elbow_x, elbow_y), (hand_x, hand_y), body_color, 10)
    cv2.circle(frame, (hand_x, hand_y), 8, body_color, -1)
    
    # ラケット
    racket_length = 40
    racket_end_x = hand_x + int(racket_length * math.cos(math.radians(forearm_angle)))
    racket_end_y = hand_y + int(racket_length * math.sin(math.radians(forearm_angle)))
    cv2.line(frame, (hand_x, hand_y), (racket_end_x, racket_end_y), (139, 69, 19), 4)
    cv2.ellipse(frame, (racket_end_x, racket_end_y), (15, 20), forearm_angle, 0, 360, (255, 255, 255), 2)
    
    # 左腕（トス腕）
    left_shoulder_x = torso_x - 25
    left_shoulder_y = neck_y + 20
    
    toss_arm_angle = -60 if toss_height > 0 else -30
    left_elbow_x = left_shoulder_x + int(40 * math.cos(math.radians(toss_arm_angle)))
    left_elbow_y = left_shoulder_y + int(40 * math.sin(math.radians(toss_arm_angle)))
    cv2.line(frame, (left_shoulder_x, left_shoulder_y), (left_elbow_x, left_elbow_y), body_color, 12)
    cv2.circle(frame, (left_shoulder_x, left_shoulder_y), 8, body_color, -1)
    cv2.circle(frame, (left_elbow_x, left_elbow_y), 6, body_color, -1)
    
    left_hand_x = left_elbow_x + int(35 * math.cos(math.radians(toss_arm_angle - 20)))
    left_hand_y = left_elbow_y + int(35 * math.sin(math.radians(toss_arm_angle - 20)))
    cv2.line(frame, (left_elbow_x, left_elbow_y), (left_hand_x, left_hand_y), body_color, 10)
    cv2.circle(frame, (left_hand_x, left_hand_y), 8, body_color, -1)
    
    # 脚部
    # 右脚
    right_knee_x = hip_x + 15
    right_knee_y = hip_y + 40 + int(knee_bend)
    right_foot_x = right_knee_x + 10
    right_foot_y = center_y + 120
    
    cv2.line(frame, (hip_x + 10, hip_y + 10), (right_knee_x, right_knee_y), body_color, 14)
    cv2.line(frame, (right_knee_x, right_knee_y), (right_foot_x, right_foot_y), body_color, 12)
    cv2.circle(frame, (right_knee_x, right_knee_y), 8, body_color, -1)
    cv2.ellipse(frame, (right_foot_x, right_foot_y), (20, 8), 0, 0, 360, (0, 0, 0), -1)
    
    # 左脚
    left_knee_x = hip_x - 15
    left_knee_y = hip_y + 40 + int(knee_bend * 0.7)
    left_foot_x = left_knee_x - 5
    left_foot_y = center_y + 120
    
    cv2.line(frame, (hip_x - 10, hip_y + 10), (left_knee_x, left_knee_y), body_color, 14)
    cv2.line(frame, (left_knee_x, left_knee_y), (left_foot_x, left_foot_y), body_color, 12)
    cv2.circle(frame, (left_knee_x, left_knee_y), 8, body_color, -1)
    cv2.ellipse(frame, (left_foot_x, left_foot_y), (20, 8), 0, 0, 360, (0, 0, 0), -1)
    
    # ボール（トス中）
    if toss_height > 0:
        ball_x = left_hand_x - 20
        ball_y = left_hand_y - int(toss_height)
        cv2.circle(frame, (ball_x, ball_y), 8, (0, 255, 255), -1)
        cv2.circle(frame, (ball_x, ball_y), 8, (0, 0, 0), 2)


def main():
    """メイン関数"""
    try:
        video_path = create_realistic_tennis_serve_video()
        print(f"\n✅ デモ動画が作成されました: {video_path}")
        print("この動画を使用してシステムをテストできます。")
        
        # 動画情報表示
        cap = cv2.VideoCapture(video_path)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            
            print(f"\n動画情報:")
            print(f"  解像度: {width}x{height}")
            print(f"  フレームレート: {fps}fps")
            print(f"  時間: {duration:.1f}秒")
            print(f"  フレーム数: {frame_count}")
            
            cap.release()
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")


if __name__ == "__main__":
    main()

