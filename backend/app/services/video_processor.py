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
        self.target_fps = 30
        self.target_resolution = (1280, 720)  # HD解像度
        self.max_duration = 30  # 最大30秒
    
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
            
        except Exception as e:
            validation_result['error_message'] = f'検証中にエラーが発生しました: {str(e)}'
        
        return validation_result
    
    def get_video_metadata(self, video_path: str) -> Optional[Dict]:
        """
        動画メタデータの取得
        
        Args:
            video_path: 動画ファイルパス
            
        Returns:
            メタデータの辞書、エラー時はNone
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return None
            
            # 基本情報取得
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # 時間計算
            duration = frame_count / fps if fps > 0 else 0
            
            # ファイル情報
            file_size = os.path.getsize(video_path)
            file_name = os.path.basename(video_path)
            
            cap.release()
            
            return {
                'filename': file_name,
                'file_size': file_size,
                'width': width,
                'height': height,
                'fps': fps,
                'frame_count': frame_count,
                'duration': duration,
                'aspect_ratio': width / height if height > 0 else 0,
                'bitrate': (file_size * 8) / duration if duration > 0 else 0  # bps
            }
            
        except Exception as e:
            print(f"メタデータ取得エラー: {e}")
            return None
    
    def extract_frames(self, video_path: str, 
                      start_time: float = 0.0, 
                      end_time: Optional[float] = None,
                      target_fps: Optional[int] = None) -> List[np.ndarray]:
        """
        動画からフレームを抽出
        
        Args:
            video_path: 動画ファイルパス
            start_time: 開始時間（秒）
            end_time: 終了時間（秒）、Noneの場合は最後まで
            target_fps: 目標フレームレート、Noneの場合は元のFPS
            
        Returns:
            フレームのリスト
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"動画ファイルを開けません: {video_path}")
        
        # 動画情報取得
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / original_fps if original_fps > 0 else 0
        
        # 時間範囲の調整
        if end_time is None:
            end_time = duration
        end_time = min(end_time, duration)
        start_time = max(0, start_time)
        
        # フレーム範囲計算
        start_frame = int(start_time * original_fps)
        end_frame = int(end_time * original_fps)
        
        # フレームサンプリング設定
        if target_fps is None:
            target_fps = original_fps
        
        frame_interval = max(1, int(original_fps / target_fps))
        
        frames = []
        frame_number = 0
        
        try:
            # 開始フレームまでスキップ
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            while True:
                ret, frame = cap.read()
                if not ret or frame_number >= (end_frame - start_frame):
                    break
                
                # フレームサンプリング
                if frame_number % frame_interval == 0:
                    frames.append(frame.copy())
                
                frame_number += 1
                
                # 進捗表示
                if len(frames) % 30 == 0:
                    progress = (frame_number / (end_frame - start_frame)) * 100
                    print(f"フレーム抽出進捗: {progress:.1f}% ({len(frames)}フレーム)")
        
        finally:
            cap.release()
        
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
        output_fps = min(self.target_fps, original_fps)
        
        # 動画ライター設定
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, output_fps, (output_width, output_height))
        
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # リサイズ
                if (original_width, original_height) != (output_width, output_height):
                    frame = cv2.resize(frame, (output_width, output_height), interpolation=cv2.INTER_LANCZOS4)
                
                # 画質向上処理
                frame = self._enhance_frame_quality(frame)
                
                out.write(frame)
                frame_count += 1
                
                # 進捗表示
                if frame_count % 30 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"前処理進捗: {progress:.1f}% ({frame_count}/{total_frames})")
        
        finally:
            cap.release()
            out.release()
        
        print(f"前処理完了: {output_path}")
        return output_path
    
    def create_video_from_frames(self, frames: List[np.ndarray], 
                                output_path: str, 
                                fps: float = 30.0) -> bool:
        """
        フレームから動画を作成
        
        Args:
            frames: フレームのリスト
            output_path: 出力動画ファイルパス
            fps: フレームレート
            
        Returns:
            成功時True、失敗時False
        """
        if not frames:
            return False
        
        try:
            height, width = frames[0].shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            for i, frame in enumerate(frames):
                out.write(frame)
                
                # 進捗表示
                if (i + 1) % 30 == 0:
                    progress = ((i + 1) / len(frames)) * 100
                    print(f"動画作成進捗: {progress:.1f}% ({i + 1}/{len(frames)})")
            
            out.release()
            print(f"動画作成完了: {output_path}")
            return True
            
        except Exception as e:
            print(f"動画作成エラー: {e}")
            return False
    
    def extract_key_frames(self, video_path: str, num_frames: int = 10) -> List[Tuple[int, np.ndarray]]:
        """
        キーフレームの抽出
        
        Args:
            video_path: 動画ファイルパス
            num_frames: 抽出するフレーム数
            
        Returns:
            (フレーム番号, フレーム画像)のタプルリスト
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"動画ファイルを開けません: {video_path}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # キーフレームのインデックス計算
        if num_frames >= total_frames:
            frame_indices = list(range(total_frames))
        else:
            frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
        
        key_frames = []
        
        try:
            for frame_idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if ret:
                    key_frames.append((frame_idx, frame.copy()))
        
        finally:
            cap.release()
        
        print(f"キーフレーム抽出完了: {len(key_frames)}フレーム")
        return key_frames
    
    def save_frames_as_images(self, frames: List[np.ndarray], 
                             output_dir: str, 
                             prefix: str = "frame") -> List[str]:
        """
        フレームを画像ファイルとして保存
        
        Args:
            frames: フレームのリスト
            output_dir: 出力ディレクトリ
            prefix: ファイル名のプレフィックス
            
        Returns:
            保存された画像ファイルパスのリスト
        """
        os.makedirs(output_dir, exist_ok=True)
        
        saved_paths = []
        
        for i, frame in enumerate(frames):
            filename = f"{prefix}_{i:06d}.jpg"
            filepath = os.path.join(output_dir, filename)
            
            success = cv2.imwrite(filepath, frame)
            if success:
                saved_paths.append(filepath)
            
            # 進捗表示
            if (i + 1) % 50 == 0:
                progress = ((i + 1) / len(frames)) * 100
                print(f"画像保存進捗: {progress:.1f}% ({i + 1}/{len(frames)})")
        
        print(f"画像保存完了: {len(saved_paths)}ファイル")
        return saved_paths
    
    def get_video_thumbnail(self, video_path: str, timestamp: float = 1.0) -> Optional[np.ndarray]:
        """
        動画のサムネイル取得
        
        Args:
            video_path: 動画ファイルパス
            timestamp: サムネイル取得時間（秒）
            
        Returns:
            サムネイル画像、エラー時はNone
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return None
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(timestamp * fps)
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            
            cap.release()
            
            return frame if ret else None
            
        except Exception as e:
            print(f"サムネイル取得エラー: {e}")
            return None
    
    def _calculate_output_resolution(self, width: int, height: int) -> Tuple[int, int]:
        """出力解像度の計算"""
        target_width, target_height = self.target_resolution
        
        # アスペクト比を保持してリサイズ
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
    
    def _enhance_frame_quality(self, frame: np.ndarray) -> np.ndarray:
        """フレーム品質の向上"""
        # ノイズ除去
        denoised = cv2.bilateralFilter(frame, 9, 75, 75)
        
        # コントラスト調整
        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # CLAHE（Contrast Limited Adaptive Histogram Equalization）適用
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def cleanup_temp_files(self):
        """一時ファイルのクリーンアップ"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = tempfile.mkdtemp(prefix='tennis_analyzer_')


def main():
    """テスト用のメイン関数"""
    processor = VideoProcessor()
    
    # テスト用の動画ファイルパス
    test_video_path = "/path/to/test_video.mov"
    
    try:
        # 動画検証
        validation_result = processor.validate_video(test_video_path)
        
        if validation_result['is_valid']:
            print("動画検証成功")
            print(f"メタデータ: {validation_result['metadata']}")
            
            if validation_result['warnings']:
                print("警告:")
                for warning in validation_result['warnings']:
                    print(f"  - {warning}")
            
            # 前処理実行
            preprocessed_path = processor.preprocess_video(test_video_path)
            print(f"前処理済み動画: {preprocessed_path}")
            
            # フレーム抽出
            frames = processor.extract_frames(preprocessed_path, target_fps=15)
            print(f"抽出フレーム数: {len(frames)}")
            
            # キーフレーム抽出
            key_frames = processor.extract_key_frames(preprocessed_path, num_frames=5)
            print(f"キーフレーム数: {len(key_frames)}")
            
            # サムネイル取得
            thumbnail = processor.get_video_thumbnail(preprocessed_path)
            if thumbnail is not None:
                cv2.imwrite("thumbnail.jpg", thumbnail)
                print("サムネイル保存: thumbnail.jpg")
        
        else:
            print(f"動画検証失敗: {validation_result['error_message']}")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    finally:
        # クリーンアップ
        processor.cleanup_temp_files()


if __name__ == "__main__":
    main()

