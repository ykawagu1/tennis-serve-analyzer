"""
テニスサービス動作解析 - 動画処理サービス（完全版）
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
        result = {
            'is_valid': False,
            'error_message': '',
            'warnings': [],
            'metadata': {}
        }
        
        try:
            # ファイル存在確認
            if not os.path.exists(file_path):
                result['error_message'] = 'ファイルが存在しません'
                return result
            
            # ファイルサイズ確認
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                result['error_message'] = f'ファイルサイズが大きすぎます（最大{self.max_file_size // (1024*1024)}MB）'
                return result
            
            # 動画メタデータ取得
            metadata = self.get_video_metadata(file_path)
            if not metadata:
                result['error_message'] = '動画ファイルの読み込みに失敗しました'
                return result
            
            result['metadata'] = metadata
            
            # 形式確認
            file_extension = Path(file_path).suffix.lower()
            if file_extension not in self.supported_formats:
                result['error_message'] = f'サポートされていない形式です: {file_extension}'
                return result
            
            # 解像度確認
            width, height = metadata['width'], metadata['height']
            if width < 480 or height < 360:
                result['warnings'].append('解像度が低すぎます（推奨: 720p以上）')
            
            # フレームレート確認
            fps = metadata['fps']
            if fps < 15:
                result['warnings'].append('フレームレートが低すぎます（推奨: 30fps以上）')
            
            # 長さ確認
            duration = metadata['duration']
            if duration > self.max_duration:
                result['warnings'].append(f'動画が長すぎます（最大{self.max_duration}秒）')
            
            result['is_valid'] = True
            
        except Exception as e:
            result['error_message'] = f'検証中にエラーが発生しました: {str(e)}'
        
        return result
    
    def get_video_metadata(self, video_path: str) -> Optional[Dict]:
        """
        動画ファイルのメタデータを取得
        
        Args:
            video_path: 動画ファイルパス
            
        Returns:
            メタデータの辞書、失敗時はNone
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
            
            # 長さ計算
            duration = frame_count / fps if fps > 0 else 0
            
            # ファイルサイズ
            file_size = os.path.getsize(video_path)
            
            cap.release()
            
            return {
                'width': width,
                'height': height,
                'fps': fps,
                'frame_count': frame_count,
                'duration': duration,
                'file_size': file_size,
                'format': Path(video_path).suffix.lower()
            }
            
        except Exception as e:
            print(f"メタデータ取得エラー: {e}")
            return None
    
    def extract_frames(self, video_path: str, 
                      max_frames: Optional[int] = None,
                      frame_interval: int = 1,
                      start_time: float = 0.0,
                      end_time: Optional[float] = None) -> List[np.ndarray]:
        """
        動画からフレームを抽出
        
        Args:
            video_path: 動画ファイルパス
            max_frames: 最大フレーム数（Noneの場合は全フレーム）
            frame_interval: フレーム間隔（1なら全フレーム、2なら1フレームおき）
            start_time: 開始時間（秒）
            end_time: 終了時間（秒、Noneの場合は最後まで）
            
        Returns:
            フレームのリスト
        """
        frames = []
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"動画ファイルを開けません: {video_path}")
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # 開始フレーム計算
            start_frame = int(start_time * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            # 終了フレーム計算
            if end_time is not None:
                end_frame = min(int(end_time * fps), total_frames)
            else:
                end_frame = total_frames
            
            frame_count = 0
            extracted_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_frame = start_frame + frame_count
                if current_frame >= end_frame:
                    break
                
                # フレーム間隔チェック
                if frame_count % frame_interval == 0:
                    frames.append(frame.copy())
                    extracted_count += 1
                    
                    # 最大フレーム数チェック
                    if max_frames and extracted_count >= max_frames:
                        break
                
                frame_count += 1
                
                # 進捗表示
                if frame_count % 30 == 0:
                    progress = (current_frame / total_frames) * 100
                    print(f"フレーム抽出進捗: {progress:.1f}% ({extracted_count}フレーム抽出)")
            
            cap.release()
            
        except Exception as e:
            print(f"フレーム抽出エラー: {e}")
            raise e
        
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
                if i % 30 == 0:
                    progress = (i / len(frames)) * 100
                    print(f"動画作成進捗: {progress:.1f}% ({i}/{len(frames)})")
            
            out.release()
            print(f"動画作成完了: {output_path}")
            return True
            
        except Exception as e:
            print(f"動画作成エラー: {e}")
            return False
    
    def extract_key_frames(self, video_path: str, num_frames: int = 10) -> List[Tuple[int, np.ndarray]]:
        """
        動画からキーフレームを抽出
        
        Args:
            video_path: 動画ファイルパス
            num_frames: 抽出するフレーム数
            
        Returns:
            (フレーム番号, フレーム)のタプルのリスト
        """
        key_frames = []
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"動画ファイルを開けません: {video_path}")
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # 等間隔でフレームを選択
            frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
            
            for frame_idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if ret:
                    key_frames.append((frame_idx, frame.copy()))
            
            cap.release()
            
        except Exception as e:
            print(f"キーフレーム抽出エラー: {e}")
        
        print(f"キーフレーム抽出完了: {len(key_frames)}フレーム")
        return key_frames
    
    def save_frames_as_images(self, frames: List[np.ndarray], 
                             output_dir: str, 
                             prefix: str = "frame",
                             format: str = "jpg") -> List[str]:
        """
        フレームを画像ファイルとして保存
        
        Args:
            frames: フレームのリスト
            output_dir: 出力ディレクトリ
            prefix: ファイル名のプレフィックス
            format: 画像形式（jpg, png）
            
        Returns:
            保存されたファイルパスのリスト
        """
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []
        
        try:
            for i, frame in enumerate(frames):
                filename = f"{prefix}_{i:06d}.{format}"
                file_path = os.path.join(output_dir, filename)
                
                if cv2.imwrite(file_path, frame):
                    saved_paths.append(file_path)
                else:
                    print(f"フレーム保存失敗: {file_path}")
            
        except Exception as e:
            print(f"フレーム保存エラー: {e}")
        
        print(f"フレーム保存完了: {len(saved_paths)}ファイル")
        return saved_paths
    
    def get_video_thumbnail(self, video_path: str, timestamp: float = 1.0) -> Optional[np.ndarray]:
        """
        動画のサムネイルを取得
        
        Args:
            video_path: 動画ファイルパス
            timestamp: サムネイル取得時間（秒）
            
        Returns:
            サムネイル画像、失敗時はNone
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
            
            if ret:
                return frame
            else:
                return None
                
        except Exception as e:
            print(f"サムネイル取得エラー: {e}")
            return None
    
    def _calculate_output_resolution(self, width: int, height: int) -> Tuple[int, int]:
        """
        出力解像度を計算
        
        Args:
            width: 元の幅
            height: 元の高さ
            
        Returns:
            (出力幅, 出力高さ)
        """
        target_width, target_height = self.target_resolution
        
        # アスペクト比を維持しながらリサイズ
        aspect_ratio = width / height
        target_aspect_ratio = target_width / target_height
        
        if aspect_ratio > target_aspect_ratio:
            # 横長の場合
            output_width = target_width
            output_height = int(target_width / aspect_ratio)
        else:
            # 縦長の場合
            output_height = target_height
            output_width = int(target_height * aspect_ratio)
        
        # 偶数に調整（動画エンコーダーの要件）
        output_width = output_width - (output_width % 2)
        output_height = output_height - (output_height % 2)
        
        return output_width, output_height
    
    def _enhance_frame_quality(self, frame: np.ndarray) -> np.ndarray:
        """
        フレームの画質向上処理
        
        Args:
            frame: 入力フレーム
            
        Returns:
            処理済みフレーム
        """
        try:
            # ノイズ除去
            frame = cv2.bilateralFilter(frame, 9, 75, 75)
            
            # コントラスト調整
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            frame = cv2.merge([l, a, b])
            frame = cv2.cvtColor(frame, cv2.COLOR_LAB2BGR)
            
            return frame
            
        except Exception as e:
            print(f"画質向上処理エラー: {e}")
            return frame
    
    def cleanup_temp_files(self):
        """一時ファイルのクリーンアップ"""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = tempfile.mkdtemp(prefix='tennis_analyzer_')


def main():
    """テスト用のメイン関数"""
    processor = VideoProcessor()
    print("VideoProcessor初期化完了")
    print(f"サポート形式: {processor.supported_formats}")
    print(f"一時ディレクトリ: {processor.temp_dir}")


if __name__ == "__main__":
    main()

