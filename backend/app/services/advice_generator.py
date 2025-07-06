import json
from typing import Dict, List, Optional
import logging

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
    
    def generate_advice(self, analysis_data: Dict, use_chatgpt: bool = False) -> Dict:
        """
        解析データに基づいてアドバイスを生成
        
        Args:
            analysis_data: 動作解析データ
            use_chatgpt: ChatGPT APIを使用するかどうか
            
        Returns:
            アドバイスデータ
        """
        try:
            logger.info(f"アドバイス生成開始 - ChatGPT使用: {use_chatgpt}, APIキー: {'あり' if self.api_key else 'なし'}")
            
            # 基本アドバイスを生成
            basic_advice = self._generate_basic_advice(analysis_data)
            
            if use_chatgpt and self.api_key:
                logger.info("ChatGPT詳細アドバイス生成を開始")
                # ChatGPT APIを使用して詳細アドバイスを生成
                enhanced_advice = self._generate_enhanced_advice(analysis_data, basic_advice)
                logger.info(f"ChatGPT詳細アドバイス生成完了 - Enhanced: {enhanced_advice.get('enhanced', False)}")
                return enhanced_advice
            else:
                logger.info("基本アドバイスのみ生成")
                return basic_advice
                
        except Exception as e:
            logger.error(f"アドバイス生成エラー: {e}")
            return self._generate_fallback_advice()
    
    def _generate_basic_advice(self, analysis_data: Dict) -> Dict:
        """基本的なアドバイスを生成"""
        total_score = analysis_data.get('total_score', 0)
        phase_analysis = analysis_data.get('phase_analysis', {})
        
        # 総合評価
        if total_score >= 8:
            overall = "素晴らしいサービスフォームです！細かい調整でさらに向上できます。"
        elif total_score >= 6:
            overall = "良好なサービスフォームです。いくつかの改善点があります。"
        elif total_score >= 4:
            overall = "基本的なフォームはできています。重要なポイントを改善しましょう。"
        else:
            overall = "フォームに改善の余地があります。基礎から見直しましょう。"
        
        # 技術的ポイント
        technical_points = []
        practice_suggestions = []
        
        for phase, data in phase_analysis.items():
            score = data.get('score', 0)
            if score < 6:
                if phase == "準備フェーズ":
                    technical_points.append("スタンス幅を肩幅程度に調整し、体重を前足に乗せましょう")
                    practice_suggestions.append("壁打ちで正しいスタンスを練習する")
                elif phase == "トスフェーズ":
                    technical_points.append("トスの高さと位置を一定にしましょう")
                    practice_suggestions.append("トスのみの練習を毎日50回行う")
                elif phase == "バックスイングフェーズ":
                    technical_points.append("ラケットを大きく引いて、肩の回転を意識しましょう")
                    practice_suggestions.append("シャドースイングで正しいバックスイングを身につける")
                elif phase == "インパクトフェーズ":
                    technical_points.append("インパクト時の体重移動とラケット面を安定させましょう")
                    practice_suggestions.append("低いネットでのサービス練習")
                elif phase == "フォロースルーフェーズ":
                    technical_points.append("フォロースルーを大きく取り、体の回転を完了させましょう")
                    practice_suggestions.append("フォロースルーを意識したスローモーション練習")
        
        return {
            "overall_advice": overall,
            "technical_points": technical_points[:5],  # 最大5つ
            "practice_suggestions": practice_suggestions[:5],  # 最大5つ
            "enhanced": False
        }
    
    def _generate_enhanced_advice(self, analysis_data: Dict, basic_advice: Dict) -> Dict:
        """ChatGPT APIを使用して詳細なアドバイスを生成"""
        try:
            logger.info("ChatGPT API呼び出し開始")
            
            # 解析データを整理
            total_score = analysis_data.get('total_score', 0)
            phase_analysis = analysis_data.get('phase_analysis', {})
            
            # ChatGPTへの詳細プロンプトを作成
            prompt = self._create_ultra_detailed_prompt(total_score, phase_analysis, basic_advice)
            
            # ChatGPT APIを呼び出し
            ai_response = self._call_chatgpt_api(prompt)
            
            if ai_response:
                logger.info("ChatGPT API呼び出し成功")
                # レスポンスを解析
                enhanced_advice = self._parse_ai_response(ai_response, basic_advice)
                enhanced_advice["enhanced"] = True
                enhanced_advice["full_ai_response"] = ai_response
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
            basic_advice["error"] = f"AI解析でエラーが発生しました: {str(e)}"
            return basic_advice
    
    def _call_chatgpt_api(self, prompt: str) -> str:
        """ChatGPT APIを呼び出し"""
        try:
            if self.client:
                # OpenAI v1.0+ 対応
                logger.info("OpenAI v1.0+ APIを使用")
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": """あなたは20年以上の経験を持つプロテニスコーチです。テニスサービスの動作解析の専門家として、以下の専門知識を持っています：

