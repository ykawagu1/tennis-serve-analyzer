"""
テニスサービス動作解析 - ポーズ検出サービス
MediaPipeを使用した人体ポーズ検出機能
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, List, Optional, Tuple
import json
import time


class PoseDetector:
    """MediaPipeを使用したポーズ検出クラス"""
    
    def __init__(self, 
                 model_complexity: int = 2,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        ポーズ検出器の初期化
        
        Args:
            model_complexity: モデルの複雑さ (0, 1, 2)
            min_detection_confidence: 検出の最小信頼度
            min_tracking_confidence: トラッキングの最小信頼度
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=model_complexity,
            enable_segmentation=False,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # テニスサービス解析に重要なランドマーク
        self.key_landmarks = {
            'nose': 0,
            'left_eye_inner': 1,
            'left_eye': 2,
            'left_eye_outer': 3,
            'right_eye_inner': 4,
            'right_eye': 5,
            'right_eye_outer': 6,
            'left_ear': 7,
            'right_ear': 8,
            'mouth_left': 9,
            'mouth_right': 10,
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_pinky': 17,
            'right_pinky': 18,
            'left_index': 19,
            'right_index': 20,
            'left_thumb': 21,
            'right_thumb': 22,
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28,
            'left_heel': 29,
            'right_heel': 30,
            'left_foot_index': 31,
            'right_foot_index': 32
        }
    
    def detect_pose(self, frame: np.ndarray, frame_number: int = 0, timestamp: float = 0.0) -> Dict:
        """
        単一フレームのポーズ検出
        
        Args:
            frame: 入力画像フレーム
            frame_number: フレーム番号
            timestamp: タイムスタンプ
            
        Returns:
            ポーズ検出結果の辞書
        """
        # BGRからRGBに変換
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # ポーズ検出実行
        results = self.pose.process(rgb_frame)
        
        # 結果を辞書形式で構造化
        pose_data = {
            'frame_number': frame_number,
            'timestamp': timestamp,
            'landmarks': {},
            'visibility_scores': {},
            'detection_confidence': 0.0,
            'has_pose': False
        }
        
        if results.pose_landmarks:
            pose_data['has_pose'] = True
            
            # 各ランドマークの座標と可視性を抽出
            for name, idx in self.key_landmarks.items():
                if idx < len(results.pose_landmarks.landmark):
                    landmark = results.pose_landmarks.landmark[idx]
                    pose_data['landmarks'][name] = {
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z,
                        'visibility': landmark.visibility
                    }
                    pose_data['visibility_scores'][name] = landmark.visibility
            
            # 全体的な検出信頼度を計算
            visible_landmarks = [v for v in pose_data['visibility_scores'].values() if v > 0.5]
            if visible_landmarks:
                pose_data['detection_confidence'] = sum(visible_landmarks) / len(visible_landmarks)
        
        return pose_data
    
    def process_video(self, video_path: str, output_path: Optional[str] = None) -> List[Dict]:
        """
        動画全体のポーズ検出処理
        
        Args:
            video_path: 入力動画ファイルパス
            output_path: 出力動画ファイルパス（オプション）
            
        Returns:
            全フレームのポーズ検出結果リスト
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"動画ファイルを開けません: {video_path}")
        
        # 動画情報取得
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"動画情報: {width}x{height}, {fps}fps, {frame_count}フレーム")
        
        # 出力動画の設定
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        pose_results = []
        frame_number = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                timestamp = frame_number / fps
                
                # ポーズ検出実行
                pose_data = self.detect_pose(frame, frame_number, timestamp)
                pose_results.append(pose_data)
                
                # 可視化（出力動画がある場合）
                if out is not None and pose_data['has_pose']:
                    annotated_frame = self._draw_pose_landmarks(frame, pose_data)
                    out.write(annotated_frame)
                elif out is not None:
                    out.write(frame)
                
                frame_number += 1
                
                # 進捗表示
                if frame_number % 30 == 0:
                    progress = (frame_number / frame_count) * 100
                    print(f"処理進捗: {progress:.1f}% ({frame_number}/{frame_count})")
        
        finally:
            cap.release()
            if out:
                out.release()
        
        print(f"ポーズ検出完了: {len(pose_results)}フレーム処理")
        return pose_results
    
    def _draw_pose_landmarks(self, frame: np.ndarray, pose_data: Dict) -> np.ndarray:
        """
        フレームにポーズランドマークを描画
        
        Args:
            frame: 入力フレーム
            pose_data: ポーズ検出結果
            
        Returns:
            ランドマークが描画されたフレーム
        """
        annotated_frame = frame.copy()
        
        if not pose_data['has_pose']:
            return annotated_frame
        
        # ランドマークを描画
        landmarks = pose_data['landmarks']
        height, width = frame.shape[:2]
        
        # 主要な関節を描画
        key_points = ['left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
                     'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
                     'left_knee', 'right_knee', 'left_ankle', 'right_ankle']
        
        for point_name in key_points:
            if point_name in landmarks:
                landmark = landmarks[point_name]
                if landmark['visibility'] > 0.5:
                    x = int(landmark['x'] * width)
                    y = int(landmark['y'] * height)
                    cv2.circle(annotated_frame, (x, y), 5, (0, 255, 0), -1)
        
        # 骨格線を描画
        connections = [
            ('left_shoulder', 'right_shoulder'),
            ('left_shoulder', 'left_elbow'),
            ('left_elbow', 'left_wrist'),
            ('right_shoulder', 'right_elbow'),
            ('right_elbow', 'right_wrist'),
            ('left_shoulder', 'left_hip'),
            ('right_shoulder', 'right_hip'),
            ('left_hip', 'right_hip'),
            ('left_hip', 'left_knee'),
            ('left_knee', 'left_ankle'),
            ('right_hip', 'right_knee'),
            ('right_knee', 'right_ankle')
        ]
        
        for start_point, end_point in connections:
            if (start_point in landmarks and end_point in landmarks and
                landmarks[start_point]['visibility'] > 0.5 and
                landmarks[end_point]['visibility'] > 0.5):
                
                start_x = int(landmarks[start_point]['x'] * width)
                start_y = int(landmarks[start_point]['y'] * height)
                end_x = int(landmarks[end_point]['x'] * width)
                end_y = int(landmarks[end_point]['y'] * height)
                
                cv2.line(annotated_frame, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)
        
        return annotated_frame
    
    def save_pose_data(self, pose_results: List[Dict], output_path: str):
        """
        ポーズ検出結果をJSONファイルに保存
        
        Args:
            pose_results: ポーズ検出結果リスト
            output_path: 出力ファイルパス
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(pose_results, f, indent=2, ensure_ascii=False)
        
        print(f"ポーズデータを保存しました: {output_path}")
    
    def load_pose_data(self, input_path: str) -> List[Dict]:
        """
        JSONファイルからポーズ検出結果を読み込み
        
        Args:
            input_path: 入力ファイルパス
            
        Returns:
            ポーズ検出結果リスト
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            pose_results = json.load(f)
        
        print(f"ポーズデータを読み込みました: {input_path}")
        return pose_results
    
    def get_pose_statistics(self, pose_results: List[Dict]) -> Dict:
        """
        ポーズ検出結果の統計情報を取得
        
        Args:
            pose_results: ポーズ検出結果リスト
            
        Returns:
            統計情報の辞書
        """
        total_frames = len(pose_results)
        detected_frames = sum(1 for result in pose_results if result['has_pose'])
        
        if detected_frames == 0:
            return {
                'total_frames': total_frames,
                'detected_frames': 0,
                'detection_rate': 0.0,
                'average_confidence': 0.0,
                'landmark_visibility': {}
            }
        
        # 平均信頼度計算
        total_confidence = sum(result['detection_confidence'] for result in pose_results if result['has_pose'])
        average_confidence = total_confidence / detected_frames
        
        # ランドマーク可視性統計
        landmark_visibility = {}
        for landmark_name in self.key_landmarks.keys():
            visible_count = 0
            total_visibility = 0.0
            
            for result in pose_results:
                if result['has_pose'] and landmark_name in result['landmarks']:
                    visibility = result['landmarks'][landmark_name]['visibility']
                    if visibility > 0.5:
                        visible_count += 1
                    total_visibility += visibility
            
            if detected_frames > 0:
                landmark_visibility[landmark_name] = {
                    'visible_rate': visible_count / detected_frames,
                    'average_visibility': total_visibility / detected_frames
                }
        
        return {
            'total_frames': total_frames,
            'detected_frames': detected_frames,
            'detection_rate': detected_frames / total_frames,
            'average_confidence': average_confidence,
            'landmark_visibility': landmark_visibility
        }


def main():
    """テスト用のメイン関数"""
    detector = PoseDetector()
    
    # テスト用の動画ファイルがある場合の処理例
    test_video_path = "/path/to/test_video.mov"
    
    try:
        # ポーズ検出実行
        pose_results = detector.process_video(test_video_path, "output_with_pose.mp4")
        
        # 結果保存
        detector.save_pose_data(pose_results, "pose_data.json")
        
        # 統計情報表示
        stats = detector.get_pose_statistics(pose_results)
        print("ポーズ検出統計:")
        print(f"総フレーム数: {stats['total_frames']}")
        print(f"検出フレーム数: {stats['detected_frames']}")
        print(f"検出率: {stats['detection_rate']:.2%}")
        print(f"平均信頼度: {stats['average_confidence']:.3f}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()

