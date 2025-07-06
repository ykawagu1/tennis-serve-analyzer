"""
テニスサービス動作解析 - Flask APIサーバー（完全修正版）
動画アップロード、解析、アドバイス生成のWebAPI

【主な修正点】
1. FormDataとJSON両方のリクエスト形式に対応
2. 415 Unsupported Media Typeエラーの解決
3. ChatGPT統合とエラーハンドリング強化
4. AdviceGeneratorの引数エラー修正
5. PoseDetectorのdetect_posesメソッド対応
"""

import os
import json
import time
import uuid
import shutil
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tempfile

# サービスクラスのインポート
from services.video_processor import VideoProcessor
from services.pose_detector import PoseDetector
from services.motion_analyzer import MotionAnalyzer
from services.advice_generator import AdviceGenerator

# Flask アプリケーションの初期化
app = Flask(__name__)
CORS(app)  # CORS設定

# 設定
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['SECRET_KEY'] = 'tennis-serve-analyzer-secret-key'

# ディレクトリ作成
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# サービスインスタンスの初期化
video_processor = VideoProcessor()
pose_detector = PoseDetector()
motion_analyzer = MotionAnalyzer()

# アドバイス生成器（APIキーが設定されている場合のみ）
try:
    advice_generator = AdviceGenerator()
    advice_available = True
except Exception as e:
    print(f"アドバイス生成器の初期化に失敗しました: {e}")
    advice_generator = None
    advice_available = False

# 許可されるファイル拡張子
ALLOWED_EXTENSIONS = {'.mov', '.mp4', '.avi', '.mkv', '.wmv'}


