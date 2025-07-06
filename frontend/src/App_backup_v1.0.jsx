import React, { useState, useCallback, useRef } from 'react';
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
  Brain
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
  const [apiKey, setApiKey] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const [useChatGPT, setUseChatGPT] = useState(false);
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
      } else if (trimmedLine.length > 0) {
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

  const handleFileSelect = useCallback((event) => {
    const file = event.target.files[0];
    if (file) {
      // ファイル形式チェック（拡張子ベース）
      const fileName = file.name.toLowerCase();
      const allowedExtensions = ['.mp4', '.avi', '.mov', '.mkv', '.m4v', '.wmv'];
      const isValidFormat = allowedExtensions.some(ext => fileName.endsWith(ext));
      
      if (!isValidFormat) {
        setError('サポートされていないファイル形式です。MP4, AVI, MOV, MKVファイルを選択してください。');
        return;
      }

      // ファイルサイズチェック（100MB）
      if (file.size > 100 * 1024 * 1024) {
        setError('ファイルサイズが大きすぎます。100MB以下のファイルを選択してください。');
        return;
      }

      setSelectedFile(file);
      setError(null);
      setCurrentStep(2);
    }
  }, []);

  const handleDrop = useCallback((event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      const fakeEvent = { target: { files: [file] } };
      handleFileSelect(fakeEvent);
    }
  }, [handleFileSelect]);

  const handleDragOver = useCallback((event) => {
    event.preventDefault();
  }, []);

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
      console.log('バックエンドからのレスポンス:', response.data);
      console.log('解析結果データ:', response.data.result);
      
      // レスポンスの構造を確認して適切にデータを設定
      if (response.data && response.data.success && response.data.result) {
        setAnalysisResult(response.data.result);
        console.log('解析結果設定完了:', response.data.result);
      } else {
        console.error('予期しないレスポンス構造:', response.data);
        setError('解析結果の形式が正しくありません');
        return;
      }
      
      setCurrentStep(3);
    } catch (err) {
      console.error('解析エラー:', err);
      if (err.response?.data?.error) {
        setError(`解析エラー: ${err.response.data.error}`);
      } else {
        setError('解析中にエラーが発生しました。もう一度お試しください。');
      }
    } finally {
      setIsAnalyzing(false);
      setUploadProgress(0);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setAnalysisResult(null);
    setError(null);
    setCurrentStep(1);
    setUploadProgress(0);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSaveApiKey = () => {
    if (apiKey.trim()) {
      setUseChatGPT(true);
      setShowSettings(false);
    } else {
      setUseChatGPT(false);
    }
  };

  const handleRemoveApiKey = () => {
    setApiKey('');
    setUseChatGPT(false);
    setShowSettings(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* ヘッダー */}
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-green-500 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-gray-800">テニスサービス動作解析システム</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              {useChatGPT && (
                <div className="flex items-center space-x-2 bg-purple-100 px-3 py-1 rounded-full">
                  <Sparkles className="w-4 h-4 text-purple-600" />
                  <span className="text-sm font-medium text-purple-800">ChatGPT詳細解析が有効です</span>
                </div>
              )}
              
              <button
                onClick={() => setShowSettings(true)}
                className="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg transition-colors"
              >
                <Settings className="w-4 h-4" />
                <span className="text-sm font-medium">設定</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 設定モーダル */}
      {showSettings && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800">ChatGPT API設定</h3>
              <button
                onClick={() => setShowSettings(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  OpenAI APIキー
                </label>
                <div className="relative">
                  <input
                    type={showApiKey ? "text" : "password"}
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="sk-..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowApiKey(!showApiKey)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  ChatGPTによる詳細なアドバイス生成に使用されます
                </p>
              </div>
              
              <div className="flex space-x-3">
                <button
                  onClick={handleSaveApiKey}
                  disabled={!apiKey.trim()}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                >
                  保存して有効化
                </button>
                {useChatGPT && (
                  <button
                    onClick={handleRemoveApiKey}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    削除
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="container mx-auto px-4 py-8">
        {/* ステップインジケーター */}
        <div className="flex items-center justify-center space-x-8 mb-12">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = currentStep === step.id;
            const isCompleted = currentStep > step.id;
            
            return (
              <div key={step.id} className="flex items-center">
                <div className={`flex items-center justify-center w-12 h-12 rounded-full border-2 transition-all ${
                  isCompleted 
                    ? 'bg-green-500 border-green-500 text-white' 
                    : isActive 
                      ? 'bg-blue-500 border-blue-500 text-white' 
                      : 'bg-white border-gray-300 text-gray-400'
                }`}>
                  {isCompleted ? (
                    <CheckCircle className="w-6 h-6" />
                  ) : (
                    <Icon className="w-6 h-6" />
                  )}
                </div>
                <div className="ml-3">
                  <div className={`text-sm font-medium ${
                    isActive ? 'text-blue-600' : isCompleted ? 'text-green-600' : 'text-gray-500'
                  }`}>
                    {step.title}
                  </div>
                </div>
                {index < steps.length - 1 && (
                  <div className={`w-16 h-0.5 mx-8 ${
                    currentStep > step.id ? 'bg-green-500' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            );
          })}
        </div>

        {/* メインコンテンツ */}
        <div className="max-w-4xl mx-auto">
          {/* エラー表示 */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start">
              <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <h4 className="text-red-800 font-medium">エラーが発生しました</h4>
                <p className="text-red-700 text-sm mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* ステップ1: ファイル選択 */}
          {currentStep === 1 && (
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="text-center mb-8">
                <FileVideo className="w-16 h-16 text-blue-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">動画ファイルを選択</h2>
                <p className="text-gray-600">テニスサービスの動画をアップロードして解析を開始しましょう</p>
              </div>

              <div
                className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition-colors cursor-pointer"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-lg text-gray-600 mb-2">
                  ファイルをドラッグ&ドロップするか、クリックして選択
                </p>
                <p className="text-sm text-gray-500">
                  対応形式: MP4, AVI, MOV, MKV（最大100MB）
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".mp4,.avi,.mov,.mkv,.m4v,.wmv"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </div>

              {/* 撮影のコツ */}
              <div className="mt-8 bg-blue-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-blue-800 mb-3 flex items-center">
                  <Target className="w-5 h-5 mr-2" />
                  撮影のコツ
                </h3>
                <ul className="space-y-2 text-blue-700">
                  <li className="flex items-start">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    横から全身が映るように撮影してください
                  </li>
                  <li className="flex items-start">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    サービス動作全体（準備からフォロースルーまで）を含めてください
                  </li>
                  <li className="flex items-start">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    明るい場所で、背景がシンプルな環境で撮影してください
                  </li>
                </ul>
              </div>
            </div>
          )}

          {/* ステップ2: 解析実行 */}
          {currentStep === 2 && selectedFile && (
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="text-center mb-8">
                <Play className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">解析準備完了</h2>
                <p className="text-gray-600">選択されたファイル: {selectedFile.name}</p>
              </div>

              {isAnalyzing ? (
                <div className="text-center">
                  <Loader2 className="w-12 h-12 text-blue-500 mx-auto mb-4 animate-spin" />
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">解析中...</h3>
                  <p className="text-gray-600 mb-4">動画を解析しています。しばらくお待ちください。</p>
                  
                  {uploadProgress > 0 && (
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center">
                  <button
                    onClick={handleAnalyze}
                    className="bg-gradient-to-r from-blue-500 to-green-500 hover:from-blue-600 hover:to-green-600 text-white font-bold py-4 px-8 rounded-lg text-lg transition-all transform hover:scale-105 flex items-center mx-auto"
                  >
                    <Sparkles className="w-6 h-6 mr-2" />
                    {useChatGPT ? 'AI詳細解析開始' : '解析開始'}
                  </button>
                  
                  <button
                    onClick={handleReset}
                    className="mt-4 text-gray-500 hover:text-gray-700 underline"
                  >
                    別のファイルを選択
                  </button>
                </div>
              )}
            </div>
          )}

          {/* ステップ3: 結果表示 */}
          {currentStep === 3 && analysisResult && (
            <div className="space-y-6">
              {/* 総合スコア */}
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <Award className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-4">解析結果</h2>
                
                <div className="flex items-center justify-center space-x-8 mb-6">
                  <div className="text-center">
                    <div className="text-4xl font-bold text-blue-600 mb-2">
                      {analysisResult.total_score?.toFixed(1) || '0.0'}
                    </div>
                    <div className="text-gray-600">総合スコア</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-semibold text-green-600 mb-2">
                      {analysisResult.frame_count || 0}
                    </div>
                    <div className="text-gray-600">解析フレーム数</div>
                  </div>
                </div>
              </div>

              {/* フェーズ別解析 */}
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
                  <BarChart3 className="w-5 h-5 mr-3 text-blue-600" />
                  フェーズ別解析
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {analysisResult.phase_analysis && Object.entries(analysisResult.phase_analysis).map(([phase, data]) => (
                    <div key={phase} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-gray-800">{phase}</h4>
                        <span className="text-lg font-bold text-blue-600">
                          {data.score?.toFixed(1) || '0.0'}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${(data.score || 0) * 10}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

                {/* AIアドバイス */}
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
                  <Brain className="w-5 h-5 mr-3 text-purple-600" />
                  AIアドバイス
                </h3>
                
                <div className="space-y-6">
                  {/* 詳細アドバイス（Markdown形式） */}
                  {analysisResult.advice?.detailed_advice && (
                    <div className="prose max-w-none">
                      <div 
                        className="text-gray-700 leading-relaxed"
                        dangerouslySetInnerHTML={{
                          __html: analysisResult.advice.detailed_advice
                            .replace(/## /g, '<h2 class="text-lg font-bold text-gray-800 mt-6 mb-3">')
                            .replace(/### /g, '<h3 class="text-md font-semibold text-gray-700 mt-4 mb-2">')
                            .replace(/#### /g, '<h4 class="text-sm font-medium text-gray-600 mt-3 mb-2">')
                            .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-gray-800">$1</strong>')
                            .replace(/- \*\*(.*?)\*\*:/g, '<li class="ml-4"><strong class="text-gray-800">$1</strong>:')
                            .replace(/- (.*?)$/gm, '<li class="ml-4 text-gray-700">$1</li>')
                            .replace(/\n\n/g, '</p><p class="mb-4">')
                            .replace(/^\s*(.+)$/gm, '<p class="mb-4">$1</p>')
                            .replace(/\| (.*?) \|/g, '<td class="border px-4 py-2">$1</td>')
                            .replace(/\|---/g, '<tr>')
                        }}
                      />
                    </div>
                  )}

                  {/* フォールバック: 基本的なアドバイス表示 */}
                  {!analysisResult.advice?.detailed_advice && (
                    <>
                      <div>
                        <h4 className="font-semibold text-gray-800 mb-3">総合評価</h4>
                        <p className="text-gray-700 bg-blue-50 p-4 rounded-lg">
                          {analysisResult.advice?.summary || 'アドバイスを生成中...'}
                        </p>
                      </div>

                      {analysisResult.advice?.improvements && analysisResult.advice.improvements.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-gray-800 mb-3">改善ポイント</h4>
                          <ul className="space-y-2">
                            {analysisResult.advice.improvements.map((point, index) => (
                              <li key={index} className="flex items-start">
                                <span className="bg-blue-100 text-blue-800 text-sm font-medium px-2 py-1 rounded mr-3 mt-0.5">
                                  {index + 1}
                                </span>
                                <span className="text-gray-700">{point}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {analysisResult.advice?.drills && analysisResult.advice.drills.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-gray-800 mb-3">練習メニュー</h4>
                          <ul className="space-y-2">
                            {analysisResult.advice.drills.map((drill, index) => (
                              <li key={index} className="flex items-start">
                                <span className="bg-green-100 text-green-800 text-sm font-medium px-2 py-1 rounded mr-3 mt-0.5">
                                  {index + 1}
                                </span>
                                <span className="text-gray-700">{drill}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>v>

              {/* AI詳細解析レポート */}
              {analysisResult.advice?.enhanced && analysisResult.advice?.full_ai_response && (
                <div className="bg-white rounded-lg shadow-lg p-8">
                  <h3 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
                    <Brain className="w-5 h-5 mr-3 text-purple-600" />
                    AI詳細解析レポート
                    <span className="ml-3 bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                      ChatGPT生成
                    </span>
                  </h3>
                  
                  <div className="bg-white rounded-lg p-6">
                    <div className="ai-response-content">
                      {formatAIResponse(analysisResult.advice.full_ai_response)}
                    </div>
                  </div>
                </div>
              )}

              {/* 新しい解析ボタン */}
              <div className="text-center">
                <button
                  onClick={handleReset}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors"
                >
                  新しい動画を解析
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

