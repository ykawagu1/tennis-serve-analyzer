"""
テニスサービス動作解析 - アドバイス生成サービス（デバッグ版）
解析結果に基づいて改善アドバイスを生成
"""

import logging
from typing import Dict, List, Optional
import json

logger = logging.getLogger(__name__)

class AdviceGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        アドバイス生成器の初期化
        
        Args:
            api_key: OpenAI API キー（オプション）
        """
        self.api_key = api_key
        self.client = None
        
        if api_key:
            try:
                # OpenAI v1.0+ 対応
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
                logger.info("OpenAI クライアント初期化成功（v1.0+）")
            except ImportError:
                try:
                    # OpenAI v0.x 対応
                    import openai
                    openai.api_key = api_key
                    logger.info("OpenAI API キー設定成功（v0.x）")
                except ImportError:
                    logger.error("OpenAI ライブラリがインストールされていません")
    
    def generate_advice(self, analysis_data: Dict, user_level: str = 'intermediate', focus_areas: List = None, use_chatgpt: bool = False, api_key: str = '', user_concerns: str = '') -> Dict:
        """
        解析データに基づいてアドバイスを生成（user_concerns対応）
        
        Args:
            analysis_data: 動作解析データ
            user_level: ユーザーレベル
            focus_areas: 重点分野
            use_chatgpt: ChatGPT APIを使用するかどうか
            api_key: OpenAI APIキー
            user_concerns: ユーザーの気になっていること（新機能）
            
        Returns:
            アドバイスデータ
        """
        try:
            logger.info(f"アドバイス生成開始 - ChatGPT使用: {use_chatgpt}, APIキー: {'あり' if (api_key or self.api_key) else 'なし'}, 気になること: {bool(user_concerns)}")
            
            # デバッグ: analysis_dataの内容をログ出力
            print(f"🔍 DEBUG: analysis_data = {analysis_data}")
            logger.info(f"🔍 DEBUG: analysis_data = {analysis_data}")
            
            # APIキーの設定（引数で渡された場合は優先）
            if api_key and not self.api_key:
                self.api_key = api_key
                try:
                    from openai import OpenAI
                    self.client = OpenAI(api_key=api_key)
                except ImportError:
                    import openai
                    openai.api_key = api_key
            
            # 基本アドバイスを生成
            basic_advice = self._generate_basic_advice(analysis_data)
            
            if use_chatgpt and (self.api_key or api_key):
                logger.info("ChatGPT詳細アドバイス生成を開始")
                # ChatGPT APIを使用して詳細アドバイスを生成（user_concerns対応）
                enhanced_advice = self._generate_enhanced_advice(analysis_data, basic_advice, user_concerns)
                logger.info(f"ChatGPT詳細アドバイス生成完了 - Enhanced: {enhanced_advice.get('enhanced', False)}")
                return enhanced_advice
            else:
                logger.info("基本アドバイスのみ生成")
                # user_concernsがある場合は基本的なワンポイントアドバイスを追加
                if user_concerns:
                    basic_advice['one_point_advice'] = self._generate_basic_one_point_advice(user_concerns)
                return basic_advice
                
        except Exception as e:
            logger.error(f"アドバイス生成エラー: {e}")
            return self._generate_fallback_advice()
    
    def _generate_basic_advice(self, analysis_data: Dict) -> Dict:
        """基本的なアドバイスを生成"""
        
        # デバッグ: 入力データの詳細確認
        print(f"🔍 DEBUG: _generate_basic_advice called with analysis_data = {analysis_data}")
        
        # total_scoreの取得方法を複数試行
        total_score = None
        
        # 方法1: 直接取得
        if 'total_score' in analysis_data:
            total_score = analysis_data['total_score']
            print(f"🔍 DEBUG: total_score from 'total_score' = {total_score}")
        
        # 方法2: tiered_evaluationから取得
        elif 'tiered_evaluation' in analysis_data and analysis_data['tiered_evaluation']:
            tiered_eval = analysis_data['tiered_evaluation']
            if 'total_score' in tiered_eval:
                total_score = tiered_eval['total_score']
                print(f"🔍 DEBUG: total_score from 'tiered_evaluation.total_score' = {total_score}")
        
        # 方法3: overall_scoreから取得
        elif 'overall_score' in analysis_data:
            total_score = analysis_data['overall_score']
            print(f"🔍 DEBUG: total_score from 'overall_score' = {total_score}")
        
        # デフォルト値
        if total_score is None:
            total_score = 0
            print(f"🔍 DEBUG: total_score defaulted to 0")
        
        print(f"🔍 DEBUG: Final total_score = {total_score} (type: {type(total_score)})")
        
        # phase_analysisの取得
        phase_analysis = analysis_data.get('phase_analysis', {})
        print(f"🔍 DEBUG: phase_analysis = {phase_analysis}")
        
        # 総合評価の決定
        if total_score >= 8:
            overall = "素晴らしいサービスフォームです！細かい調整でさらに向上できます。"
            print(f"🔍 DEBUG: Score >= 8, selected: {overall}")
        elif total_score >= 6:
            overall = "良好なサービスフォームです。いくつかの改善点があります。"
            print(f"🔍 DEBUG: Score >= 6, selected: {overall}")
        elif total_score >= 4:
            overall = "基本的なフォームはできています。重要なポイントを改善しましょう。"
            print(f"🔍 DEBUG: Score >= 4, selected: {overall}")
        else:
            overall = "フォームに改善の余地があります。基礎から見直しましょう。"
            print(f"🔍 DEBUG: Score < 4, selected: {overall}")
        
        # 技術的ポイント
        technical_points = []
        practice_suggestions = []
        
        for phase, data in phase_analysis.items():
            score = data.get('score', 0) if isinstance(data, dict) else 0
            print(f"🔍 DEBUG: Phase '{phase}' score = {score}")
            
            if score < 7:
                if phase == "準備":
                    technical_points.append("スタンス（足の位置）の安定性を向上させましょう")
                    practice_suggestions.append("壁に向かって正しいスタンスで素振り練習")
                elif phase == "トスアップ":
                    technical_points.append("トスの高さと位置の一貫性を改善しましょう")
                    practice_suggestions.append("一定の高さでトスを上げる反復練習")
                elif phase == "バックスイング":
                    technical_points.append("ラケットの引き方とタイミングを調整しましょう")
                    practice_suggestions.append("ゆっくりとしたシャドースイング練習")
                elif phase == "フォワードスイング":
                    technical_points.append("スイングスピードと軌道を最適化しましょう")
                    practice_suggestions.append("段階的にスピードを上げるスイング練習")
                elif phase == "インパクト":
                    technical_points.append("ボールとの接触点を改善しましょう")
                    practice_suggestions.append("ネット前でのインパクト確認練習")
                elif phase == "フォロースルー":
                    technical_points.append("フィニッシュの形を安定させましょう")
                    practice_suggestions.append("フォロースルーを意識したスロー練習")
        
        result = {
            "basic_advice": overall,
            "technical_points": technical_points,
            "practice_suggestions": practice_suggestions,
            "enhanced": False
        }
        
        print(f"🔍 DEBUG: Generated basic_advice result = {result}")
        
        return result
    
    def _generate_enhanced_advice(self, analysis_data: Dict, basic_advice: Dict, user_concerns: str = '') -> Dict:
        """ChatGPT APIを使用して詳細なアドバイスを生成（user_concerns対応）"""
        try:
            logger.info("ChatGPT API呼び出し開始")
            
            # 解析データを整理
            total_score = analysis_data.get('total_score', 0)
            phase_analysis = analysis_data.get('phase_analysis', {})
            
            # ChatGPTへの詳細なプロンプトを作成（user_concerns対応）
            prompt = self._create_detailed_prompt(total_score, phase_analysis, basic_advice, user_concerns)
            
            # ChatGPT APIを呼び出し
            ai_response = self._call_chatgpt_api(prompt)
            
            if ai_response:
                logger.info("ChatGPT API呼び出し成功")
                # レスポンスを解析
                enhanced_advice = self._parse_ai_response(ai_response, basic_advice)
                enhanced_advice["enhanced"] = True
                enhanced_advice["detailed_advice"] = ai_response
                
                # user_concernsがある場合はワンポイントアドバイスを抽出
                if user_concerns:
                    enhanced_advice["one_point_advice"] = self._extract_one_point_advice(ai_response, user_concerns)
                
                return enhanced_advice
            else:
                logger.error("ChatGPT APIからの応答が空です")
                basic_advice["enhanced"] = False
                basic_advice["error"] = "ChatGPT APIからの応答が空でした"
                return basic_advice
            
        except Exception as e:
            logger.error(f"ChatGPT API呼び出しエラー: {e}")
            # エラー時は基本アドバイスを返す
            basic_advice["enhanced"] = False
            basic_advice["error"] = f"ChatGPT接続エラー: {str(e)}"
            # user_concernsがある場合は基本的なワンポイントアドバイスを追加
            if user_concerns:
                basic_advice['one_point_advice'] = self._generate_basic_one_point_advice(user_concerns)
            return basic_advice
    
    def _call_chatgpt_api(self, prompt: str) -> str:
        """ChatGPT APIを呼び出し"""
        try:
            if self.client:
                # OpenAI v1.0+ 対応
                logger.info("OpenAI v1.0+ APIを使用")
                response = self.client.chat.completions.create(
                    model="gpt-4o",  # GPT-4oを使用
                    messages=[
                        {
                            "role": "system",
                            "content": """あなたは30年以上の経験を持つATP/WTAツアーのプロテニスコーチです。グランドスラム優勝者を指導した実績があり、スポーツ科学博士号（バイオメカニクス専門）を持っています。

