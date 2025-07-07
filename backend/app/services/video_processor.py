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

        # 前処理パラメータ（追加）
        self.frame_skip = 5    # 5フレームに1フレーム残す
        self.scale = 0.3       # 解像度30%に縮小

    def __del__(self):
        """デストラクタ - 一時ディレクトリのクリーンアップ"""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def validate_video(self, file_path: str) -> Dict[str, Union[bool, str, Dict]]:
        """
        動画ファイルの検証
        """
        validation_result = {
            'is_valid': False,
            'error_message': '',
            'warnings': [],
            'metadata': {}
        }

        try:
            if not os.path.exists(file_path):
                validation_result['error_message'] = 'ファイルが存在しません'
                return validation_result

            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                validation_result['error_message'] = f'ファイルサイズが大きすぎます（最大: {self.max_file_size // (1024*1024)}MB）'
                return validation_result

            file_extension = Path(file_path).suffix.lower()
            if file_extension not in self.supported_formats:
                validation_result['error_message'] = f'サポートされていないファイル形式です（対応形式: {", ".join(self.supported_formats)}）'
                return validation_result

            metadata = self.get_video_metadata(file_path)
            if not metadata:
                validation_result['error_message'] = '動画ファイルを読み込めません'
                return validation_result

            validation_result['metadata'] = metadata

            if metadata['duration'] > self.max_duration:
                validation_result['warnings'].append(f'動画が長すぎます（推奨: {self.max_duration}秒以下）')

            if metadata['width'] < 640 or metadata['height'] < 480:
                validation_result['warnings'].append('解像度が低すぎる可能性があります（推奨: 640x480以上）')

            if metadata['fps'] < 15:
                validation_result['warnings'].append('フレームレートが低すぎる可能性があります（推奨: 15fps以上）')

            if metadata['frame_count'] < 30:
                validation_result['warnings'].append('動画が短すぎる可能性があります（推奨: 1秒以上）')

            validation_result['is_valid'] = True

        except Exception as e:
            validation_result['error_message'] = f'検証中にエラーが発生しました: {str(e)}'

        return validation_result

    def get_video_metadata(self, video_path: str) -> Optional[Dict]:
        """
        動画メタデータの取得
        """
        try:
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                return None

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            duration = frame_count / fps if fps > 0 else 0
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
                'bitrate': (file_size * 8) / duration if duration > 0 else 0
            }

        except Exception as e:
            print(f"メタデータ取得エラー: {e}")
            return None

    def preprocess_video(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        動画の前処理（リサイズ＋間引き）
        """
        if output_path is None:
            output_path = os.path.join(self.temp_dir, f"preprocessed_{int(time.time())}.mp4")

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"動画ファイルを開けません: {video_path}")

        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        original_fps = cap.get(cv2.CAP_PROP_FPS)

        # 出力設定
        output_fps = original_fps / self.frame_skip if original_fps > 0 else 10.0
        output_width = int(original_width * self.scale)
        output_height = int(original_height * self.scale)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, output_fps, (output_width, output_height))

        frame_count = 0
        kept_frames = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # フレーム間引き
                if frame_count % self.frame_skip == 0:
                    resized_frame = cv2.resize(frame, (output_width, output_height))
                    enhanced_frame = self._enhance_frame_quality(resized_frame)
                    out.write(enhanced_frame)
                    kept_frames += 1

                frame_count += 1

                if kept_frames % 30 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"前処理進捗: {progress:.1f}% ({kept_frames}フレーム保存)")

        finally:
            cap.release()
            out.release()

        print(f"✅ 前処理完了: {output_path}")
        print(f"📊 元フレーム数: {total_frames}, 保存フレーム数: {kept_frames}")
        print(f"🆕 新FPS: {output_fps:.2f}, 新解像度: {output_width}x{output_height}")

        return output_path

    def _enhance_frame_quality(self, frame: np.ndarray) -> np.ndarray:
        """フレーム品質の向上"""
        denoised = cv2.bilateralFilter(frame, 9, 75, 75)
        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        return enhanced
