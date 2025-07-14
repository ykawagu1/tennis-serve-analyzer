"""
テニスサービス動作解析 - ポーズ検出サービス（detect_posesメソッド追加版）
MediaPipeを使用した人体ポーズ検出機能
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, List, Optional, Tuple
import json
import time
import os


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
    
    def detect_poses(self, video_path: str, output_dir: str) -> List[Dict]:
        """
        動画からポーズを検出（main.pyから呼び出されるメインメソッド）
        
        Args:
            video_path: 入力動画ファイルパス
            output_dir: 出力ディレクトリ
            
        Returns:
            全フレームのポーズ検出結果リスト
        """
        try:
            print(f"ポーズ検出開始: {video_path}")
            
            # 出力ファイルパスを決定
            output_video_path = os.path.join(output_dir, f"pose_detected_{int(time.time())}.mp4")
            output_json_path = os.path.join(output_dir, f"pose_data_{int(time.time())}.json")
            
            # 動画全体のポーズ検出を実行
            pose_results = self.process_video(video_path, output_video_path)
            
            # 結果をJSONファイルに保存
            self.save_pose_data(pose_results, output_json_path)
            
            print(f"ポーズ検出完了: {len(pose_results)}フレーム処理")
            print(f"出力動画: {output_video_path}")
            print(f"出力データ: {output_json_path}")
            
            return pose_results
            
        except Exception as e:
            print(f"ポーズ検出エラー: {e}")
            # エラーの場合は空のリストを返す（フォールバック）
            return []
    
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
            
            # ランドマークデータを抽出
            for landmark_name, landmark_idx in self.key_landmarks.items():
                if landmark_idx < len(results.pose_landmarks.landmark):
                    landmark = results.pose_landmarks.landmark[landmark_idx]
                    pose_data['landmarks'][landmark_name] = {
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    }
                    pose_data['visibility_scores'][landmark_name] = landmark.visibility
            
            # 検出信頼度の計算（可視性スコアの平均）
            if pose_data['visibility_scores']:
                pose_data['detection_confidence'] = np.mean(list(pose_data['visibility_scores'].values()))
        
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
            print(f"=== ポーズ検出開始 ===")
            print(f"動画ファイル: {video_path}")
            print(f"MediaPipe初期化状況: {self.pose is not None}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                timestamp = frame_number / fps
                
                # ポーズ検出実行
                try:
                    pose_data = self.detect_pose(frame, frame_number, timestamp)
                except Exception as e:
                    print(f"フレーム {frame_number}: detect_poseでエラー - {e}")
                    pose_data = {
                        'frame_number': frame_number,
                        'timestamp': timestamp,
                        'landmarks': {},
                        'visibility_scores': {},
                        'detection_confidence': 0.0,
                        'has_pose': False
                    }
                
                pose_results.append(pose_data)
                
                # ポーズ描画（出力動画がある場合）
                if out is not None:
                    annotated_frame = self._draw_pose_landmarks(frame, pose_data)
                    out.write(annotated_frame)
                
                frame_number += 1
                
                # 進捗表示
                if frame_number % 30 == 0:
                    progress = (frame_number / frame_count) * 100
                    detected_count = sum(1 for p in pose_results if p['has_pose'])
                    print(f"ポーズ検出進捗: {progress:.1f}% ({frame_number}/{frame_count}) - 検出成功: {detected_count}")
                
        finally:
            cap.release()
            if out is not None:
                out.release()
        
        # 統計情報を表示
        detected_count = sum(1 for p in pose_results if p['has_pose'])
        detection_rate = (detected_count / len(pose_results)) * 100 if pose_results else 0
        
        print(f"=== ポーズ検出完了 ===")
        print(f"総フレーム数: {len(pose_results)}")
        print(f"検出成功フレーム: {detected_count}")
        print(f"検出成功率: {detection_rate:.1f}%")
        
        return pose_results
    
    def _draw_pose_landmarks(self, frame: np.ndarray, pose_data: Dict) -> np.ndarray:
        """
        フレームにポーズランドマークを描画
        
        Args:
            frame: 入力フレーム
            pose_data: ポーズデータ
            
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
                x = int(landmark['x'] * width)
                y = int(landmark['y'] * height)
                
                # 可視性に基づいて色を決定
                visibility = pose_data['visibility_scores'].get(point_name, 0)
                if visibility > 0.5:
                    color = (0, 255, 0)  # 緑（高可視性）
                elif visibility > 0.3:
                    color = (0, 255, 255)  # 黄（中可視性）
                else:
                    color = (0, 0, 255)  # 赤（低可視性）
                
                cv2.circle(annotated_frame, (x, y), 5, color, -1)
        
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
            if start_point in landmarks and end_point in landmarks:
                start_landmark = landmarks[start_point]
                end_landmark = landmarks[end_point]
                
                start_x = int(start_landmark['x'] * width)
                start_y = int(start_landmark['y'] * height)
                end_x = int(end_landmark['x'] * width)
                end_y = int(end_landmark['y'] * height)
                
                cv2.line(annotated_frame, (start_x, start_y), (end_x, end_y), (255, 255, 255), 2)
        
        # 検出信頼度を表示
        confidence = pose_data['detection_confidence']
        cv2.putText(annotated_frame, f'Confidence: {confidence:.2f}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
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
        
        print(f"ポーズデータ保存完了: {output_path}")
    
    def load_pose_data(self, input_path: str) -> List[Dict]:
        """
        JSONファイルからポーズデータを読み込み
        
        Args:
            input_path: 入力ファイルパス
            
        Returns:
            ポーズ検出結果リスト
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            pose_results = json.load(f)
        
        print(f"ポーズデータ読み込み完了: {len(pose_results)}フレーム")
        return pose_results
    
    def get_pose_statistics(self, pose_results: List[Dict]) -> Dict:
        """
        ポーズ検出結果の統計情報を取得
        
        Args:
            pose_results: ポーズ検出結果リスト
            
        Returns:
            統計情報の辞書
        """
        if not pose_results:
            return {}
        
        total_frames = len(pose_results)
        detected_frames = sum(1 for p in pose_results if p['has_pose'])
        detection_rate = (detected_frames / total_frames) * 100
        
        # 信頼度の統計
        confidences = [p['detection_confidence'] for p in pose_results if p['has_pose']]
        avg_confidence = np.mean(confidences) if confidences else 0
        max_confidence = np.max(confidences) if confidences else 0
        min_confidence = np.min(confidences) if confidences else 0
        
        # ランドマーク検出率
        landmark_detection_rates = {}
        for landmark_name in self.key_landmarks.keys():
            detected_count = sum(1 for p in pose_results 
                               if p['has_pose'] and landmark_name in p['landmarks'])
            landmark_detection_rates[landmark_name] = (detected_count / detected_frames) * 100 if detected_frames > 0 else 0
        
        return {
            'total_frames': total_frames,
            'detected_frames': detected_frames,
            'detection_rate': detection_rate,
            'confidence_stats': {
                'average': avg_confidence,
                'maximum': max_confidence,
                'minimum': min_confidence
            },
            'landmark_detection_rates': landmark_detection_rates,
            'duration': pose_results[-1]['timestamp'] if pose_results else 0
        }
    
    def __del__(self):
        """デストラクタ - MediaPipeリソースのクリーンアップ"""
        if hasattr(self, 'pose') and self.pose:
            self.pose.close()


def main():
    """テスト用のメイン関数"""
    detector = PoseDetector()
    
    # テスト動画パス（実際のファイルパスに変更してください）
    test_video = "test_video.mp4"
    output_dir = "output"
    
    if os.path.exists(test_video):
        os.makedirs(output_dir, exist_ok=True)
        
        # ポーズ検出実行
        pose_results = detector.detect_poses(test_video, output_dir)
        
        # 統計情報表示
        stats = detector.get_pose_statistics(pose_results)
        print("統計情報:", json.dumps(stats, indent=2, ensure_ascii=False))
    else:
        print(f"テスト動画が見つかりません: {test_video}")


if __name__ == "__main__":
    main()