テニスサービスの動作解析結果に基づいて、世界基準の詳細なアドバイスを提供してください。

以下の構成で、合計2000文字程度の詳細なアドバイスを生成してください：

## フォーム改善点の詳細分析
（約500文字）
- 現在のフォームの具体的な問題点
- 理想的なフォームとの比較
- 改善による効果の科学的説明

## 4週間トレーニングプログラム
（約500文字）
- 週ごとの段階的な技術練習メニュー
- 各週の重点ポイント
- 練習時間と頻度の具体的指示

## フィジカル強化メニュー
（約500文字）
- サーブに必要な筋力強化
- 柔軟性向上のストレッチ
- 体幹安定性の向上方法
- 週3回、各30分程度の具体的メニュー

## 実戦での確認ポイント
（約300文字）
- 練習での確認方法
- 試合での意識すべき点
- 上達の測定方法

## ワンポイントアドバイス
（約200文字）
- ユーザーの具体的な悩みに対する即効性のあるアドバイス
- 明日から実践できる具体的な方法

必ず日本語で回答し、専門用語は分かりやすく説明してください。"""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=3000,
                    temperature=0.7
                )
                return response.choices[0].message.content
            else:
                # OpenAI v0.x 対応
                logger.info("OpenAI v0.x APIを使用")
                import openai
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": """あなたは30年以上の経験を持つATP/WTAツアーのプロテニスコーチです。グランドスラム優勝者を指導した実績があり、スポーツ科学博士号（バイオメカニクス専門）を持っています。

