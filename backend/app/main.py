"""
テニスサーブ解析システム - メインアプリケーション（完全修正版・回転物理補正対応）
"""

import os
import sys
import logging
import traceback
import subprocess
import json

from utils import generate_overlay_images_with_dominant_hand
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid

# サービスのインポート
from services.video_processor import VideoProcessor
from services.pose_detector import PoseDetector
from services.motion_analyzer import MotionAnalyzer
from services.advice_generator import AdviceGenerator

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    static_url_path='/static'
)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ★★★ ffprobeで回転を完全検出(JSON解析) ★★★
def detect_rotation_ffprobe(file_path):
    try:
        cmd = [
            'ffprobe', '-v', 'error', '-print_format', 'json',
            '-show_streams', '-show_format', file_path
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        meta = json.loads(output)
        rotate = 0
        for stream in meta.get('streams', []):
            tags = stream.get('tags', {})
            if 'rotate' in tags:
                try:
                    rotate = int(tags['rotate'])
                    break
                except Exception:
                    pass
            for side_data in stream.get('side_data_list', []):
                if 'rotation' in side_data:
                    try:
                        rotate = int(side_data['rotation'])
                        break
                    except Exception:
                        pass
        return rotate
    except Exception as e:
        print(f"ffprobe回転取得エラー: {e}")
        return 0

# ★★★ ffmpegで物理的に動画を回転 ★★★
def physically_rotate_video(input_path, output_path, rotate):
    # ±90/±180/±270対応（±270はtransposeの都合で一部サポート外）
    transpose_val = None
    if rotate == 90:
        transpose_val = 1  # 時計回り
    elif rotate == -90 or rotate == 270:
        transpose_val = 3  # 反時計回り
    elif rotate == 180 or rotate == -180:
        transpose_val = 2  # 上下反転（近似）
    else:
        # 回転不要 or 未対応
        return input_path
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"transpose={transpose_val}",
        "-metadata:s:v", "rotate=0",
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"ffmpegで物理回転補正済: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg回転失敗: {e.stderr.decode()}")
        return input_path

@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    try:
        logger.info("=== 動画解析リクエスト受信 ===")
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'ビデオファイルが見つかりません'}), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'ファイルが選択されていません'}), 400
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': '対応していないファイル形式です'}), 400

        # ファイル保存
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        video_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(video_path)
        logger.info(f"ファイル保存完了: {video_path}")

        # (1) ffprobeで回転検出
        rotate = detect_rotation_ffprobe(video_path)
        logger.info(f"ffprobe回転角度: {rotate}")

        # (2) 回転物理補正（必要時のみ）
        processed_path = video_path
        if rotate not in [0, None]:
            rotated_path = os.path.join(UPLOAD_FOLDER, f"rotated_{unique_filename}")
            processed_path = physically_rotate_video(video_path, rotated_path, rotate)
        logger.info(f"物理回転補正済みパス: {processed_path}")

        # (3) 軽量化 (cv2で解像度/フレーム数ダウン)
        video_processor = VideoProcessor()
        preprocessed_path = video_processor.preprocess_video(processed_path)

        # (4) 解析用出力ディレクトリ生成
        out_dir = os.path.join(OUTPUT_FOLDER, str(uuid.uuid4()))
        os.makedirs(out_dir, exist_ok=True)

        # (5) メタデータ再取得 (※今度は正しい向き)
        video_metadata = video_processor.get_video_metadata(preprocessed_path)
        logger.info(f"動画メタデータ: {video_metadata}")

        # (6) ポーズ検出
        pose_detector = PoseDetector()
        pose_results = pose_detector.detect_poses(preprocessed_path, out_dir)
        logger.info(f"ポーズ検出フレーム数: {len(pose_results)}")

        # (7) サーブフェーズ検出
        from services.motion_analyzer import ServePhase
        total_frames = len(pose_results)
        phase_duration = total_frames // 6 if total_frames else 1
        phase_names = [
            'preparation', 'ball_toss', 'trophy_position',
            'acceleration', 'contact', 'follow_through'
        ]
        serve_phases = []
        for i, name in enumerate(phase_names):
            start_frame = i * phase_duration
            end_frame = min((i+1) * phase_duration, total_frames)
            duration = (end_frame - start_frame) / video_metadata.get('fps', 30)
            serve_phases.append(ServePhase(
                name=name, start_frame=start_frame,
                end_frame=end_frame, duration=duration, key_events=[]
            ))

        # (8) 動作解析
        motion_analyzer = MotionAnalyzer()
        analysis_result = motion_analyzer.analyze_motion(
            pose_results, serve_phases, video_metadata
        )

        # (9) 段階的評価
        tiered_evaluation = motion_analyzer.calculate_tiered_overall_score(analysis_result)
        analysis_result['tiered_evaluation'] = tiered_evaluation

        # (10) アドバイス生成
        advice_generator = AdviceGenerator()
        advice = advice_generator.generate_advice(
            analysis_result, use_chatgpt=False, api_key="",
            user_concerns="", user_level="intermediate"
        )
        analysis_result['advice'] = advice

        # (11) オーバーレイ画像生成
        overlay_images = generate_overlay_images_with_dominant_hand(
            preprocessed_path, pose_results, out_dir, pose_detector
        )
        analysis_result['overlay_images'] = [
            '/' + os.path.relpath(img_path, start=os.path.dirname(__file__)).replace('\\', '/')
            for img_path in overlay_images
        ]
        logger.info(f"生成オーバーレイ画像: {overlay_images}")

        return jsonify({'success': True, 'result': analysis_result})

    except Exception as e:
        logger.error(f"解析エラー: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/api/download/<filename>")
def download_file(filename):
    """アップロード/生成ファイルDL用（デバッグ用）"""
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    logger.info("テニスサーブ解析システム起動中...")
    app.run(host='0.0.0.0', port=5000, debug=True)
