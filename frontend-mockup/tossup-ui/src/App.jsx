
import React, { useState } from "react";
import { uploadVideo, analyzeVideo } from "./api";
import ScoreDisplay from "./components/ScoreDisplay";
import AdviceBox from "./components/AdviceBox";
import ActionButtons from "./components/ActionButtons";

function App() {
  const [score, setScore] = useState(null);
  const [advice, setAdvice] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setLoading(true);
      setError("");
      const uploadRes = await uploadVideo(file);
      const analyzeRes = await analyzeVideo(uploadRes.upload_id);
      setScore(analyzeRes.result.total_score.toFixed(2)); // 小数第3位を四捨五入
      setAdvice(analyzeRes.result.advice.overall_advice);
    } catch (err) {
      console.error(err);
      setError("解析中にエラーが発生しました。");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-blue-50 flex flex-col items-center justify-center p-4">
      <h1 className="text-2xl font-bold text-blue-900 mb-6">Tennis Serve Analyzer</h1>
      <input
        type="file"
        accept="video/*"
        onChange={handleUpload}
        className="mb-6"
      />
      {loading && <p className="text-gray-700">解析中...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {score && <ScoreDisplay score={score} />}
      {advice && <AdviceBox advice={advice} />}
      {score && <ActionButtons />}
    </div>
  );
}

export default App;