テニスサービスの動作解析結果に基づいて、世界基準の詳細なアドバイスを提供してください。

以下の構成で、合計2000文字程度の詳細なアドバイスを生成してください：

## フォーム改善点の詳細分析
（約500文字）
- 現在のフォームの具体的な問題点
- 理想的なフォームとの比較
- 改善による効果の科学的説明

## 4週間トレーニングプログラム
（約500文字）
- 週ごとの段階的な技術練習メニュー
- 各週の重点ポイント
- 練習時間と頻度の具体的指示

## フィジカル強化メニュー
（約500文字）
- サーブに必要な筋力強化
- 柔軟性向上のストレッチ
- 体幹安定性の向上方法
- 週3回、各30分程度の具体的メニュー

## 実戦での確認ポイント
（約300文字）
- 練習での確認方法
- 試合での意識すべき点
- 上達の測定方法

## ワンポイントアドバイス
（約200文字）
- ユーザーの具体的な悩みに対する即効性のあるアドバイス
- 明日から実践できる具体的な方法

必ず日本語で回答し、専門用語は分かりやすく説明してください。"""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=3000,
                    temperature=0.7
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"ChatGPT API呼び出しエラー: {e}")
            return None
    
    def _create_detailed_prompt(self, total_score: float, phase_analysis: Dict, basic_advice: Dict, user_concerns: str = '') -> str:
        """詳細なプロンプトを作成（user_concerns対応）"""
        
        # フェーズ別スコアの整理
        phase_scores = []
        weak_phases = []
        for phase, data in phase_analysis.items():
            score = data.get('score', 0) if isinstance(data, dict) else 0
            phase_scores.append(f"{phase}: {score:.1f}点")
            if score < 7:
                weak_phases.append(phase)
        
        # ユーザーの悩みに関する情報
        concerns_text = ""
        if user_concerns:
            concerns_text = f"\n\n【ユーザーの具体的な悩み】\n{user_concerns}\n\n上記の悩みに特に焦点を当てて、具体的で実践的なアドバイスを含めてください。"
        
        prompt = f"""