1. バイオメカニクス（運動力学）の深い理解
2. 身体各部位の最適な角度と動作タイミング
3. プロ選手のフォーム分析経験
4. 段階的な技術向上プログラムの設計
5. 個人の身体的特徴に応じた指導法

解析結果に基づいて、現在のフォームと理想のフォームの具体的な違いを明示し、段階的な改善方法を提供してください。特に以下の点を重視してください：
- 現在の状態と理想の状態の明確な比較
- なぜその修正が必要なのかの科学的根拠
- 具体的な数値目標（角度、タイミングなど）
- 段階的な改善ステップ
- 毎日の練習での確認方法

日本語で、プロレベルの詳細さで回答してください。"""
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
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": """あなたは20年以上の経験を持つプロテニスコーチです。現在のフォームと理想のフォームの違いを明示し、具体的な改善方法を提供してください。日本語で、プロレベルの詳細さで回答してください。"""
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
            raise e
    
    def _create_ultra_detailed_prompt(self, total_score: float, phase_analysis: Dict, basic_advice: Dict) -> str:
        """超詳細なプロンプトを作成"""
        prompt = f"""
【テニスサービス動作解析結果】

総合スコア: {total_score}/10

フェーズ別詳細スコア:
"""
        
        for phase, data in phase_analysis.items():
            score = data.get('score', 0)
            prompt += f"- {phase}: {score}/10\n"
        
        prompt += f"""

基本評価:
- 総合評価: {basic_advice.get('overall_advice', '')}
- 主要改善点: {', '.join(basic_advice.get('technical_points', []))}

【詳細アドバイス要求】

以下の形式で、現在のフォームと理想のフォームを比較した超詳細なアドバイスを提供してください：

## 1. 現在フォーム vs 理想フォーム 詳細比較分析

### 肘の分析
**現在の状態:**
- 準備時の肘の角度: 現在○○度 → 問題点を具体的に指摘
- バックスイング時の肘の位置: 現在の位置と問題点
- インパクト時の肘の伸展: 現在のタイミングと角度の問題

**理想的な状態:**
- 準備時の肘の角度: 理想○○度 → なぜこの角度が最適なのか理由も説明
- バックスイング時の肘の位置: 理想的な位置と効果
- インパクト時の肘の伸展: 理想的なタイミングと角度

**現在→理想への具体的改善方法:**
1. ステップ1: まず○○を意識して練習
2. ステップ2: 次に○○を調整
3. ステップ3: 最終的に○○を完成させる
4. 確認方法: ○○で正しくできているかチェック

### 膝の分析
**現在の状態:**
- スタンス時の膝の曲がり具合: 現在○○度 → 問題点
- 体重移動時の膝の動き: 現在の動きの問題
- インパクト時の膝の状態: 現在の状態と改善点

**理想的な状態:**
- スタンス時の膝の曲がり具合: 理想○○度 → 効果と理由
- 体重移動時の膝の動き: 理想的な動きとパワー伝達
- インパクト時の膝の状態: 理想的な状態と安定性

**現在→理想への具体的改善方法:**
1. 膝の角度修正: ○○の練習で改善
2. 体重移動練習: ○○を意識した練習
3. 安定性向上: ○○のトレーニング
4. 確認方法: ○○で進歩をチェック

### 手首の分析
**現在の状態:**
- グリップ時の手首角度: 現在○○度 → 問題点
- インパクト時の手首の固定: 現在の状態と課題
- フォロースルー時の手首の動き: 現在の動きの問題

**理想的な状態:**
- グリップ時の手首角度: 理想○○度 → コントロール向上の理由
- インパクト時の手首の固定: 理想的な固定とパワー伝達
- フォロースルー時の手首の動き: 理想的な動きと効果

**現在→理想への具体的改善方法:**
1. グリップ調整: ○○の方法で修正
2. 固定練習: ○○の練習で安定化
3. 動き改善: ○○を意識した練習
4. 確認方法: ○○で正確性をチェック

### 肩・腰の分析
**現在の状態:**
- 肩の回転角度: 現在○○度 → 不足している回転
- 腰の回転タイミング: 現在のタイミングの問題
- 体幹の安定性: 現在の安定性の課題
- 重心移動の軌道: 現在の軌道の問題点

**理想的な状態:**
- 肩の回転角度: 理想○○度 → パワー最大化の理由
- 腰の回転タイミング: 理想的なタイミングと連動効果
- 体幹の安定性: 理想的な安定性とコントロール
- 重心移動の軌道: 理想的な軌道と効率性

**現在→理想への具体的改善方法:**
1. 回転角度向上: ○○の練習で改善
2. タイミング調整: ○○を意識した練習
3. 安定性強化: ○○のトレーニング
4. 軌道修正: ○○の練習で改善
5. 確認方法: ○○で連動性をチェック

## 2. 問題点の優先順位と段階的改善プラン

