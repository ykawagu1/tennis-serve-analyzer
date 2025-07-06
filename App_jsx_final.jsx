import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { Upload, Play, Settings, Brain, TrendingUp, Target, Award } from 'lucide-react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState({
    useChatGPT: false,
    apiKey: '',
    userLevel: 'beginner',
    focusAreas: []
  });

  const handleFileSelect = useCallback((event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setAnalysisResult(null);
    }
  }, []);

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert('動画ファイルを選択してください');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const formData = new FormData();
      formData.append('video', selectedFile);
      formData.append('use_chatgpt', settings.useChatGPT);
      formData.append('api_key', settings.apiKey);
      formData.append('user_level', settings.userLevel);
      formData.append('focus_areas', settings.focusAreas.join(','));

      console.log('解析リクエストを送信中...');
      
      const response = await axios.post('http://localhost:5000/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 300000
      });

      console.log('バックエンドからのレスポンス:', response.data);
      
      if (response.data.success && response.data.result) {
        console.log('解析結果データ:', response.data.result);
        setAnalysisResult(response.data.result);
        console.log('解析結果設定完了:', response.data.result);
      } else {
        throw new Error('解析結果の取得に失敗しました');
      }
    } catch (error) {
      console.error('解析エラー:', error);
      alert(`解析エラー: ${error.response?.data?.error || error.message}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const toggleSettings = () => {
    setShowSettings(!showSettings);
  };

  const handleSettingsChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const resetAnalysis = () => {
    setSelectedFile(null);
    setAnalysisResult(null);
    setIsAnalyzing(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-white rounded-full p-4 shadow-lg mr-4">
              <TrendingUp className="w-12 h-12 text-blue-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-800">
              テニスサービス動作解析システム
            </h1>
          </div>
          <p className="text-xl text-gray-600 mb-6">
            AI技術でサーブフォームを詳細解析
          </p>
          
          <div className="flex justify-center items-center space-x-8 mb-8">
            <div className="flex items-center bg-white rounded-lg px-4 py-2 shadow-md">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span className="text-sm font-medium text-gray-700">動画解析</span>
            </div>
            <div className="flex items-center bg-white rounded-lg px-4 py-2 shadow-md">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span className="text-sm font-medium text-gray-700">動作分析</span>
            </div>
            <div className="flex items-center bg-white rounded-lg px-4 py-2 shadow-md">
              <TrendingUp className="w-4 h-4 text-blue-500 mr-2" />
              <span className="text-sm font-medium text-gray-700">結果表示</span>
            </div>
          </div>

          <div className="flex justify-center items-center space-x-4">
            {settings.useChatGPT && (
              <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-medium flex items-center">
                <Brain className="w-4 h-4 mr-2" />
                ChatGPT詳細解析が有効です
              </div>
            )}
            <button
              onClick={toggleSettings}
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-full text-sm font-medium flex items-center transition-colors"
            >
              <Settings className="w-4 h-4 mr-2" />
              設定
            </button>
          </div>
        </header>

        {showSettings && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8 max-w-2xl mx-auto">
            <h3 className="text-lg font-bold text-gray-800 mb-4">解析設定</h3>
            
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="useChatGPT"
                  checked={settings.useChatGPT}
                  onChange={(e) => handleSettingsChange('useChatGPT', e.target.checked)}
                  className="mr-3"
                />
                <label htmlFor="useChatGPT" className="text-gray-700">
                  AI詳細解析を使用する（ChatGPT）
                </label>
              </div>

              {settings.useChatGPT && (
                <div>
                  <label className="block text-gray-700 mb-2">OpenAI APIキー</label>
                  <input
                    type="password"
                    value={settings.apiKey}
                    onChange={(e) => handleSettingsChange('apiKey', e.target.value)}
                    placeholder="sk-..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              )}

              <div>
                <label className="block text-gray-700 mb-2">プレイヤーレベル</label>
                <select
                  value={settings.userLevel}
                  onChange={(e) => handleSettingsChange('userLevel', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="beginner">初心者</option>
                  <option value="intermediate">中級者</option>
                  <option value="advanced">上級者</option>
                </select>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={toggleSettings}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
              >
                設定を保存
              </button>
            </div>
          </div>
        )}

        <div className="max-w-4xl mx-auto">
          {!analysisResult ? (
            <div className="bg-white rounded-lg shadow-lg p-8 text-center">
              <Upload className="w-16 h-16 text-blue-500 mx-auto mb-6" />
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                動画ファイルをアップロード
              </h2>
              <p className="text-gray-600 mb-6">
                テニスサーブの動画をアップロードして、AI解析を開始しましょう
              </p>
              
              <div className="mb-6">
                <input
                  type="file"
                  accept="video/*"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="video-upload"
                />
                <label
                  htmlFor="video-upload"
                  className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium cursor-pointer transition-colors"
                >
                  ファイルを選択
                </label>
              </div>

              {selectedFile && (
                <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                  <p className="text-gray-700">
                    選択されたファイル: <span className="font-medium">{selectedFile.name}</span>
                  </p>
                  <p className="text-sm text-gray-500">
                    サイズ: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              )}

              <button
                onClick={handleAnalyze}
                disabled={!selectedFile || isAnalyzing}
                className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-8 py-3 rounded-lg font-medium transition-colors flex items-center mx-auto"
              >
                {isAnalyzing ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                    解析中...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5 mr-3" />
                    解析開始
                  </>
                )}
              </button>

              <div className="mt-8 text-sm text-gray-500">
                <p>対応形式: MP4, MOV, AVI（最大100MB）</p>
                <p>推奨: 5-30秒のサーブ動作動画</p>
              </div>
            </div>
          ) : (
            <div className="space-y-8">
              <div className="text-center mb-8">
                <Play className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">解析完了</h2>
                <p className="text-gray-600">
                  サーブフォームの詳細解析が完了しました
                </p>
                <button
                  onClick={resetAnalysis}
                  className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                >
                  新しい解析を開始
                </button>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <Award className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-800 mb-6">解析結果</h3>
                
                <div className="grid grid-cols-2 gap-8">
                  <div>
                    <div className="text-4xl font-bold text-blue-600 mb-2">
                      {analysisResult.total_score || 0}
                    </div>
                    <div className="text-gray-600">総合スコア</div>
                  </div>
                  <div>
                    <div className="text-4xl font-bold text-green-600 mb-2">
                      {analysisResult.frame_count || analysisResult.pose_data_count || 0}
                    </div>
                    <div className="text-gray-600">解析フレーム数</div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-xl font-bold text-gray-800 mb-6">フェーズ別解析</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {analysisResult.phase_analysis && Object.entries(analysisResult.phase_analysis).map(([phase, data]) => (
                    <div key={phase} className="text-center">
                      <h4 className="font-semibold text-gray-700 mb-2">{phase}</h4>
                      <div className="text-3xl font-bold text-blue-600 mb-1">
                        {data.score || 0}
                      </div>
                      {data.feedback && (
                        <p className="text-sm text-gray-500">{data.feedback}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
                  <Brain className="w-5 h-5 mr-3 text-purple-600" />
                  AIアドバイス
                  {analysisResult.advice?.enhanced && (
                    <span className="ml-3 bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                      GPT-4o生成
                    </span>
                  )}
                </h3>
                
                <div className="space-y-6">
                  {/* GPT-4oの詳細アドバイスを優先表示 */}
                  {analysisResult.advice?.detailed_advice ? (
                    <div className="prose max-w-none">
                      <div 
                        className="text-gray-700 leading-relaxed whitespace-pre-wrap"
                        style={{ 
                          maxHeight: 'none',
                          overflow: 'visible',
                          wordBreak: 'break-word',
                          lineHeight: '1.6'
                        }}
                        dangerouslySetInnerHTML={{
                          __html: analysisResult.advice.detailed_advice
                            .replace(/## (.*?)$/gm, '<h2 class="text-xl font-bold text-gray-800 mt-8 mb-4 border-b-2 border-purple-200 pb-2">$1</h2>')
                            .replace(/### (.*?)$/gm, '<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-3">$1</h3>')
                            .replace(/#### (.*?)$/gm, '<h4 class="text-md font-medium text-gray-600 mt-4 mb-2">$1</h4>')
                            .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-gray-800">$1</strong>')
                            .replace(/^- (.*?)$/gm, '<li class="ml-6 mb-2 text-gray-700 list-disc">$1</li>')
                            .replace(/^(\d+)\. (.*?)$/gm, '<li class="ml-6 mb-2 text-gray-700 list-decimal">$2</li>')
                            .replace(/\n\n/g, '</p><p class="mb-4">')
                            .replace(/^\s*([^<].*?)$/gm, '<p class="mb-4">$1</p>')
                            .replace(/\|([^|]+)\|([^|]+)\|([^|]+)\|/g, '<tr><td class="border border-gray-300 px-4 py-2 bg-gray-50">$1</td><td class="border border-gray-300 px-4 py-2">$2</td><td class="border border-gray-300 px-4 py-2">$3</td></tr>')
                            .replace(/<tr>/g, '<table class="w-full border-collapse border border-gray-300 my-4"><tr>')
                            .replace(/<\/tr>(?!.*<tr>)/g, '</tr></table>')
                        }}
                      />
                    </div>
                  ) : (
                    /* 基本アドバイスの表示 */
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

                  {/* エラー情報の表示 */}
                  {analysisResult.advice?.error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <h4 className="font-semibold text-red-800 mb-2">ChatGPT接続エラー</h4>
                      <p className="text-red-700 text-sm">{analysisResult.advice.error}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