【テニスサーブ動作解析結果】

総合スコア: {total_score:.1f}/10点

フェーズ別スコア:
{chr(10).join(phase_scores)}

改善が必要なフェーズ: {', '.join(weak_phases) if weak_phases else 'なし'}

基本的な技術ポイント:
{chr(10).join(f"- {point}" for point in basic_advice.get('technical_points', []))}
{concerns_text}

この解析結果に基づいて、以下の構成で詳細なアドバイスを生成してください：

1. フォーム改善点の詳細分析（500文字程度）
2. 4週間トレーニングプログラム（500文字程度）
3. フィジカル強化メニュー（500文字程度）
4. 実戦での確認ポイント（300文字程度）
5. ワンポイントアドバイス（200文字程度）

特に改善が必要なフェーズ（{', '.join(weak_phases)}）に重点を置いて、具体的で実践的なアドバイスをお願いします。
"""
        
        return prompt
    
    def _parse_ai_response(self, ai_response: str, basic_advice: Dict) -> Dict:
        """AI応答を解析してアドバイスデータに変換"""
        # 基本アドバイスをベースにして、AI応答を追加
        enhanced_advice = basic_advice.copy()
        enhanced_advice["detailed_advice"] = ai_response
        enhanced_advice["enhanced"] = True
        
        return enhanced_advice
    
    def _extract_one_point_advice(self, ai_response: str, user_concerns: str) -> str:
        """AI応答からワンポイントアドバイスを抽出"""
        # ワンポイントアドバイスの部分を抽出
        lines = ai_response.split('\n')
        one_point_section = False
        one_point_advice = []
        
        for line in lines:
            if 'ワンポイント' in line or '即効性' in line:
                one_point_section = True
                continue
            elif one_point_section and line.strip():
                if line.startswith('#') and 'ワンポイント' not in line:
                    break
                one_point_advice.append(line.strip())
        
        if one_point_advice:
            return '\n'.join(one_point_advice)
        else:
            # フォールバック: user_concernsに基づく基本的なアドバイス
            return self._generate_basic_one_point_advice(user_concerns)
    
    def _generate_basic_one_point_advice(self, user_concerns: str) -> str:
        """user_concernsに基づく基本的なワンポイントアドバイス"""
        concerns_lower = user_concerns.lower()
        
        if 'トス' in user_concerns or 'toss' in concerns_lower:
            return "トスの安定性向上のため、毎日10回、同じ高さ・同じ位置にトスを上げる練習を行いましょう。"
        elif '威力' in user_concerns or 'パワー' in user_concerns or 'power' in concerns_lower:
            return "サーブの威力向上には、体幹の回転を意識し、下半身から上半身への運動連鎖を強化しましょう。"
        elif 'フォーム' in user_concerns or 'form' in concerns_lower:
            return "フォームの安定には、鏡の前でのスロー練習を週3回、各10分間行うことが効果的です。"
        elif 'コントロール' in user_concerns or 'control' in concerns_lower:
            return "コントロール向上のため、ターゲットを設置してのサーブ練習を1日20球から始めましょう。"
        else:
            return "まずは基本的なサーブフォームの確認から始め、一つずつ改善点を意識して練習しましょう。"
    
    def _generate_fallback_advice(self) -> Dict:
        """エラー時のフォールバックアドバイス"""
        return {
            "basic_advice": "サーブフォームの基本を確認し、段階的に改善していきましょう。",
            "technical_points": [
                "正しいスタンスの確認",
                "トスの一貫性向上",
                "スムーズなスイング動作"
            ],
            "practice_suggestions": [
                "基本フォームの反復練習",
                "ターゲット練習",
                "スロー練習からの段階的向上"
            ],
            "enhanced": False,
            "error": "アドバイス生成中にエラーが発生しました"
        }

