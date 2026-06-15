import React from 'react';

export default function WeightSliders({ alpha, setAlpha, onAlphaChange }) {
  const handleChange = (e) => {
    const val = parseFloat(e.target.value);
    setAlpha(val);
    if (onAlphaChange) {
      onAlphaChange(val);
    }
  };

  const tfidfPercent = Math.round(alpha * 100);
  const sbertPercent = Math.round((1 - alpha) * 100);

  return (
    <div className="glass-panel p-5 rounded-xl border border-slate-800">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-sm font-semibold text-slate-300 flex items-center gap-2">
          <span>⚙️</span> Scoring Weights Configuration
        </h3>
        <span className="text-xs bg-slate-900 px-2.5 py-1 border border-slate-800 rounded-lg text-slate-400 font-mono">
          α = {alpha.toFixed(1)}
        </span>
      </div>

      <div className="space-y-4">
        {/* Slider element */}
        <div className="relative pt-1">
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={alpha}
            onChange={handleChange}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-brand-500 focus:outline-none"
          />
        </div>

        {/* Labels and values */}
        <div className="flex justify-between items-center text-xs font-medium">
          <div className="flex flex-col items-start">
            <span className="text-slate-400">TF-IDF (Lexical)</span>
            <span className="text-brand-400 text-sm font-bold font-mono">{tfidfPercent}%</span>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-slate-400">SBERT (Semantic)</span>
            <span className="text-emerald-400 text-sm font-bold font-mono">{sbertPercent}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
