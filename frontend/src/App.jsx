import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import {
  Upload, Loader2, CheckCircle, AlertCircle
} from "lucide-react";
import "./App.css";

const API_BASE_URL = "https://tennis-serve-analyzer.onrender.com";

function App() {
  // --- 無料/有料判定と利用回数 ---
  const [isPremium, setIsPremium] = useState(
    localStorage.getItem("isPremium") === "true"
  );
  const [usageCount, setUsageCount] = useState(
    parseInt(localStorage.getItem("usageCount") || "0")
  );
  const [usageDate, setUsageDate] = useState(
    localStorage.getItem("usageDate") || new Date().toLocaleDateString()
  );
  const FREE_LIMIT = 3;
  const PREMIUM_LIMIT = 8;
  const USAGE_LIMIT = isPremium ? PREMIUM_LIMIT : FREE_LIMIT;

  // --- モーダル/ガイド/各種ステート ---
  const [showGuide, setShowGuide] = useState(false);
  const [showUpgrade, setShowUpgrade] = useState(false);

  // --- 解析用の各種ステート ---
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadProgress, setUploadProgress] = useState(0);

  // --- 設定値/フォーム ---
  const [userLevel, setUserLevel] = useState("intermediate");
  const [userConcerns, setUserConcerns] = useState("");
  const [focusAreas, setFocusAreas] = useState([]);
  const fileInputRef = useRef(null);

  // --- 無料/有料回数上限管理 ---
  useEffect(() => {
    // 日付が変わったらusageCountリセット
    const today = new Date().toLocaleDateString();
    if (usageDate !== today) {
      setUsageCount(0);
      localStorage.setItem("usageCount", "0");
      setUsageDate(today);
      localStorage.setItem("usageDate", today);
    }
    if (usageCount >= USAGE_LIMIT) setShowUpgrade(true);
    else setShowUpgrade(false);
  }, [usageCount, usageDate, isPremium]);

  // --- 解析処理（無料/有料の切り分け） ---
  const handleAnalyze = async () => {
    if (!selectedFile) return;

    if (usageCount >= USAGE_LIMIT) {
      setError(
        isPremium
          ? `サブスク会員の1日あたりの解析上限（${PREMIUM_LIMIT}回）に達しました。`
          : `無料枠の1日あたりの解析上限（${FREE_LIMIT}回）に達しました。`
      );
      setShowUpgrade(true);
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append("video", selectedFile);
      formData.append("is_premium", isPremium ? "true" : "false");
      formData.append("user_level", userLevel);
      formData.append("focus_areas", JSON.stringify(focusAreas));
      // 有料枠のみconcerns渡す
      if (isPremium && userConcerns.trim()) {
        formData.append("user_concerns", userConcerns);
      }

      const response = await axios.post(
        `${API_BASE_URL}/api/analyze`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          onUploadProgress: (progressEvent) => {
            const progress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(progress);
          },
        }
      );

      if (response.data.success) {
        setAnalysisResult(response.data.result);
        setCurrentStep(3);
        // 利用回数を加算
        const today = new Date().toLocaleDateString();
        setUsageCount((c) => c + 1);
        localStorage.setItem("usageCount", (usageCount + 1).toString());
        setUsageDate(today);
        localStorage.setItem("usageDate", today);
      } else {
        throw new Error(response.data.error || "解析に失敗しました");
      }
    } catch (err) {
      setError(
        err.response?.data?.error ||
          err.message ||
          "解析中にエラーが発生しました"
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  // --- ファイル選択/ドラッグドロップ ---
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
    if (file && file.type.startsWith("video/")) {
      setSelectedFile(file);
      setCurrentStep(2);
      setError(null);
    }
  };
  const handleDragOver = (event) => event.preventDefault();

  // --- サブスク切替（デモ用） ---
  const handleUpgrade = () => {
    setIsPremium(true);
    localStorage.setItem("isPremium", "true");
    setShowUpgrade(false);
  };

  // --- UI ---
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
        </div>
      </header>

      {/* サブスク切替トグル＆利用回数表示 */}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "12px 0" }}>
        <button
          onClick={() => {
            setIsPremium(!isPremium);
            localStorage.setItem("isPremium", (!isPremium).toString());
          }}
          className={`${
            isPremium ? "bg-yellow-400" : "bg-gray-200"
          } text-sm px-3 py-1 rounded-lg font-bold`}
        >
          {isPremium ? "有料モード (課金ユーザー)" : "無料モード (ゲストユーザー)"}
        </button>
        <div style={{ color: "#888", fontSize: 14, margin: 4 }}>
          {isPremium
            ? `今日の解析回数（サブスク枠）：${usageCount} / ${PREMIUM_LIMIT}`
            : `今日の無料解析回数：${usageCount} / ${FREE_LIMIT}`}
        </div>
      </div>

      {/* 撮影ガイドボタン */}
      <div style={{ display: "flex", justifyContent: "center" }}>
        <button
          onClick={() => setShowGuide(true)}
          className="guide-btn"
        >
          📸 撮影ガイドを見る（横向き撮影必須！）
        </button>
      </div>

      {/* 無料枠上限到達モーダル */}
      {showUpgrade && (
        <div className="modal-overlay" onClick={() => setShowUpgrade(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div style={{ padding: 18 }}>
              <h2 style={{ fontSize: 22, fontWeight: "bold", color: "#1d3d7b", marginBottom: 14 }}>🎾 解析回数の上限に達しました</h2>
              <p style={{ marginBottom: 10 }}>本日ご利用できる無料解析回数（{FREE_LIMIT}回）は終了しました。</p>
              <ul style={{ margin: "0 0 14px 16px", color: "#555" }}>
                <li>・サブスク登録で回数制限なくご利用可能！</li>
                <li>・広告なし、詳細AIアドバイス、機能追加も順次！</li>
              </ul>
              <button
                onClick={handleUpgrade}
                style={{
                  background: "#fbbf24", color: "#242424", fontWeight: "bold",
                  border: "none", borderRadius: 8, padding: "10px 32px", fontSize: 18, marginBottom: 12, marginTop: 8
                }}
              >
                サブスク登録（デモ）
              </button>
              <br />
              <button
                onClick={() => setShowUpgrade(false)}
                style={{ background: "#eee", color: "#888", border: "none", borderRadius: 6, padding: "6px 22px", fontWeight: "bold" }}
              >閉じる</button>
            </div>
          </div>
        </div>
      )}

      {/* 撮影ガイドモーダル */}
      {showGuide && (
        <div className="modal-overlay" onClick={() => setShowGuide(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <img src="/camera_guide.png" alt="撮影ガイド" style={{ width: "90%", maxWidth: 400, marginBottom: 20 }} />
            <button
              onClick={() => setShowGuide(false)}
              style={{
                marginTop: 8,
                padding: "8px 24px",
                borderRadius: 6,
                background: "#2D8CFF",
                color: "#fff",
                border: "none",
                fontWeight: 600
              }}
            >
              閉じる
            </button>
          </div>
        </div>
      )}

      {/* 1画面目：動画アップロード */}
      {currentStep === 1 && (
        <div className="max-w-2xl mx-auto">
          <div className="unified-card">
            <div className="unified-card-header">
              <Upload className="upload-icon" />
              <h2 className="unified-title">動画をアップロード</h2>
            </div>
            <div
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              className="upload-area"
              onClick={() => fileInputRef.current?.click()}
              style={{
                border: "2px dashed #aaa",
                borderRadius: "12px",
                padding: "36px",
                textAlign: "center",
                cursor: "pointer",
                background: "#f8fafc",
              }}
            >
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
      {/* 2画面目：解析設定 */}
      {currentStep === 2 && (
        <div className="max-w-2xl mx-auto">
          <div className="unified-card">
            <h2 className="unified-title">解析設定</h2>
            {/* 有料時だけ表示 */}
            {isPremium && (
              <div style={{ margin: 8 }}>
                <label>
                  気になること（任意）:
                  <input
                    type="text"
                    value={userConcerns}
                    onChange={e => setUserConcerns(e.target.value)}
                    style={{ marginLeft: 8, width: 200 }}
                  />
                </label>
              </div>
            )}
            <div style={{ margin: 16 }}>
              <button onClick={handleAnalyze} disabled={isAnalyzing}>
                {isAnalyzing ? "解析中..." : "解析開始"}
              </button>
              <button onClick={() => setCurrentStep(1)} style={{ marginLeft: 12 }}>
                ← 戻る
              </button>
            </div>
            {error && <div style={{ color: "red", margin: 8 }}>{error}</div>}
          </div>
        </div>
      )}
      {/* 3画面目：解析完了 */}
      {currentStep === 3 && (
        <div className="max-w-2xl mx-auto">
          <div className="unified-card">
            {isAnalyzing ? (
              <div>
                <Loader2 className="animate-spin" />
                <p>解析中です。しばらくお待ちください…</p>
                <div>進捗: {uploadProgress}%</div>
              </div>
            ) : analysisResult ? (
              <div>
                <CheckCircle className="text-green-600" />
                <h2 className="unified-title">解析完了！</h2>
                {/* トータルスコアカード */}
                {analysisResult && (
                  <div style={{
                    maxWidth: 340,
                    margin: "24px auto 16px",
                    background: "#23264d",
                    color: "#fff",
                    borderRadius: 18,
                    boxShadow: "0 4px 12px #23264d33",
                    padding: 24,
                    textAlign: "center"
                  }}>
                    <div style={{ fontSize: 20, fontWeight: 600, marginBottom: 4, letterSpacing: 2 }}>
                      総合スコア
                    </div>
                    <div style={{ fontSize: 60, fontWeight: 700, lineHeight: 1, margin: "0 0 8px 0", letterSpacing: 2 }}>
                      {analysisResult.tiered_evaluation?.total_score?.toFixed(2) ?? analysisResult.overall_score?.toFixed(2) ?? "--"}
                    </div>
                    <div style={{
                      fontSize: 18,
                      fontWeight: 500,
                      color: "#ffd700",
                      marginBottom: 2
                    }}>
                      {analysisResult.tiered_evaluation?.skill_level_name || "レベル不明"}
                    </div>
                  </div>
                )}
                {/* フェーズ別スコアカード群 */}
                {analysisResult?.phase_analysis && (
                  <div style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: 12,
                    justifyContent: "center",
                    marginBottom: 18
                  }}>
                    {Object.entries(analysisResult.phase_analysis).map(([phase, value]) => (
                      <div key={phase} style={{
                        background: "#fff",
                        borderRadius: 14,
                        minWidth: 150,
                        padding: 14,
                        margin: "0 4px",
                        boxShadow: "0 2px 8px #23264d19",
                        border: "2px solid #e4e8fc",
                        textAlign: "center"
                      }}>
                        <div style={{ fontSize: 15, fontWeight: 700, color: "#23264d", marginBottom: 4 }}>
                          {phase.replace("_", " ").toUpperCase()}
                        </div>
                        <div style={{ fontSize: 28, fontWeight: 700, color: "#2846a1" }}>
                          {value.score?.toFixed(1) ?? "--"}
                        </div>
                        <div style={{ fontSize: 13, color: "#777", marginTop: 2 }}>
                          {value.feedback || ""}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                {/* オーバーレイ画像（縦並び） */}
                {analysisResult.overlay_images && analysisResult.overlay_images.length > 0 && (
                  <div>
                    <h3 style={{ fontWeight: "bold", margin: "14px 0 6px" }}>静止ポーズ画像（オーバーレイ）</h3>
                    <div style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: 8,
                      alignItems: "center"
                    }}>
                      {analysisResult.overlay_images.map((img, idx) => (
                        <img
                          key={idx}
                          src={API_BASE_URL + img}
                          alt={`Pose Overlay ${idx + 1}`}
                          style={{ width: 140, borderRadius: 8, border: "1px solid #ddd" }}
                        />
                      ))}
                    </div>
                  </div>
                )}
                {/* アドバイスなどはお好みで追加 */}
                <pre style={{ background: "#f9f9f9", padding: 12, borderRadius: 8, fontSize: 14, marginTop: 12 }}>
                  {JSON.stringify(analysisResult, null, 2)}
                </pre>
                <button onClick={() => setCurrentStep(1)} style={{ marginTop: 14 }}>
                  ← 最初に戻る
                </button>
              </div>
            ) : (
              <div>
                <AlertCircle className="text-red-600" />
                <p>解析結果がありません。</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
