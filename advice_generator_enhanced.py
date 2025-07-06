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
    
    def _generate_enhanced_advice(self, analysis_data: Dict, basic_advice: Dict) -> Dict:
        """ChatGPTを使用して超詳細なテニスコーチングアドバイスを生成"""
        try:
            total_score = analysis_data.get('total_score', 0)
            phase_analysis = analysis_data.get('phase_analysis', {})
            frame_count = analysis_data.get('frame_count', 0)
            
            # 超詳細なプロンプトを作成
            prompt = self._create_world_class_coaching_prompt(total_score, phase_analysis, basic_advice, frame_count)
            
            # ChatGPT APIを呼び出し（GPT-4o使用）
            if self.client:  # OpenAI v1.0+
                response = self.client.chat.completions.create(
                    model="gpt-4o",  # 最新のGPT-4o使用
                    messages=[
                        {"role": "system", "content": """あなたは世界最高レベルのテニスコーチです。以下の専門性を持っています：

🏆 **経歴・実績**
- ATP/WTAツアーで30年以上の指導経験
- グランドスラム優勝者を複数指導
- 世界ランキング1位選手のコーチ経験

🔬 **専門知識**
- スポーツ科学博士号（バイオメカニクス専門）
- 動作解析の世界的権威
- 個別化トレーニングプログラムの開発者

科学的根拠に基づく詳細な技術指導を提供してください。"""},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=3000,  # GPT-4oはより長いコンテキストに対応
                    temperature=0.7
                )
                ai_advice = response.choices[0].message.content
            else:  # OpenAI v0.x
                import openai
                response = openai.ChatCompletion.create(
                    model="gpt-4o",  # 最新のGPT-4o使用
                    messages=[
                        {"role": "system", "content": "あなたは世界最高レベルのテニスコーチです。科学的根拠に基づく詳細な技術指導を提供してください。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=3000,  # GPT-4oはより長いコンテキストに対応
                    temperature=0.7
                )
                ai_advice = response.choices[0].message.content
            
            logger.info("ChatGPT詳細アドバイス生成成功")
            
            # 基本アドバイスにChatGPTの詳細アドバイスを追加
            enhanced_advice = basic_advice.copy()
            enhanced_advice.update({
                'enhanced': True,
                'detailed_advice': ai_advice,
                'full_ai_response': ai_advice,
                'coaching_level': 'world_class',
                'personalized': True,
                'scientific_analysis': True
            })
            
            return enhanced_advice
            
        except Exception as e:
            logger.error(f"ChatGPT詳細アドバイス生成エラー: {e}")
            # エラー時は基本アドバイスを返す
            basic_advice['enhanced'] = False
            basic_advice['error'] = f"ChatGPT接続エラー: {str(e)}"
            return basic_advice
    
    def _create_world_class_coaching_prompt(self, total_score: float, phase_analysis: Dict, basic_advice: Dict, frame_count: int) -> str:
        """世界クラスのコーチング用プロンプトを作成"""
        
        # フェーズ別詳細データを整理
        phase_details = ""
        critical_phases = []
        excellent_phases = []
        
        for phase, data in phase_analysis.items():
            score = data.get('score', 0)
            feedback = data.get('feedback', '')
            phase_details += f"- **{phase}**: {score}/10 - {feedback}\n"
            
            if score < 5:
                critical_phases.append(f"{phase}({score}/10)")
            elif score >= 8.5:
                excellent_phases.append(f"{phase}({score}/10)")
        
        skill_level = self._get_detailed_skill_assessment(total_score)
        
        prompt = f"""# 🎾 世界クラステニスコーチング依頼

## 📊 選手プロフィール分析
- **総合技術レベル**: {total_score}/10 ({skill_level})
- **解析フレーム数**: {frame_count}フレーム
- **優秀なフェーズ**: {', '.join(excellent_phases) if excellent_phases else '特に突出したフェーズなし'}
- **緊急改善フェーズ**: {', '.join(critical_phases) if critical_phases else '致命的な問題なし'}

## 🔬 詳細技術データ
{phase_details}

## 🎯 現在の基本評価
- **総合所見**: {basic_advice.get('overall_advice', '')}
- **主要課題**: {', '.join(basic_advice.get('technical_points', []))}

---

# 🏆 世界レベルコーチングプログラム作成依頼

あなたは**錦織圭、大坂なおみクラスの選手を指導する世界最高峰のコーチ**として、この選手を次のレベルに引き上げる完全なプログラムを作成してください。

## 📋 求める指導内容

### 1. 🔬 バイオメカニクス完全分析（各項目500文字）

#### A. 運動連鎖の科学的分析
**現在の問題点と理想状態の比較**
- **地面反力の活用効率**: 現在○%→理想95%以上（世界トップレベル）
- **エネルギー伝達ロス**: 現在○%のロス→理想5%以下
- **回転軸の安定性**: 現在のブレ○度→理想±2度以内
- **タイミング同期率**: 現在○%→理想90%以上

#### B. 身体各部位の精密分析

**🦵 下半身（膝・足・重心）**
- **膝の角度変化**: 
  - 準備時: 現在○度 → 理想155-165度（フェデラー基準）
  - インパクト時: 現在○度 → 理想170-180度
  - なぜこの角度が最適なのか科学的根拠を説明
- **足幅とスタンス**: 
  - 現在○cm → 理想肩幅+10cm（身長比1.2倍）
  - 体重配分: 現在後足○%→理想後足60%→前足70%
- **重心移動軌道**: 
  - 現在の軌道の問題点と理想的な放物線軌道
  - 移動速度: 現在○秒 → 理想0.3-0.4秒

**🏋️ 体幹（肩・腰・背中）**
- **肩の回転角度**: 
  - 現在○度 → 理想90-110度（ジョコビッチレベル）
  - 回転開始タイミング: 現在より○秒早く/遅く
- **腰の回転連動**: 
  - 現在の腰→肩の時間差○秒 → 理想0.1-0.15秒
  - 回転軸のブレ: 現在○度 → 理想±3度以内
- **背中の反り**: 
  - 現在○度 → 理想15-25度（パワー最大化）

**💪 上半身（肘・手首・ラケット）**
- **肘の軌道分析**: 
  - 準備時高さ: 現在肩基準○cm → 理想+8-12cm
  - バックスイング最下点: 現在○cm → 理想腰レベル-5cm
  - インパクト時伸展: 現在○度 → 理想95-98%伸展
- **手首の角度制御**: 
  - グリップ時: 現在○度 → 理想15-20度（背屈）
  - インパクト時: 現在○度 → 理想±5度以内の安定
- **ラケット面コントロール**: 
  - 現在の面ブレ○度 → 理想±3度以内
  - インパクト時の面角度: 現在○度 → 理想垂直±2度

**🎾 トス技術の精密分析**
- **高さ制御**: 
  - 現在○cm → 理想最高到達点+30cm（ラケット長基準）
  - 高さのばらつき: 現在±○cm → 理想±3cm以内
- **位置精度**: 
  - 前方: 現在○cm → 理想12-15cm（身長比）
  - 右側: 現在○cm → 理想5-8cm
  - 位置のばらつき: 現在±○cm → 理想±2cm以内
- **リリース技術**: 
  - 手首角度: 現在○度 → 理想90度固定
  - 指先コントロール: 現在の問題点と改善方法

### 2. 🏅 世界トップ選手との詳細比較

| 技術要素 | あなた | フェデラー | ジョコビッチ | ナダル | サンプラス | 改善目標 |
|---------|--------|-----------|-------------|--------|-----------|----------|
| 膝角度(準備) | ○度 | 160度 | 165度 | 155度 | 158度 | ○度に調整 |
| 肘高さ | ○cm | +10cm | +12cm | +8cm | +9cm | ○cm上げる |
| 肩回転角度 | ○度 | 105度 | 110度 | 95度 | 100度 | ○度に拡大 |
| 体重移動速度 | ○秒 | 0.35秒 | 0.30秒 | 0.40秒 | 0.32秒 | ○秒に短縮 |
| トス精度 | ±○cm | ±2cm | ±1.5cm | ±3cm | ±2.5cm | ±○cmに向上 |
| 回転軸安定性 | ±○度 | ±2度 | ±1.5度 | ±3度 | ±2.5度 | ±○度に改善 |

### 3. 🎯 段階的マスタープログラム（16週間）

#### 🔥 フェーズ1（1-4週）：基礎技術革命期
**目標**: 最重要課題の根本的改善

**第1週：診断と基礎固め**
- **月曜日**: 膝角度修正集中練習（90分）
  - ウォームアップ: 動的ストレッチ15分
  - 膝角度確認練習: 鏡前で正しい角度を体感30分
  - シャドースイング: 正しい膝角度で100回
  - 壁打ち: 膝角度意識で200球
  - クールダウン: 静的ストレッチ15分
  - **確認ポイント**: 膝角度が○度になっているか毎回チェック

- **火曜日**: 肘の軌道修正（90分）
  - [詳細なメニュー]

- **水曜日**: 体幹安定化トレーニング（90分）
  - [詳細なメニュー]

- **木曜日**: トス精度向上（90分）
  - [詳細なメニュー]

- **金曜日**: 統合練習（90分）
  - [詳細なメニュー]

- **土曜日**: 実戦形式練習（120分）
  - [詳細なメニュー]

- **日曜日**: 回復とメンタル強化（60分）
  - [詳細なメニュー]

**第2週〜第4週**: [同様に詳細な週別プログラム]

#### ⚡ フェーズ2（5-8週）：技術統合期
#### 🚀 フェーズ3（9-12週）：実戦応用期
#### 🏆 フェーズ4（13-16週）：マスター完成期

### 4. 🏋️ 専門フィジカル強化プログラム

#### A. 下半身パワー強化（週4回）
- **スクワット系**: ○○kg×○回×○セット
- **ランジ系**: ○○kg×○回×○セット
- **プライオメトリクス**: ○○×○回×○セット
- **バランス強化**: ○○秒×○セット

#### B. 体幹安定化（毎日）
- **プランク系**: ○○秒×○セット
- **回転系**: ○○回×○セット
- **抗回転系**: ○○秒×○セット

#### C. 上半身連動性（週3回）
- **肩甲骨可動域**: ○○回×○セット
- **ローテーターカフ**: ○○kg×○回×○セット
- **連動性ドリル**: ○○回×○セット

### 5. 🧠 メンタル・戦術強化

#### A. 集中力向上プログラム
- **ルーティン確立**: ○○の手順を毎回実行
- **呼吸法**: ○○呼吸を○回
- **イメージトレーニング**: ○○を○分間

#### B. 実戦での確認システム
**練習中のチェックリスト**
- [ ] 膝角度: ○度をキープ
- [ ] 肘高さ: 肩より○cm高い位置
- [ ] トス位置: 前方○cm、右側○cm
- [ ] 体重移動: ○秒で完了
- [ ] ラケット面: 垂直±○度以内

### 6. 📈 進歩測定システム

#### 週間評価指標
- **技術精度**: ○○の成功率○%以上
- **パワー指標**: ○○の数値○以上
- **安定性**: ○○のばらつき±○以内

#### 月間目標
- **1ヶ月後**: 総合スコア{total_score} → ○点
- **2ヶ月後**: ○○の習得完了
- **3ヶ月後**: 実戦レベル到達
- **4ヶ月後**: 上級者レベル到達

### 7. 🚨 重要注意事項

#### よくある失敗パターンと対策
1. **○○の間違い**: 
   - 症状: ○○
   - 原因: ○○
   - 対策: ○○
   - 確認方法: ○○

#### 怪我予防プロトコル
- **ウォームアップ**: 必須○分間
- **クールダウン**: 必須○分間
- **危険サイン**: ○○を感じたら即中止
- **回復方法**: ○○

### 8. 🎪 実戦投入プロトコル

#### 段階的実戦導入
- **練習試合**: ○週目から開始
- **公式戦**: ○週目から投入
- **成功基準**: ○○の達成

---

**重要指示**: 
1. 全ての数値は具体的に記載し、科学的根拠も併記
2. この選手のレベル（{total_score}/10）に最適化
3. 実践的で明日から実行可能な内容
4. 世界トップレベルを目指す高い基準設定
5. 段階的で無理のない進歩プログラム

Markdown形式で、見やすく構造化して回答してください。"""

        return prompt
    
    def _get_detailed_skill_assessment(self, total_score: float) -> str:
        """詳細なスキルレベル評価を取得"""
        if total_score >= 9.0:
            return "世界トップレベル（プロツアー上位）"
        elif total_score >= 8.0:
            return "プロレベル（国内トップクラス）"
        elif total_score >= 7.0:
            return "上級者レベル（地域大会優勝クラス）"
        elif total_score >= 6.0:
            return "中上級者レベル（クラブ上位）"
        elif total_score >= 5.0:
            return "中級者レベル（基本技術習得済み）"
        elif total_score >= 4.0:
            return "初中級者レベル（基礎練習中）"
        else:
            return "初級者レベル（基礎から要習得）"
    
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
            "summary": overall,
            "improvements": technical_points[:5],
            "drills": practice_suggestions[:5],
            "enhanced": False
        }
    
    def _generate_fallback_advice(self) -> Dict:
        """フォールバック用の基本アドバイス"""
        return {
            "summary": "解析が完了しました。基本的なサービスフォームの確認を行いましょう。",
            "improvements": [
                "正しいスタンスを確認しましょう",
                "トスの安定性を向上させましょう",
                "体重移動を意識しましょう"
            ],
            "drills": [
                "毎日のシャドースイング練習",
                "壁打ちでの基礎練習",
                "トスの反復練習"
            ],
            "enhanced": False,
            "error": "詳細分析でエラーが発生しました"
        }

