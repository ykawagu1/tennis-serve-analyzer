import React from "react";

const ScoreDisplay = ({ score, phaseScores }) => {
  // 小数点以下1桁に丸める
  const roundedTotal = parseFloat(score).toFixed(1);

  return (
    <div className="flex flex-col items-center">
      {/* 総合スコア */}
      <p className="text-xl text-gray-600">総合スコア</p>
      <p className="text-6xl font-extrabold text-blue-700 animate-pulse">
        {roundedTotal} / 10
      </p>

      {/* フェーズ別スコア */}
      {phaseScores && Object.keys(phaseScores).length > 0 && (
        <div className="mt-6 w-full max-w-sm bg-blue-50 rounded-lg p-4 shadow">
          <p className="text-lg text-blue-800 font-semibold mb-2">フェーズ別スコア</p>
          <ul className="text-blue-900">
            {Object.entries(phaseScores).map(([phase, data]) => (
              <li key={phase} className="flex justify-between">
                <span>{phase}</span>
                <span>{parseFloat(data.score).toFixed(1)} / 10</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ScoreDisplay;