def allowed_file(filename):
    """ファイル拡張子の確認"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    """APIの基本情報"""
    return jsonify({
        'service': 'Tennis Serve Analyzer API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'upload': '/api/upload',
            'analyze': '/api/analyze',
            'advice': '/api/advice',
            'status': '/api/status/<analysis_id>',
            'download': '/api/download/<analysis_id>/<file_type>'
        },
        'features': {
            'video_processing': True,
            'pose_detection': True,
            'motion_analysis': True,
            'advice_generation': advice_available
        }
    })


@app.route('/api/upload', methods=['POST'])
def upload_video():
    """動画ファイルのアップロード"""
    try:
        # ファイルの確認
        if 'video' not in request.files:
            return jsonify({'error': 'ビデオファイルが選択されていません'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'サポートされていないファイル形式です。対応形式: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # ファイル保存
        filename = secure_filename(file.filename)
        upload_id = str(uuid.uuid4())
        file_extension = Path(filename).suffix
        saved_filename = f"{upload_id}{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        
        file.save(file_path)
        
        # ファイル検証
        validation_result = video_processor.validate_video(file_path)
        
        if not validation_result['is_valid']:
            os.remove(file_path)  # 無効なファイルを削除
            return jsonify({
                'error': f'動画ファイルの検証に失敗しました: {validation_result["error_message"]}'
            }), 400
        
        return jsonify({
            'success': True,
            'upload_id': upload_id,
            'filename': filename,
            'file_size': validation_result['metadata']['file_size'],
            'duration': validation_result['metadata']['duration'],
            'resolution': f"{validation_result['metadata']['width']}x{validation_result['metadata']['height']}",
            'fps': validation_result['metadata']['fps'],
            'warnings': validation_result['warnings']
        })
        
    except Exception as e:
        return jsonify({'error': f'アップロード中にエラーが発生しました: {str(e)}'}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """
    動画解析の実行
    
    【修正点】
    - FormDataとJSON両方のリクエスト形式に対応
    - Content-Typeを自動判定して適切に処理
    - ChatGPT設定パラメータの受信対応
    """
    try:
        # FormDataまたはJSONデータの両方に対応
        if request.content_type and 'application/json' in request.content_type:
            # JSON形式の場合
            data = request.get_json()
            if not data or 'upload_id' not in data:
                return jsonify({'error': 'upload_idが指定されていません'}), 400
            
            upload_id = data['upload_id']
            user_level = data.get('user_level', 'intermediate')
            focus_areas = data.get('focus_areas', [])
            use_chatgpt = data.get('use_chatgpt', False)
            api_key = data.get('api_key', '')
        else:
            # FormData形式の場合（動画ファイルと一緒に送信される場合）
            if 'video' not in request.files:
                return jsonify({'error': 'ビデオファイルが見つかりません'}), 400
            
            file = request.files['video']
            if file.filename == '':
                return jsonify({'error': 'ファイルが選択されていません'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({
                    'error': f'サポートされていないファイル形式です。対応形式: {", ".join(ALLOWED_EXTENSIONS)}'
                }), 400
            
            # ファイルを一時保存
            filename = secure_filename(file.filename)
            upload_id = str(uuid.uuid4())
            file_extension = Path(filename).suffix
            saved_filename = f"{upload_id}{file_extension}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(file_path)
            
            # FormDataからパラメータを取得
            user_level = request.form.get('user_level', 'intermediate')
            focus_areas = request.form.get('focus_areas', '').split(',') if request.form.get('focus_areas') else []
            use_chatgpt = request.form.get('use_chatgpt', 'false').lower() == 'true'
            api_key = request.form.get('api_key', '').strip()
        
        # アップロードされたファイルの確認（JSON形式の場合）
        if request.content_type and 'application/json' in request.content_type:
            uploaded_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.startswith(upload_id)]
            
            if not uploaded_files:
                return jsonify({'error': '指定されたファイルが見つかりません'}), 404
            
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_files[0])
        else:
            # FormData形式の場合は既にfile_pathが設定済み
            video_path = file_path
        
        # 出力ディレクトリの作成
        analysis_id = str(uuid.uuid4())
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], analysis_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # 解析実行（ChatGPT設定を含む）
        analysis_result = perform_analysis(video_path, output_dir, user_level, focus_areas, use_chatgpt, api_key)
        
        # 結果保存
        result_file = os.path.join(output_dir, 'analysis_result.json')
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'analysis_id': analysis_id,
            'result': analysis_result
        })
        
    except Exception as e:
        return jsonify({'error': f'解析中にエラーが発生しました: {str(e)}'}), 500


@app.route('/api/advice', methods=['POST'])
def generate_advice():
    """
    アドバイス生成
    
    【修正点】
    - AdviceGeneratorの正しい引数（use_chatgpt）を使用
    - 存在しないメソッドの呼び出しを削除
    """
    try:
        if not advice_available:
            return jsonify({
                'error': 'アドバイス生成機能が利用できません。OpenAI APIキーを設定してください。'
            }), 503
        
        data = request.get_json()
        
        if not data or 'analysis_id' not in data:
            return jsonify({'error': 'analysis_idが指定されていません'}), 400
        
        analysis_id = data['analysis_id']
        user_level = data.get('user_level', 'intermediate')
        focus_areas = data.get('focus_areas', [])
        advice_style = data.get('advice_style', 'constructive')
        
        # 解析結果の読み込み
        result_file = os.path.join(app.config['OUTPUT_FOLDER'], analysis_id, 'analysis_result.json')
        
        if not os.path.exists(result_file):
            return jsonify({'error': '指定された解析結果が見つかりません'}), 404
        
        with open(result_file, 'r', encoding='utf-8') as f:
            analysis_results = json.load(f)
        
        # アドバイス生成（修正済み）
        advice_result = advice_generator.generate_advice(
            analysis_results,
            use_chatgpt=False
        )
        
        # ドリル推奨も生成（基本的な推奨のみ）
        drill_result = {
            "basic_drills": [
                "シャドースイング練習",
                "トスの反復練習",
                "壁打ち練習"
            ],
            "focus_drills": [
                "体重移動練習",
                "フォロースルー練習"
            ]
        }
        
        # 結果を統合
        combined_result = {
            'advice': advice_result,
            'drills': drill_result,
            'generation_timestamp': time.time()
        }
        
        # アドバイス結果保存
        advice_file = os.path.join(app.config['OUTPUT_FOLDER'], analysis_id, 'advice_result.json')
        with open(advice_file, 'w', encoding='utf-8') as f:
            json.dump(combined_result, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'advice': advice_result,
            'drills': drill_result
        })
        
    except Exception as e:
        return jsonify({'error': f'アドバイス生成中にエラーが発生しました: {str(e)}'}), 500


@app.route('/api/status/<analysis_id>', methods=['GET'])
def get_analysis_status(analysis_id):
    """解析状況の確認"""
    try:
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], analysis_id)
        
        if not os.path.exists(output_dir):
            return jsonify({'error': '指定された解析IDが見つかりません'}), 404
        
        # ファイル存在確認
        files_status = {}
        expected_files = [
            'analysis_result.json',
            'pose_data.json',
            'preprocessed_video.mp4',
            'pose_visualization.mp4'
        ]
        
        for filename in expected_files:
            file_path = os.path.join(output_dir, filename)
            files_status[filename] = {
                'exists': os.path.exists(file_path),
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
        
        # 解析結果の読み込み（存在する場合）
        result_file = os.path.join(output_dir, 'analysis_result.json')
        analysis_summary = None
        
        if os.path.exists(result_file):
            with open(result_file, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
                analysis_summary = {
                    'overall_score': analysis_data.get('overall_score', 0.0),
                    'technical_scores': {
                        category: results.get('overall_score', 0.0)
                        for category, results in analysis_data.get('technical_analysis', {}).items()
                    }
                }
        
        return jsonify({
            'analysis_id': analysis_id,
            'status': 'completed' if files_status['analysis_result.json']['exists'] else 'processing',
            'files': files_status,
            'summary': analysis_summary
        })
        
    except Exception as e:
        return jsonify({'error': f'状況確認中にエラーが発生しました: {str(e)}'}), 500


@app.route('/api/download/<analysis_id>/<file_type>', methods=['GET'])
def download_file(analysis_id, file_type):
    """ファイルダウンロード"""
    try:
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], analysis_id)
        
        if not os.path.exists(output_dir):
            return jsonify({'error': '指定された解析IDが見つかりません'}), 404
        
        # ファイルタイプに応じたファイルパス
        file_mapping = {
            'analysis': 'analysis_result.json',
            'advice': 'advice_result.json',
            'pose_data': 'pose_data.json',
            'preprocessed_video': 'preprocessed_video.mp4',
            'pose_visualization': 'pose_visualization.mp4'
        }
        
        if file_type not in file_mapping:
            return jsonify({'error': f'サポートされていないファイルタイプです: {file_type}'}), 400
        
        filename = file_mapping[file_type]
        file_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': f'ファイルが見つかりません: {filename}'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': f'ダウンロード中にエラーが発生しました: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """ヘルスチェック"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'services': {
            'video_processor': True,
            'pose_detector': True,
            'motion_analyzer': True,
            'advice_generator': advice_available
        }
    })


