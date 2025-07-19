import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import {
  Upload,
  Play,
  BarChart3,
  Loader2,
  CheckCircle,
  AlertCircle,
  Sparkles,
  Settings,
  Eye,
  EyeOff,
  ChevronDown,
  ChevronUp,
  Trophy,
  Target,
  Users,
  BookOpen,
  Calendar,
  Brain,
  MessageCircle,
  Camera,
  Zap,
  Share2
} from 'lucide-react';
import './App.css';

const API_BASE_URL = 'https://tennis-serve-analyzer.onrender.com';

function App() {
  const [showGuide, setShowGuide] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const [useChatGPT, setUseChatGPT] = useState(false);
  const [userConcerns, setUserConcerns] = useState('');
  const [userLevel, setUserLevel] = useState('intermediate');
  const [focusAreas, setFocusAreas] = useState([]);
  const fileInputRef = useRef(null);

  const steps = [
    { id: 1, title: '動画選択', icon: Upload },
    { id: 2, title: '解析実行', icon: Play },
    { id: 3, title: '結果確認', icon: BarChart3 }
  ];

  // 技術レベルの選択肢
  const skillLevels = [
    { value: 'beginner', label: '初心者', icon: BookOpen, description: 'テニスを始めたばかり、基本を学びたい' },
    { value: 'intermediate', label: '中級者', icon: Target, description: '基本はできるが、さらに上達したい' },
    { value: 'advanced', label: '上級者', icon: Users, description: '高いレベルでプレー、細かい技術を磨きたい' },
    { value: 'professional', label: 'プロレベル', icon: Trophy, description: 'プロまたはプロ級の技術レベル' }
  ];

  // 重点解析エリアの選択肢
  const focusAreaOptions = [
    { id: 'serve_motion', label: 'サーブ動作' },
    { id: 'toss', label: 'トス' },
    { id: 'follow_through', label: 'フォロースルー' },
    { id: 'body_rotation', label: '体の回転' }
  ];

  // 重点エリアの切り替え
  const toggleFocusArea = (areaId) => {
    setFocusAreas(prev => 
      prev.includes(areaId) 
        ? prev.filter(id => id !== areaId)
        : [...prev, areaId]
    );
  };

  // フェーズ名の日本語変換
  const getPhaseNameInJapanese = (phase) => {
    const phaseMap = {
      'preparation': '準備',
      'toss_up': 'トスアップ',
      'backswing': 'バックスイング',
      'forward_swing': 'フォワードスイング',
      'impact': 'インパクト',
      'follow_through': 'フォロースルー'
    };
    return phaseMap[phase] || phase;
  };

  // 最高スコアと最低スコアのフェーズを取得
  const getBestAndWorstPhases = (phaseAnalysis) => {
    if (!phaseAnalysis) return { best: null, worst: null };
    
    const phases = Object.entries(phaseAnalysis).map(([phase, data]) => ({
      phase,
      score: data.score || 7.0,
      name: getPhaseNameInJapanese(phase)
    }));
    
    const sortedPhases = phases.sort((a, b) => b.score - a.score);
    return {
      best: sortedPhases[0],
      worst: sortedPhases[sortedPhases.length - 1]
    };
  };

  // SNS共有機能
  const shareToTwitter = () => {
    if (!analysisResult) return;
    
    const score = analysisResult.tiered_evaluation?.total_score || analysisResult.overall_score || 0;
    const text = `テニスサーブ解析結果: ${score}/10点 🎾\n\n#テニス #サーブ解析 #TossUp`;
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank');
  };

  const shareToInstagram = () => {
    // Instagram Web版は直接投稿できないため、アプリを開く
    const url = 'https://www.instagram.com/';
    window.open(url, '_blank');
  };

  const shareToTikTok = () => {
    if (!analysisResult) return;
    
    const score = analysisResult.tiered_evaluation?.total_score || analysisResult.overall_score || 0;
    const text = `テニスサーブ解析結果: ${score}/10点 🎾 #テニス #サーブ解析 #TossUp`;
    // TikTokのWeb版を開く
    const url = `https://www.tiktok.com/`;
    window.open(url, '_blank');
  };

  // マークダウンテキストをフォーマットする関数（マークダウン記法を除去）
  const formatAIResponse = (text) => {
    if (!text) return null;
    
    const lines = text.split('\n');
    const elements = [];
    let currentSection = [];
    
    lines.forEach((line, index) => {
      const trimmedLine = line.trim();
      
      if (trimmedLine.startsWith('## ')) {
        // 前のセクションを追加
        if (currentSection.length > 0) {
          elements.push(
            <div key={`section-${elements.length}`} className="mb-6">
              {currentSection}
            </div>
          );
          currentSection = [];
        }
        // 大見出し（##を除去）
        elements.push(
          <h2 key={`h2-${index}`} className="text-2xl font-bold text-blue-800 mb-4 mt-8 border-b-2 border-blue-200 pb-2">
            {trimmedLine.replace('## ', '')}
          </h2>
        );
      } else if (trimmedLine.startsWith('### ')) {
        // 中見出し（###を除去）
        currentSection.push(
          <h3 key={`h3-${index}`} className="text-xl font-semibold text-green-700 mb-3 mt-6">
            {trimmedLine.replace('### ', '')}
          </h3>
        );
      } else if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**')) {
        // 太字見出し（**を除去）
        currentSection.push(
          <h4 key={`h4-${index}`} className="text-lg font-semibold text-purple-700 mb-2 mt-4">
            {trimmedLine.replace(/\*\*/g, '')}
          </h4>
        );
      } else if (trimmedLine.includes('**')) {
        // 行内の太字記法を除去
        const cleanText = trimmedLine.replace(/\*\*/g, '');
        currentSection.push(
          <p key={`p-${index}`} className="text-gray-700 leading-relaxed mb-3">
            {cleanText}
          </p>
        );
      } else if (trimmedLine.startsWith('- ')) {
        // リスト項目
        currentSection.push(
          <div key={`li-${index}`} className="flex items-start mb-2">
            <span className="text-blue-500 mr-2 mt-1">•</span>
            <span className="text-gray-700">{trimmedLine.substring(2)}</span>
          </div>
        );
      } else if (trimmedLine) {
        // 通常のテキスト
        currentSection.push(
          <p key={`p-${index}`} className="text-gray-700 leading-relaxed mb-3">
            {trimmedLine}
          </p>
        );
      }
    });
    
    // 最後のセクションを追加
    if (currentSection.length > 0) {
      elements.push(
        <div key={`section-${elements.length}`} className="mb-6">
          {currentSection}
        </div>
      );
    }
    
    return elements;
  };

  // デバッグ用のuseEffect
  useEffect(() => {
    console.log('🔍 状態変化検出:');
    console.log('- currentStep:', currentStep);
    console.log('- analysisResult:', analysisResult ? '存在' : 'null');
    console.log('- isAnalyzing:', isAnalyzing);
    console.log('- error:', error);
    console.log('- userLevel:', userLevel);
  }, [currentStep, analysisResult, isAnalyzing, error, userLevel]);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setCurrentStep(2);
      setError(null);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('video/')) {
      setSelectedFile(file);
      setCurrentStep(2);
      setError(null);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setError(null);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('video', selectedFile);
      formData.append('use_chatgpt', useChatGPT ? 'true' : 'false');
      formData.append('user_concerns', userConcerns);
      formData.append('user_level', userLevel);
      formData.append('focus_areas', JSON.stringify(focusAreas));
      if (useChatGPT && apiKey) {
        formData.append('api_key', apiKey);
      }

      console.log('🚀 解析開始:');
      console.log('- userLevel:', userLevel);
      console.log('- useChatGPT:', useChatGPT);
      console.log('- userConcerns:', userConcerns);
      console.log('- focusAreas:', focusAreas);

      const response = await axios.post(`${API_BASE_URL}/api/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        },
      });

      // デバッグ: レスポンスデータの確認
      console.log('=== フロントエンド レスポンス受信 ===');
      console.log('response.status:', response.status);
      console.log('response.data:', response.data);
      console.log('response.data.success:', response.data?.success);
      console.log('response.data.result:', response.data?.result);
      console.log('overlay_images:', response.data.result.overlay_images);

      
      // 重要: スコアデータの詳細確認
      if (response.data?.result) {
        console.log('🎯 スコアデータ詳細確認:');
        console.log('total_score:', response.data.result.total_score);
        console.log('phase_analysis:', response.data.result.phase_analysis);
        console.log('tiered_evaluation:', response.data.result.tiered_evaluation);
        
        if (response.data.result.phase_analysis) {
          Object.entries(response.data.result.phase_analysis).forEach(([phase, data]) => {
            console.log(`${phase}: ${data.score}`);
          });
        }
      }
      
      if (response.data?.result?.advice) {
        console.log('advice keys:', Object.keys(response.data.result.advice));
      }
      console.log('=====================================');

      if (response.data.success) {
        setAnalysisResult(response.data.result);
        setCurrentStep(3);
      } else {
        throw new Error(response.data.error || '解析に失敗しました');
      }
    } catch (err) {
      console.error('解析エラー:', err);
      setError(err.response?.data?.error || err.message || '解析中にエラーが発生しました');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetAnalysis = () => {
    setCurrentStep(1);
    setSelectedFile(null);
    setAnalysisResult(null);
    setError(null);
    setIsAnalyzing(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* ヘッダー */}
      <header className="modern-header">
        <div className="header-container">
          <div className="header-brand">
            <img src="/tossup-icon.png" alt="TossUp" className="header-logo" />
            <div className="header-text">
              <h1 className="header-title">TossUp</h1>
              <p className="header-subtitle">Tennis Serve Analyzer</p>
            </div>
          </div>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="settings-button"
          >
            <Settings className="w-5 h-5" />
            <span className="settings-text">設定</span>
            {showSettings ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </header>

      {/* 👇 ここにガイドボタン */}
      <div style={{display: "flex", justifyContent: "center"}}>
        <button onClick={() => setShowGuide(true)} className="guide-btn">
          📸 撮影ガイドを見る
        </button>
      </div>




      {/* メインコンテンツ */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 詳細設定パネル */}
        {showSettings && (
          <div className="mb-8 unified-card">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">詳細設定</h3>
            
            {/* ChatGPT設定 */}
            <div className="mb-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={useChatGPT}
                  onChange={(e) => setUseChatGPT(e.target.checked)}
                  className="mr-2"
                />
                <span className="text-gray-700">ChatGPT詳細アドバイスを使用</span>
              </label>
            </div>

            {/* APIキー入力 */}
            {useChatGPT && (
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  OpenAI APIキー
                </label>
                <div className="relative">
                  <input
                    type={showApiKey ? 'text' : 'password'}
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="sk-..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    type="button"
                    onClick={() => setShowApiKey(!showApiKey)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* プログレスバー */}
        <div className="progress-container">
          <div className="progress-track">
            {steps.map((step, index) => (
              <React.Fragment key={step.id}>
                <div className="progress-step-wrapper">
                  <div className={`progress-step ${
                    currentStep >= step.id ? 'progress-step-active' : 'progress-step-inactive'
                  }`}>
                    <div className="progress-step-icon">
                      <step.icon className="w-4 h-4" />
                    </div>
                    <span className="progress-step-number">{step.id}</span>
                  </div>
                  <div className="progress-step-label">
                    <span className={`progress-step-title ${
                      currentStep >= step.id ? 'progress-step-title-active' : 'progress-step-title-inactive'
                    }`}>
                      {step.title}
                    </span>
                  </div>
                </div>
                {index < steps.length - 1 && (
                  <div className={`progress-connector ${
                    currentStep > step.id ? 'progress-connector-active' : 'progress-connector-inactive'
                  }`} />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* エラー表示 */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start">
              <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <h4 className="text-red-800 font-medium">エラーが発生しました</h4>
                <p className="text-red-700 text-sm mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* ステップ1: ファイル選択 */}
        {currentStep === 1 && (
          <div className="max-w-2xl mx-auto">
            <div className="unified-card">
              <div className="unified-card-header">
                <img src="/tossup-icon.png" alt="TossUp" className="unified-icon" />
                <h2 className="unified-title">動画をアップロード</h2>
              </div>
              
              {/* ドラッグアンドドロップエリア */}
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                className="upload-area"
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="upload-icon" />
                <p className="upload-main-text">
                  ここに動画ファイルをドラッグ&ドロップ
                </p>
                <p className="upload-sub-text">
                  または、クリックしてファイルを選択
                </p>
                <p className="upload-format-text">
                  対応形式: MP4, AVI, MOV, MKV (最大100MB)
                </p>
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="video/*"
                onChange={handleFileSelect}
                className="hidden"
              />
            </div>
          </div>
        )}

        {/* ステップ2: 設定と解析実行 */}
        {currentStep === 2 && (
          <div className="max-w-4xl mx-auto">
            <div className="unified-card">
              <div className="unified-card-header">
                <img src="/tossup-icon.png" alt="TossUp" className="unified-icon" />
                <h2 className="unified-title">解析設定</h2>
              </div>

              {/* 選択されたファイル情報 */}
              {selectedFile && (
                <div className="file-info-card">
                  <p className="file-info-name">
                    <strong>選択されたファイル:</strong> {selectedFile.name}
                  </p>
                  <p className="file-info-size">
                    サイズ: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              )}

              {/* 技術レベル選択 */}
              <div className="setting-section">
                <h3 className="setting-title">
                  <Trophy className="w-6 h-6 text-blue-600 mr-2" />
                  あなたの技術レベル
                </h3>
                <div className="skill-level-grid">
                  {skillLevels.map((level) => {
                    const IconComponent = level.icon;
                    return (
                      <button
                        key={level.value}
                        onClick={() => setUserLevel(level.value)}
                        className={`skill-level-card ${
                          userLevel === level.value ? 'skill-level-card-active' : ''
                        }`}
                      >
                        <div className="skill-level-header">
                          <IconComponent className="w-6 h-6 mr-2" />
                          <span className="skill-level-label">{level.label}</span>
                        </div>
                        <p className="skill-level-description">{level.description}</p>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* 気になっていること入力欄 */}
              <div className="concerns-section">
                <h3 className="concerns-title">
                  <MessageCircle className="w-6 h-6 mr-2" />
                  💭 気になっていることはありますか？
                </h3>
                <p className="concerns-description">
                  あなたの悩みに特化したアドバイスも生成されます（APIキー設定時）
                </p>
                <textarea
                  value={userConcerns}
                  onChange={(e) => setUserConcerns(e.target.value)}
                  placeholder="例：トスが安定しない、フォームが崩れる、パワーが出ない、コントロールが悪い..."
                  className="concerns-textarea"
                  rows="3"
                  maxLength="200"
                />
                <div className="concerns-counter">
                  {userConcerns.length}/200文字
                </div>
              </div>

              {/* 重点解析エリア */}
              <div className="setting-section">
                <h3 className="setting-title">
                  <Target className="w-6 h-6 text-green-600 mr-2" />
                  重点解析エリア（複数選択可）
                </h3>
                <div className="focus-area-grid">
                  {focusAreaOptions.map((area) => (
                    <button
                      key={area.id}
                      onClick={() => toggleFocusArea(area.id)}
                      className={`focus-area-card ${
                        focusAreas.includes(area.id) ? 'focus-area-card-active' : ''
                      }`}
                    >
                      <div className="focus-area-label">{area.label}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* 解析実行ボタン */}
              <div className="action-buttons">
                <button
                  onClick={() => setCurrentStep(1)}
                  className="back-button"
                >
                  ← 戻る
                </button>
                <button
                  onClick={handleAnalyze}
                  disabled={!selectedFile || isAnalyzing}
                  className="analyze-button"
                >
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      解析中... ({uploadProgress}%)
                    </>
                  ) : (
                    <>
                      <Zap className="w-5 h-5 mr-2" />
                      解析開始
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ステップ3: 結果表示 - 新しいスコアカードデザイン */}
        {currentStep === 3 && analysisResult && (
          <div className="space-y-8">
            {/* スコアカード */}
            <div className="max-w-md mx-auto">
              <div className="scorecard">
                {/* ヘッダー */}
                <div className="scorecard-header">
                  <img src="/tossup-icon.png" alt="TossUp" className="scorecard-icon" />
                  <h1 className="scorecard-title">TENNIS SERVE<br />SCORE CARD</h1>
                </div>

                {/* 総合スコア */}
                <div className="scorecard-main-score">
                  <div className="main-score-number">
                    {(analysisResult.tiered_evaluation?.total_score || analysisResult.overall_score || 7.4).toFixed(1)}
                  </div>
                  <div className="main-score-label">SCORE:</div>
                </div>

                {/* ベスト・ワーストフェーズ */}
                {(() => {
                  const { best, worst } = getBestAndWorstPhases(analysisResult.phase_analysis);
                  return (
                    <div className="scorecard-phases">
                      {best && (
                        <div className="phase-item best-phase">
                          <div className="phase-icon">✓</div>
                          <div className="phase-content">
                            <div className="phase-label">Best Phase:</div>
                            <div className="phase-name">{best.name}</div>
                          </div>
                          <div className="phase-score">{best.score.toFixed(1)}</div>
                        </div>
                      )}

                      {worst && (
                        <div className="phase-item needs-work-phase">
                          <div className="phase-icon">⚠</div>
                          <div className="phase-content">
                            <div className="phase-label">Needs Work:</div>
                            <div className="phase-name">{worst.name}</div>
                          </div>
                          <div className="phase-score">{worst.score.toFixed(1)}</div>
                        </div>
                      )}
                    </div>
                  );
                })()}

                {/* SNS共有ボタン */}
                <div className="scorecard-social">
                  <button onClick={shareToTwitter} className="social-btn twitter-btn">
                    <Share2 className="w-5 h-5" />
                  </button>
                  <button onClick={shareToInstagram} className="social-btn instagram-btn">
                    <Camera className="w-5 h-5" />
                  </button>
                  <button onClick={shareToTikTok} className="social-btn tiktok-btn">
                    <Play className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
            
            {/* オーバーレイ画像（縦並び）表示エリア */}
            {analysisResult.overlay_images && analysisResult.overlay_images.length > 0 && (
              <div className="overlay-images-vertical">
               {analysisResult.overlay_images.map((img, i) => (
                 <img
                    key={i}
                    src={`https://tennis-serve-analyzer.onrender.com${img}`}
                    alt={`オーバーレイ画像${i + 1}`}
                    style={{ width: "220px", margin: "0 auto 16px", borderRadius: "8px", boxShadow: "0 2px 8px #0001" }}
                  />
                ))}
              </div>
             )}

            
            {/* 新しい動画を解析ボタン */}
            <div className="text-center">
              <button
                onClick={resetAnalysis}
                className="analyze-button"
              >
                <Upload className="w-5 h-5 mr-2" />
                新しい動画を解析
              </button>
            </div>

            {/* フェーズ別解析（詳細） */}
            {analysisResult.phase_analysis && (
              <div className="unified-card">
                <div className="unified-card-header">
                  <BarChart3 className="w-8 h-8 text-blue-600 mr-3" />
                  <h2 className="unified-title">フェーズ別解析</h2>
                </div>
                <div className="phase-analysis-grid">
                  {Object.entries(analysisResult.phase_analysis).map(([phase, data]) => {
                    console.log(`🎯 フェーズ表示: ${phase} = ${data.score}`);
                    return (
                    <div key={phase} className="phase-analysis-card">
                      <h3 className="phase-analysis-title">{getPhaseNameInJapanese(phase)}</h3>
                      <div className="phase-analysis-score">
                        <div className="phase-analysis-score-number">
                          {data.score ? data.score.toFixed(1) : '7.0'}
                        </div>
                        <div className="phase-analysis-score-max">/10</div>
                      </div>
                      {data.feedback && (
                        <p className="phase-analysis-feedback">{data.feedback}</p>
                      )}
                    </div>
                  )})}
                </div>
              </div>
            )}

            {/* AI詳細アドバイス */}
            {analysisResult.advice && (analysisResult.advice.enhanced || analysisResult.advice.detailed_advice) && (
              <div className="unified-card">
                <div className="unified-card-header">
                  <Brain className="w-8 h-8 text-purple-600 mr-3" />
                  <h2 className="unified-title">AI詳細解析レポート</h2>
                  {analysisResult.advice.enhanced && (
                    <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium ml-auto">
                      ChatGPT生成
                    </span>
                  )}
                </div>
                
                {analysisResult.advice.error && (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                    <div className="flex items-start">
                      <AlertCircle className="w-5 h-5 text-yellow-500 mr-3 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="text-yellow-800 font-medium">ChatGPT接続エラー</h4>
                        <p className="text-yellow-700 text-sm mt-1">{analysisResult.advice.error}</p>
                        <p className="text-yellow-700 text-sm mt-1">基本アドバイスを表示しています。</p>
                      </div>
                    </div>
                  </div>
                )}
                
                <div className="prose max-w-none">
                  {analysisResult.advice.enhanced ? 
                    formatAIResponse(analysisResult.advice.detailed_advice) :
                    <p className="text-gray-700 leading-relaxed">{analysisResult.advice.detailed_advice}</p>
                  }
                </div>
              </div>
            )}

            {/* 基本アドバイス */}
            {analysisResult.advice && analysisResult.advice.basic_advice && (
              <div className="unified-card">
                <div className="unified-card-header">
                  <MessageCircle className="w-8 h-8 text-green-600 mr-3" />
                  <h2 className="unified-title">基本アドバイス</h2>
                </div>
                <div className="text-gray-700 leading-relaxed">
                  {analysisResult.advice.basic_advice}
                </div>
              </div>
            )}

            {/* ワンポイントアドバイス - AI詳細解析レポートがない場合のみ表示 */}
            {analysisResult.advice && analysisResult.advice.one_point_advice && 
             !analysisResult.advice.enhanced && !analysisResult.advice.detailed_advice && (
              <div className="unified-card advice-highlight">
                <div className="unified-card-header">
                  <Sparkles className="w-8 h-8 text-orange-600 mr-3" />
                  <h2 className="unified-title">ワンポイントアドバイス</h2>
                </div>
                <div className="text-orange-800 text-lg leading-relaxed font-medium">
                  {analysisResult.advice.one_point_advice}
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {showGuide && (
        <div className="modal-overlay" onClick={() => setShowGuide(false)}> 
         <div className="modal-content" onClick={e => e.stopPropagation()}>
          <img src="/camera_guide.png" alt="撮影ガイド" style={{width: '90%', maxWidth: 400, marginBottom: 20}} />
           <button
             onClick={() => setShowGuide(false)}
             style={{
             marginTop: 8,
             padding: '8px 24px',
             borderRadius: 6,
             background: '#2D8CFF',
             color: '#fff',
             border: 'none',
             fontWeight: 600
          }}
         >
           閉じる
         </button>
       </div>
      </div>
   )}

    </div>
  );
}

export default App;

