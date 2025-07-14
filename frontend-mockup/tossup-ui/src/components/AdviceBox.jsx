
import React from "react";

const AdviceBox = ({ advice }) => (
  <div className="mt-4 px-6 py-3 bg-blue-100 border border-blue-300 rounded-xl shadow">
    <p className="text-blue-800 text-center">{advice}</p>
  </div>
);

export default AdviceBox;
