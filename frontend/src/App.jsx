import React, { useState, useRef } from 'react';
import axios from 'axios';
import { 
  Upload, 
  Play, 
  BarChart3, 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  FileVideo,
  TrendingUp,
  Target,
  Award,
  Settings,
  Key,
  X,
  Eye,
  EyeOff,
  Sparkles,
  BookOpen,
  Calendar,
  Brain,
  Camera,
  HelpCircle,
  MessageSquare
} from 'lucide-react';
import './App.css';

const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  const [showCameraGuide, setShowCameraGuide] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const [useChatGPT, setUseChatGPT] = useState(false);
  const [userConcerns, setUserConcerns] = useState('');
  const fileInputRef = useRef(null);

  const steps = [
    { id: 1, title: '動画選択', icon: Upload },
    { id: 2, title: '解析実行', icon: Play },
    { id: 3, title: '結果確認', icon: BarChart3 }
  ];

  // マークダウンテキストをフォーマットする関数
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
        // 大見出し
        elements.push(
          <h2 key={`h2-${index}`} className="text-2xl font-bold text-blue-800 mb-4 mt-8 border-b-2 border-blue-200 pb-2">
            {trimmedLine.replace('## ', '')}
          </h2>
        );
      } else if (trimmedLine.startsWith('### ')) {
        // 中見出し
        currentSection.push(
          <h3 key={`h3-${index}`} className="text-xl font-semibold text-green-700 mb-3 mt-6">
            {trimmedLine.replace('### ', '')}
          </h3>
        );
      } else if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**')) {
        // 太字見出し
        currentSection.push(
          <h4 key={`h4-${index}`} className="text-lg font-semibold text-purple-700 mb-2 mt-4">
            {trimmedLine.replace(/\*\*/g, '')}
          </h4>
        );
      } else if (trimmedLine.startsWith('- ')) {
        // リスト項目
        currentSection.push(
          <div key={`li-${index}`} className="flex items-start mb-2">
            <span className="text-blue-500 mr-2 mt-1">•</span>
            <span className="text-gray-700 leading-relaxed">{trimmedLine.replace('- ', '')}</span>
          </div>
        );
      } else if (trimmedLine.match(/^\d+\./)) {
        // 番号付きリスト
        currentSection.push(
          <div key={`ol-${index}`} className="flex items-start mb-2">
            <span className="text-green-600 mr-2 mt-1 font-semibold">{trimmedLine.match(/^\d+\./)[0]}</span>
            <span className="text-gray-700 leading-relaxed">{trimmedLine.replace(/^\d+\.\s*/, '')}</span>
          </div>
        );
      } else if (trimmedLine.includes('**')) {
        // 行内の太字を処理
        const parts = trimmedLine.split('**');
        const formattedParts = parts.map((part, i) => 
          i % 2 === 1 ? <strong key={i} className="font-semibold text-gray-800">{part}</strong> : part
        );
        currentSection.push(
          <p key={`p-${index}`} className="text-gray-700 leading-relaxed mb-3">
            {formattedParts}
          </p>
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
      if (useChatGPT && apiKey) {
        formData.append('api_key', apiKey);
      }
      if (useChatGPT && userConcerns) {
        formData.append('user_concerns', userConcerns);
      }

      const response = await axios.post(`${API_BASE_URL}/api/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        },
      });

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
    setUserConcerns('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* ヘッダー */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Award className="w-8 h-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">テニスサーブ解析システム</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowCameraGuide(!showCameraGuide)}
                className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Camera className="w-5 h-5 mr-2" />
                撮影ガイド
              </button>
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Settings className="w-5 h-5 mr-2" />
                設定
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* メインコンテンツ */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 撮影ガイドパネル */}
        {showCameraGuide && (
          <div className="mb-8 bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800 flex items-center">
                <Camera className="w-6 h-6 text-blue-600 mr-2" />
                撮影ガイド
              </h3>
              <button
                onClick={() => setShowCameraGuide(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* 撮影位置ガイド */}
              <div>
                <h4 className="text-md font-semibold text-gray-700 mb-3">理想的な撮影位置</h4>
                <img 
                  src="/tennis_serve_trophy_pose.png" 
                  alt="テニスサーブ撮影位置ガイド"
                  className="w-full rounded-lg border border-gray-200"
                />
                <div className="mt-3 text-sm text-gray-600">
                  <p><strong>推奨:</strong> 斜め後方からの撮影（ベースラインに対して45度、3-4メートル離れて）</p>
                </div>
              </div>
            </div>

            {/* 撮影のコツ */}
            <div className="mt-6 bg-blue-50 rounded-lg p-4">
              <h4 className="text-md font-semibold text-blue-800 mb-2">撮影のコツ</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• 全身が画面に収まるように撮影してください</li>
                <li>• 明るい場所で撮影し、影が少ないようにしてください</li>
                <li>• カメラを固定し、手ブレを避けてください</li>
                <li>• サーブ動作全体（準備からフォロースルーまで）を撮影してください</li>
              </ul>
            </div>
          </div>
        )}

        {/* 設定パネル */}
        {showSettings && (
          <div className="mb-8 bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800">詳細設定</h3>
              <button
                onClick={() => setShowSettings(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
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

              {useChatGPT && (
                <div className="space-y-4 pl-6 border-l-2 border-blue-200">
                  <div>
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

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                      <MessageSquare className="w-4 h-4 mr-1" />
                      気になっていること・改善したいポイント
                    </label>
                    <textarea
                      value={userConcerns}
                      onChange={(e) => setUserConcerns(e.target.value)}
                      placeholder="例：サーブの威力を上げたい、フォームが安定しない、トスが不安定など..."
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      ここに入力した内容に基づいて、AIがより具体的なアドバイスを生成します
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* プログレスバー */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full ${
                  currentStep >= step.id ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'
                }`}>
                  <step.icon className="w-5 h-5" />
                </div>
                <span className={`ml-2 text-sm font-medium ${
                  currentStep >= step.id ? 'text-blue-600' : 'text-gray-500'
                }`}>
                  {step.title}
                </span>
                {index < steps.length - 1 && (
                  <div className={`w-16 h-1 mx-4 ${
                    currentStep > step.id ? 'bg-blue-600' : 'bg-gray-200'
                  }`} />
                )}
              </div>
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
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                動画をアップロード
              </h2>
              
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition-colors cursor-pointer"
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-lg text-gray-600 mb-2">
                  ここに動画ファイルをドラッグ&ドロップ
                </p>
                <p className="text-sm text-gray-500 mb-4">
                  または、クリックしてファイルを選択
                </p>
                <p className="text-xs text-gray-400">
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

        {/* ステップ2: 解析実行 */}
        {currentStep === 2 && (
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">解析実行</h2>

              {selectedFile && (
                <div className="bg-green-50 rounded-lg p-4 mb-6">
                  <p className="text-green-800">
                    <strong>選択されたファイル:</strong> {selectedFile.name}
                  </p>
                  <p className="text-sm text-green-600">
                    サイズ: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              )}

              {/* ChatGPT使用時の懸念事項表示 */}
              {useChatGPT && userConcerns && (
                <div className="bg-blue-50 rounded-lg p-4 mb-6">
                  <h4 className="text-blue-800 font-medium mb-2 flex items-center">
                    <MessageSquare className="w-4 h-4 mr-1" />
                    気になっていること
                  </h4>
                  <p className="text-blue-700 text-sm">{userConcerns}</p>
                </div>
              )}

              <div className="flex justify-between items-center">
                <button
                  onClick={() => setCurrentStep(1)}
                  className="px-6 py-3 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  ← 戻る
                </button>
                <button
                  onClick={handleAnalyze}
                  disabled={!selectedFile || isAnalyzing}
                  className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-colors"
                >
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      解析中... ({uploadProgress}%)
                    </>
                  ) : (
                    <>
                      <Play className="w-5 h-5 mr-2" />
                      解析開始
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ステップ3: 結果表示 */}
        {currentStep === 3 && analysisResult && (
          <div className="space-y-8">
            {/* 総合スコア */}
            <div className="bg-white rounded-lg shadow-lg p-8 text-center">
              <h2 className="text-3xl font-bold text-gray-800 mb-4">解析結果</h2>
              
              {/* 段階的評価結果の表示 */}
              {analysisResult.tiered_evaluation && (
                <div className="mb-6">
                  <div className="text-6xl font-bold text-blue-600 mb-2">
                    {analysisResult.tiered_evaluation.total_score || analysisResult.overall_score || 0}
                  </div>
                  <div className="text-xl text-gray-600 mb-4">/ 10点</div>
                  
                  {/* 技術レベル表示 */}
                  <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-lg font-semibold">
                    <Award className="w-6 h-6 mr-2" />
                    {analysisResult.tiered_evaluation.skill_level_name || '中級者'}
                  </div>
                </div>
              )}
              
              {/* 従来の総合スコア（フォールバック） */}
              {!analysisResult.tiered_evaluation && (
                <div className="mb-6">
                  <div className="text-6xl font-bold text-blue-600 mb-2">
                    {analysisResult.overall_score || 0}
                  </div>
                  <div className="text-xl text-gray-600">/ 10点</div>
                </div>
              )}

              <div className="flex justify-center">
                <button
                  onClick={resetAnalysis}
                  className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center"
                >
                  <Upload className="w-5 h-5 mr-2" />
                  新しい動画を解析
                </button>
              </div>
            </div>

            {/* フェーズ別解析 */}
            {analysisResult.phase_analysis && (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                  <BarChart3 className="w-8 h-8 text-blue-600 mr-3" />
                  フェーズ別解析
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Object.entries(analysisResult.phase_analysis).map(([phase, data]) => (
                    <div key={phase} className="bg-gray-50 rounded-lg p-6">
                      <h3 className="text-lg font-semibold text-gray-800 mb-3">{phase}</h3>
                      <div className="flex items-center mb-3">
                        <div className="text-2xl font-bold text-blue-600 mr-2">
                          {data.score ? data.score.toFixed(1) : '7.0'}
                        </div>
                        <div className="text-gray-600">/10</div>
                      </div>
                      {data.feedback && (
                        <p className="text-gray-700 text-sm">{data.feedback}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* AI詳細アドバイス */}
            {analysisResult.advice && (analysisResult.advice.enhanced || analysisResult.advice.detailed_advice) && (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-800 flex items-center">
                    <Brain className="w-8 h-8 text-purple-600 mr-3" />
                    AI詳細解析レポート
                    {userConcerns && (
                      <span className="ml-2 text-sm bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
                        カスタマイズ済み
                      </span>
                    )}
                  </h2>
                  {analysisResult.advice.enhanced && (
                    <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                      ChatGPT アドバイス生成
                    </span>
                  )}
                </div>
                
                {/* ユーザーの懸念事項表示 */}
                {userConcerns && (
                  <div className="bg-blue-50 rounded-lg p-4 mb-6">
                    <h4 className="text-blue-800 font-medium mb-2 flex items-center">
                      <MessageSquare className="w-4 h-4 mr-1" />
                      あなたの懸念事項
                    </h4>
                    <p className="text-blue-700 text-sm">{userConcerns}</p>
                  </div>
                )}
                
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
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                  <BookOpen className="w-8 h-8 text-green-600 mr-3" />
                  基本アドバイス
                </h2>
                <div className="text-gray-700 leading-relaxed">
                  {analysisResult.advice.basic_advice}
                </div>
              </div>
            )}

            {/* ワンポイントアドバイス */}
            {analysisResult.advice && analysisResult.advice.one_point_advice && (
              <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-lg shadow-lg p-8">
                <h2 className="text-2xl font-bold text-orange-800 mb-6 flex items-center">
                  <Sparkles className="w-8 h-8 text-orange-600 mr-3" />
                  ワンポイントアドバイス
                </h2>
                <div className="text-orange-800 text-lg leading-relaxed font-medium">
                  {analysisResult.advice.one_point_advice}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

