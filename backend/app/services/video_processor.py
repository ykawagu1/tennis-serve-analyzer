"""
テニスサービス動作解析 - 動画処理サービス
動画ファイルの読み込み、検証、前処理機能
"""

import cv2
import numpy as np
import os
import tempfile
import shutil
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path
import json
import time


class VideoProcessor:
    """動画処理クラス"""
    
    def __init__(self, max_file_size: int = 100 * 1024 * 1024):  # 100MB
        """
        動画処理器の初期化
        
        Args:
            max_file_size: 最大ファイルサイズ（バイト）
        """
        self.supported_formats = ['.mov', '.mp4', '.avi', '.mkv', '.wmv']
        self.max_file_size = max_file_size
        self.temp_dir = tempfile.mkdtemp(prefix='tennis_analyzer_')
        
        # 動画品質設定
        #最高精度
        #self.target_fps = 30
        #self.target_resolution = (1280, 720)  # HD解像度
        self.max_duration = 30  # 最大30秒
        #以下が軽量化版
        self.target_fps = 20
        self.target_resolution = (960, 540)

    def __del__(self):
        """デストラクタ - 一時ディレクトリのクリーンアップ"""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def validate_video(self, file_path: str) -> Dict[str, Union[bool, str, Dict]]:
        """
        動画ファイルの検証
        
        Args:
            file_path: 動画ファイルパス
            
        Returns:
            検証結果の辞書
        """
        validation_result = {
            'is_valid': False,
            'error_message': '',
            'warnings': [],
            'metadata': {}
        }
        
        try:
            # ファイル存在確認
            if not os.path.exists(file_path):
                validation_result['error_message'] = 'ファイルが存在しません'
                return validation_result
            
            # ファイルサイズ確認
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                validation_result['error_message'] = f'ファイルサイズが大きすぎます（最大: {self.max_file_size // (1024*1024)}MB）'
                return validation_result
            
            # ファイル拡張子確認
            file_extension = Path(file_path).suffix.lower()
            if file_extension not in self.supported_formats:
                validation_result['error_message'] = f'サポートされていないファイル形式です（対応形式: {", ".join(self.supported_formats)}）'
                return validation_result
            
            # 動画メタデータ取得
            metadata = self.get_video_metadata(file_path)
            if not metadata:
                validation_result['error_message'] = '動画ファイルを読み込めません'
                return validation_result
            
            validation_result['metadata'] = metadata
            
            # 動画時間確認
            if metadata['duration'] > self.max_duration:
                validation_result['warnings'].append(f'動画が長すぎます（推奨: {self.max_duration}秒以下）')
            
            # 解像度確認
            if metadata['width'] < 640 or metadata['height'] < 480:
                validation_result['warnings'].append('解像度が低すぎる可能性があります（推奨: 640x480以上）')
            
            # フレームレート確認
            if metadata['fps'] < 15:
                validation_result['warnings'].append('フレームレートが低すぎる可能性があります（推奨: 15fps以上）')
            
            # フレーム数確認
            if metadata['frame_count'] < 30:
                validation_result['warnings'].append('動画が短すぎる可能性があります（推奨: 1秒以上）')
            
            validation_result['is_valid'] = True
            return validation_result
            
        except Exception as e:
            validation_result['error_message'] = f'検証中にエラーが発生しました: {str(e)}'
            return validation_result
    
    def get_video_metadata(self, file_path: str) -> Optional[Dict]:
        """
        動画メタデータの取得
        
        Args:
            file_path: 動画ファイルパス
            
        Returns:
            メタデータの辞書、エラー時はNone
        """
        try:
            cap = cv2.VideoCapture(file_path)
            
            if not cap.isOpened():
                return None
            
            # 基本情報取得
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                'width': width,
                'height': height,
                'fps': fps,
                'frame_count': frame_count,
                'duration': duration,
                'file_size': os.path.getsize(file_path),
                'format': Path(file_path).suffix.lower()
            }
            
        except Exception as e:
            print(f"メタデータ取得エラー: {e}")
            return None
    #高精度版
    #def extract_frames(self, video_path: str, max_frames: int = 300) -> List[np.ndarray]:
    #以下軽量化版
    def extract_frames(self, video_path: str, max_frames: int = 200) -> List[np.ndarray]:
    
        """
        動画からフレームを抽出
        
        Args:
            video_path: 動画ファイルパス
            max_frames: 最大フレーム数
            
        Returns:
            フレームのリスト
        """
        frames = []
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"動画ファイルを開けません: {video_path}")
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # フレーム間隔を計算（最大フレーム数に収まるように）
            if total_frames <= max_frames:
                frame_interval = 1
            else:
                frame_interval = total_frames // max_frames
            
            frame_index = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_index % frame_interval == 0:
                    frames.append(frame)
                    
                    if len(frames) >= max_frames:
                        break
                
                frame_index += 1
            
            cap.release()
            
        except Exception as e:
            print(f"フレーム抽出エラー: {e}")
            return []
        
        print(f"フレーム抽出完了: {len(frames)}フレーム")
        return frames
    
    def preprocess_video(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        動画の前処理（リサイズ、フレームレート調整など）
        
        Args:
            video_path: 入力動画ファイルパス
            output_path: 出力動画ファイルパス、Noneの場合は一時ファイル
            
        Returns:
            前処理済み動画ファイルパス
        """
        if output_path is None:
            output_path = os.path.join(self.temp_dir, f"preprocessed_{int(time.time())}.mp4")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"動画ファイルを開けません: {video_path}")
        
        # 元の動画情報取得
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        
        # 出力設定決定
        output_width, output_height = self._calculate_output_resolution(original_width, original_height)
        output_fps = min(original_fps, self.target_fps)
        
        # 動画ライター設定
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, output_fps, (output_width, output_height))
        
        try:
            frame_count = 0
            max_frames = int(output_fps * self.max_duration)  # 最大フレーム数
            
            while True:
                ret, frame = cap.read()
                if not ret or frame_count >= max_frames:
                    break
                
                # フレームリサイズ
                if (original_width, original_height) != (output_width, output_height):
                    frame = cv2.resize(frame, (output_width, output_height))
                
                out.write(frame)
                frame_count += 1
            
        finally:
            cap.release()
            out.release()
        
        return output_path
    
    def _calculate_output_resolution(self, width: int, height: int) -> Tuple[int, int]:
        """
        出力解像度の計算
        
        Args:
            width: 元の幅
            height: 元の高さ
            
        Returns:
            出力解像度のタプル (width, height)
        """
        target_width, target_height = self.target_resolution
        
        # アスペクト比を維持しながらリサイズ
        aspect_ratio = width / height
        target_aspect_ratio = target_width / target_height
        
        if aspect_ratio > target_aspect_ratio:
            # 横長の場合、幅を基準にリサイズ
            output_width = target_width
            output_height = int(target_width / aspect_ratio)
        else:
            # 縦長の場合、高さを基準にリサイズ
            output_height = target_height
            output_width = int(target_height * aspect_ratio)
        
        # 偶数に調整（動画エンコーディングの要件）
        output_width = output_width - (output_width % 2)
        output_height = output_height - (output_height % 2)
        
        return output_width, output_height
    
    def cleanup(self):
        """一時ファイルのクリーンアップ"""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)


# テスト用のメイン関数
if __name__ == "__main__":
    # 簡単なテスト
    processor = VideoProcessor()
    
    # テスト用の動画ファイルパス（実際のファイルに置き換えてください）
    test_video_path = "test_video.mp4"
    
    if os.path.exists(test_video_path):
        print("=== 動画検証テスト ===")
        validation_result = processor.validate_video(test_video_path)
        print(f"検証結果: {validation_result}")
        
        if validation_result['is_valid']:
            print("\n=== メタデータ取得テスト ===")
            metadata = processor.get_video_metadata(test_video_path)
            print(f"メタデータ: {metadata}")
            
            print("\n=== フレーム抽出テスト ===")
            frames = processor.extract_frames(test_video_path, max_frames=10)
            print(f"抽出フレーム数: {len(frames)}")
            
            print("\n=== 前処理テスト ===")
            preprocessed_path = processor.preprocess_video(test_video_path)
            print(f"前処理済みファイル: {preprocessed_path}")
    else:
        print(f"テスト用動画ファイルが見つかりません: {test_video_path}")
    
    # クリーンアップ
    processor.cleanup()

