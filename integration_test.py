#!/usr/bin/env python3
"""
テニスサービス動作解析システム - 統合テストスクリプト
フロントエンドとバックエンドの連携テスト
"""

import requests
import json
import time
import os
from pathlib import Path

# API設定
API_BASE_URL = 'http://localhost:5000'
FRONTEND_URL = 'http://localhost:5173'

def test_api_health():
    """APIヘルスチェック"""
    print("=== APIヘルスチェック ===")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ APIサーバーは正常に動作しています")
            print(f"   サービス状況: {health_data['services']}")
            return True
        else:
            print(f"❌ APIサーバーエラー: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ APIサーバーに接続できません: {e}")
        return False

def test_video_upload(video_path):
    """動画アップロードテスト"""
    print("\n=== 動画アップロードテスト ===")
    
    if not os.path.exists(video_path):
        print(f"❌ テスト動画が見つかりません: {video_path}")
        return None
    
    try:
        with open(video_path, 'rb') as video_file:
            files = {'video': video_file}
            response = requests.post(f"{API_BASE_URL}/api/upload", files=files, timeout=30)
        
        if response.status_code == 200:
            upload_data = response.json()
            if upload_data['success']:
                print("✅ 動画アップロード成功")
                print(f"   アップロードID: {upload_data['upload_id']}")
                print(f"   ファイルサイズ: {upload_data['file_size']} bytes")
                print(f"   動画時間: {upload_data['duration']:.1f}秒")
                print(f"   解像度: {upload_data['resolution']}")
                print(f"   FPS: {upload_data['fps']}")
                
                if upload_data.get('warnings'):
                    print("   警告:")
                    for warning in upload_data['warnings']:
                        print(f"     - {warning}")
                
                return upload_data['upload_id']
            else:
                print(f"❌ アップロード失敗: {upload_data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"❌ アップロードエラー: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ アップロード中にエラー: {e}")
        return None

def test_video_analysis(upload_id):
    """動画解析テスト"""
    print("\n=== 動画解析テスト ===")
    
    if not upload_id:
        print("❌ アップロードIDが無効です")
        return None
    
    try:
        analysis_data = {
            'upload_id': upload_id,
            'user_level': 'intermediate',
            'focus_areas': ['knee_movement', 'elbow_position', 'toss_trajectory']
        }
        
        print("解析を開始しています...")
        response = requests.post(
            f"{API_BASE_URL}/api/analyze", 
            json=analysis_data, 
            timeout=120  # 2分のタイムアウト
        )
        
        if response.status_code == 200:
            result_data = response.json()
            if result_data['success']:
                print("✅ 動画解析成功")
                analysis_result = result_data['result']
                
                print(f"   解析ID: {result_data['analysis_id']}")
                print(f"   総合スコア: {analysis_result['overall_score']:.1f}/10.0")
                
                print("   技術要素別スコア:")
                for category, results in analysis_result.get('technical_analysis', {}).items():
                    category_name = {
                        'knee_movement': '膝の動き',
                        'elbow_position': '肘の位置',
                        'toss_trajectory': 'トス軌道',
                        'body_rotation': '体の回転',
                        'timing': 'タイミング'
                    }.get(category, category)
                    print(f"     {category_name}: {results.get('overall_score', 0):.1f}/10.0")
                
                print("   サーブフェーズ:")
                for phase_name, phase_data in analysis_result.get('serve_phases', {}).items():
                    phase_name_jp = {
                        'preparation': '準備フェーズ',
                        'ball_toss': 'ボールトス',
                        'trophy_position': 'トロフィーポジション',
                        'acceleration': '加速フェーズ',
                        'contact': 'ボール接触',
                        'follow_through': 'フォロースルー'
                    }.get(phase_name, phase_name)
                    duration = phase_data.get('duration', 0)
                    print(f"     {phase_name_jp}: {duration:.2f}秒")
                
                return result_data['analysis_id']
            else:
                print(f"❌ 解析失敗: {result_data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"❌ 解析エラー: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 解析中にエラー: {e}")
        return None

def test_advice_generation(analysis_id):
    """アドバイス生成テスト"""
    print("\n=== アドバイス生成テスト ===")
    
    if not analysis_id:
        print("❌ 解析IDが無効です")
        return False
    
    try:
        advice_data = {
            'analysis_id': analysis_id,
            'user_level': 'intermediate',
            'advice_style': 'constructive'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/advice", 
            json=advice_data, 
            timeout=60
        )
        
        if response.status_code == 200:
            result_data = response.json()
            if result_data['success']:
                print("✅ アドバイス生成成功")
                
                advice = result_data['advice']
                if advice['success']:
                    print("   個別アドバイス:")
                    advice_text = advice['advice_text'][:200] + "..." if len(advice['advice_text']) > 200 else advice['advice_text']
                    print(f"     {advice_text}")
                    
                    if 'generation_info' in advice:
                        gen_info = advice['generation_info']
                        print(f"   使用モデル: {gen_info.get('model', 'N/A')}")
                        print(f"   使用トークン数: {gen_info.get('tokens_used', 'N/A')}")
                else:
                    print(f"   ⚠️ アドバイス生成は失敗しましたが、フォールバックアドバイスを提供")
                    print(f"     理由: {advice.get('error_message', 'Unknown')}")
                
                drills = result_data['drills']
                if drills['success']:
                    print("   練習ドリル推奨:")
                    drill_text = drills['drill_text'][:200] + "..." if len(drills['drill_text']) > 200 else drills['drill_text']
                    print(f"     {drill_text}")
                else:
                    print(f"   ⚠️ ドリル推奨生成失敗: {drills.get('error_message', 'Unknown')}")
                
                return True
            else:
                print(f"❌ アドバイス生成失敗: {result_data.get('error', 'Unknown error')}")
                return False
        elif response.status_code == 503:
            print("⚠️ アドバイス生成機能は利用できません（OpenAI APIキーが未設定）")
            return True  # これは正常な状態
        else:
            print(f"❌ アドバイス生成エラー: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ アドバイス生成中にエラー: {e}")
        return False

def test_file_downloads(analysis_id):
    """ファイルダウンロードテスト"""
    print("\n=== ファイルダウンロードテスト ===")
    
    if not analysis_id:
        print("❌ 解析IDが無効です")
        return False
    
    file_types = [
        ('analysis', '解析結果'),
        ('pose_data', 'ポーズデータ'),
        ('preprocessed_video', '前処理済み動画'),
        ('pose_visualization', 'ポーズ可視化動画')
    ]
    
    success_count = 0
    
    for file_type, description in file_types:
        try:
            response = requests.get(
                f"{API_BASE_URL}/api/download/{analysis_id}/{file_type}", 
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"   ✅ {description}: ダウンロード可能 ({len(response.content)} bytes)")
                success_count += 1
            else:
                print(f"   ❌ {description}: ダウンロード失敗 ({response.status_code})")
                
        except Exception as e:
            print(f"   ❌ {description}: エラー ({e})")
    
    print(f"\nダウンロードテスト結果: {success_count}/{len(file_types)} 成功")
    return success_count == len(file_types)

def test_status_check(analysis_id):
    """ステータス確認テスト"""
    print("\n=== ステータス確認テスト ===")
    
    if not analysis_id:
        print("❌ 解析IDが無効です")
        return False
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/status/{analysis_id}", timeout=10)
        
        if response.status_code == 200:
            status_data = response.json()
            print("✅ ステータス確認成功")
            print(f"   解析ID: {status_data['analysis_id']}")
            print(f"   ステータス: {status_data['status']}")
            
            print("   ファイル状況:")
            for filename, file_info in status_data['files'].items():
                status_icon = "✅" if file_info['exists'] else "❌"
                size_info = f" ({file_info['size']} bytes)" if file_info['exists'] else ""
                print(f"     {status_icon} {filename}{size_info}")
            
            if status_data.get('summary'):
                summary = status_data['summary']
                print(f"   総合スコア: {summary['overall_score']:.1f}/10.0")
            
            return True
        else:
            print(f"❌ ステータス確認エラー: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ステータス確認中にエラー: {e}")
        return False

def test_frontend_accessibility():
    """フロントエンドアクセシビリティテスト"""
    print("\n=== フロントエンドアクセシビリティテスト ===")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        
        if response.status_code == 200:
            print("✅ フロントエンドにアクセス可能")
            
            # HTMLコンテンツの基本チェック
            html_content = response.text
            if "テニスサービス動作解析システム" in html_content:
                print("   ✅ タイトルが正しく設定されています")
            else:
                print("   ⚠️ タイトルが見つかりません")
            
            return True
        else:
            print(f"❌ フロントエンドアクセスエラー: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ フロントエンドアクセス中にエラー: {e}")
        return False

def run_integration_tests():
    """統合テストの実行"""
    print("🎾 テニスサービス動作解析システム - 統合テスト")
    print("=" * 60)
    
    # テスト結果の記録
    test_results = {}
    
    # 1. APIヘルスチェック
    test_results['api_health'] = test_api_health()
    
    # 2. フロントエンドアクセシビリティ
    test_results['frontend_access'] = test_frontend_accessibility()
    
    # 3. 動画アップロード
    demo_video_path = "demo_tennis_serve.mp4"
    upload_id = test_video_upload(demo_video_path)
    test_results['video_upload'] = upload_id is not None
    
    # 4. 動画解析
    analysis_id = None
    if upload_id:
        analysis_id = test_video_analysis(upload_id)
        test_results['video_analysis'] = analysis_id is not None
    else:
        test_results['video_analysis'] = False
    
    # 5. アドバイス生成
    if analysis_id:
        test_results['advice_generation'] = test_advice_generation(analysis_id)
    else:
        test_results['advice_generation'] = False
    
    # 6. ステータス確認
    if analysis_id:
        test_results['status_check'] = test_status_check(analysis_id)
    else:
        test_results['status_check'] = False
    
    # 7. ファイルダウンロード
    if analysis_id:
        test_results['file_downloads'] = test_file_downloads(analysis_id)
    else:
        test_results['file_downloads'] = False
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("           統合テスト結果サマリー")
    print("=" * 60)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    for test_name, result in test_results.items():
        status_icon = "✅" if result else "❌"
        test_name_jp = {
            'api_health': 'APIヘルスチェック',
            'frontend_access': 'フロントエンドアクセス',
            'video_upload': '動画アップロード',
            'video_analysis': '動画解析',
            'advice_generation': 'アドバイス生成',
            'status_check': 'ステータス確認',
            'file_downloads': 'ファイルダウンロード'
        }.get(test_name, test_name)
        
        print(f"{status_icon} {test_name_jp}")
    
    print(f"\n総合結果: {passed_tests}/{total_tests} テスト合格")
    
    if passed_tests == total_tests:
        print("🎉 すべてのテストが合格しました！システムは正常に動作しています。")
    elif passed_tests >= total_tests * 0.8:
        print("⚠️ ほとんどのテストが合格しました。一部の機能に問題がある可能性があります。")
    else:
        print("❌ 多くのテストが失敗しました。システムに重大な問題があります。")
    
    # 詳細情報
    if analysis_id:
        print(f"\n📋 テスト詳細:")
        print(f"   最終解析ID: {analysis_id}")
        print(f"   テスト動画: {demo_video_path}")
        print(f"   APIベースURL: {API_BASE_URL}")
        print(f"   フロントエンドURL: {FRONTEND_URL}")
    
    return passed_tests, total_tests

def main():
    """メイン関数"""
    try:
        passed, total = run_integration_tests()
        
        # 終了コード設定
        if passed == total:
            exit_code = 0
        elif passed >= total * 0.8:
            exit_code = 1
        else:
            exit_code = 2
        
        print(f"\n終了コード: {exit_code}")
        return exit_code
        
    except KeyboardInterrupt:
        print("\n\n⚠️ テストが中断されました")
        return 130
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        return 1

if __name__ == "__main__":
    exit(main())