### 最優先改善点（第1週-第2週）
1. **最も重要な問題**: ○○の修正
   - 現在の状態: ○○
   - 理想の状態: ○○
   - 改善方法: ○○
   - 1日の練習時間: ○○分
   - 確認方法: ○○

### 第2優先改善点（第3週-第4週）
2. **次に重要な問題**: ○○の修正
   - 現在の状態: ○○
   - 理想の状態: ○○
   - 改善方法: ○○
   - 1日の練習時間: ○○分
   - 確認方法: ○○

### 第3優先改善点（第5週-第6週）
3. **さらなる向上**: ○○の修正
   - 現在の状態: ○○
   - 理想の状態: ○○
   - 改善方法: ○○
   - 1日の練習時間: ○○分
   - 確認方法: ○○

## 3. 具体的な「修正前→修正後」の変化目標

### 数値で見る改善目標
- 肘の角度: 現在○○° → 目標○○° (差○○°の改善)
- 膝の曲がり: 現在○○° → 目標○○° (差○○°の改善)
- 手首の角度: 現在○○° → 目標○○° (差○○°の改善)
- 肩の回転: 現在○○° → 目標○○° (差○○°の改善)
- サービス成功率: 現在○○% → 目標○○% (○○%向上)
- スピード: 現在推定○○km/h → 目標○○km/h (○○km/h向上)

### 週ごとの進歩確認チェックリスト
**第1週チェック項目:**
- [ ] ○○ができるようになった
- [ ] ○○の角度が○○度改善された
- [ ] ○○の動きがスムーズになった

**第2週チェック項目:**
- [ ] ○○ができるようになった
- [ ] ○○の連動が改善された
- [ ] ○○の安定性が向上した

## 4. 「なぜその修正が必要なのか」の科学的根拠

### バイオメカニクス的説明
- ○○を修正する理由: 運動力学的に○○の効果があるため
- ○○の角度が重要な理由: ○○の力学的原理により○○が向上
- ○○のタイミングが重要な理由: ○○の連鎖反応により○○が最大化

### プロ選手との比較
- プロ選手の○○: 平均○○度
- あなたの現在の○○: ○○度
- 差を埋める方法: ○○の練習により○○を改善

## 5. 毎日の練習での「修正確認方法」

### 自己チェック方法
1. **鏡を使った確認**: ○○の角度を鏡で確認
2. **動画撮影確認**: ○○の動きを動画で確認
3. **感覚的確認**: ○○の感覚で正しさを確認
4. **数値測定**: ○○を測定して進歩を確認

### 他者チェック方法
1. **コーチ確認**: ○○をコーチに確認してもらう
2. **仲間確認**: ○○を練習仲間に確認してもらう
3. **動画分析**: ○○を第三者に分析してもらう

この詳細な比較分析により、現在のフォームの具体的な問題点と、理想のフォームとの差、そしてその差を埋めるための段階的な改善方法が明確になります。毎日の練習で意識すべきポイントが具体的に分かるため、効率的な上達が期待できます。
"""
        
        return prompt
    
    def _parse_ai_response(self, ai_response: str, basic_advice: Dict) -> Dict:
        """AI応答を解析して構造化"""
        try:
            return {
                "overall_advice": basic_advice.get('overall_advice', ''),
                "technical_points": basic_advice.get('technical_points', []),
                "practice_suggestions": basic_advice.get('practice_suggestions', []),
                "enhanced": True,
                "full_ai_response": ai_response
            }
            
        except Exception as e:
            logger.error(f"AI応答解析エラー: {e}")
            basic_advice["enhanced"] = True
            basic_advice["full_ai_response"] = ai_response
            return basic_advice
    
    def _generate_fallback_advice(self) -> Dict:
        """フォールバック用の基本アドバイス"""
        return {
            "overall_advice": "動作解析を完了しました。基本的なフォーム改善から始めましょう。",
            "technical_points": [
                "正しいスタンスを身につける",
                "安定したトスを練習する",
                "体重移動を意識する"
            ],
            "practice_suggestions": [
                "毎日のシャドースイング練習",
                "壁打ちでの基本練習",
                "トスの反復練習"
            ],
            "enhanced": False
        }

# 使用例とテスト関数
def test_advice_generator():
    """アドバイス生成器のテスト"""
    # テストデータ
    test_data = {
        'total_score': 6.5,
        'phase_analysis': {
            '準備フェーズ': {'score': 7.0},
            'トスフェーズ': {'score': 5.5},
            'バックスイングフェーズ': {'score': 6.0},
            'インパクトフェーズ': {'score': 7.5},
            'フォロースルーフェーズ': {'score': 6.5}
        }
    }
    
    # 基本アドバイスのテスト
    generator = AdviceGenerator()
    basic_advice = generator.generate_advice(test_data, use_chatgpt=False)
    print("基本アドバイス:")
    print(json.dumps(basic_advice, ensure_ascii=False, indent=2))
    
    return basic_advice

if __name__ == "__main__":
    test_advice_generator()