def perform_analysis(video_path: str, output_dir: str, user_level: str, focus_areas: list, use_chatgpt: bool = False, api_key: str = '') -> dict:
    """
    動画解析の実行
    
    【修正点】
    - ChatGPT統合とエラーハンドリング強化
    - アドバイス生成を解析プロセスに統合
    """
    
    # Step 1: 動画前処理
    preprocessed_path = video_processor.preprocess_video(
        video_path,
        os.path.join(output_dir, 'preprocessed_video.mp4')
    )
    
    # Step 2: ポーズ検出
    pose_results = pose_detector.process_video(
        preprocessed_path,
        os.path.join(output_dir, 'pose_visualization.mp4')
    )
    
    # ポーズデータ保存
    pose_data_path = os.path.join(output_dir, 'pose_data.json')
    pose_detector.save_pose_data(pose_results, pose_data_path)
    
    # Step 3: 動作解析
    analysis_result = motion_analyzer.analyze_serve_motion(pose_results)
    
    # Step 4: アドバイス生成（ChatGPT使用の場合）
    if use_chatgpt and api_key and advice_available:
        try:
            advice_gen = AdviceGenerator(api_key=api_key)
            advice_result = advice_gen.generate_advice(analysis_result, use_chatgpt=True)
            analysis_result['advice'] = advice_result
        except Exception as e:
            print(f"ChatGPTアドバイス生成エラー: {e}")
            # エラー時は基本アドバイスを生成
            basic_advice_gen = AdviceGenerator()
            advice_result = basic_advice_gen.generate_advice(analysis_result, use_chatgpt=False)
            analysis_result['advice'] = advice_result
    elif advice_available:
        # 基本アドバイス生成
        basic_advice_gen = AdviceGenerator()
        advice_result = basic_advice_gen.generate_advice(analysis_result, use_chatgpt=False)
        analysis_result['advice'] = advice_result
    
    # 追加情報の付与
    analysis_result['processing_info'] = {
        'user_level': user_level,
        'focus_areas': focus_areas,
        'processing_timestamp': time.time(),
        'video_path': video_path,
        'output_directory': output_dir,
        'chatgpt_used': use_chatgpt and api_key and advice_available
    }
    
    return analysis_result


@app.errorhandler(413)
def too_large(e):
    """ファイルサイズエラー"""
    return jsonify({'error': 'ファイルサイズが大きすぎます（最大100MB）'}), 413


@app.errorhandler(404)
def not_found(e):
    """404エラー"""
    return jsonify({'error': 'エンドポイントが見つかりません'}), 404


@app.errorhandler(500)
def internal_error(e):
    """500エラー"""
    return jsonify({'error': 'サーバー内部エラーが発生しました'}), 500


if __name__ == '__main__':
    print("🎾 テニスサービス動作解析APIサーバーを起動中...")
    print(f"アドバイス生成機能: {'有効' if advice_available else '無効（OpenAI APIキーが必要）'}")
    print("=" * 60)
    print("【修正済み機能】")
    print("✅ FormDataとJSON両方のリクエスト形式に対応")
    print("✅ 415 Unsupported Media Typeエラーの解決")
    print("✅ ChatGPT統合とエラーハンドリング強化")
    print("✅ AdviceGeneratorの引数エラー修正")
    print("✅ PoseDetectorのdetect_posesメソッド対応")
    print("=" * 60)
    
    # 開発用サーバー起動
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )

