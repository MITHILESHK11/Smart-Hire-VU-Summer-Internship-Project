import React from 'react';
import { Sliders, HelpCircle } from 'lucide-react';

export default function WeightSliders({ alpha, setAlpha, onWeightChange }) {
  const handleSliderChange = (e) => {
    const value = parseFloat(e.target.value);
    setAlpha(value);
  };

  const handleMouseUp = () => {
    if (onWeightChange) {
      onWeightChange(alpha);
    }
  };

  const tfidfWeight = Math.round(alpha * 100);
  const sbertWeight = Math.round((1 - alpha) * 100);

  return (
    <div className="space-y-2 pb-2 border-b border-brand-850/50">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-1.5">
          <Sliders className="w-4 h-4 text-brand-400" />
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Adjust Scorer Bias</h3>
        </div>
        
        <div className="group relative">
          <HelpCircle className="w-3.5 h-3.5 text-slate-500 hover:text-slate-300 cursor-pointer transition-colors" />
          <div className="absolute right-0 bottom-6 w-64 p-2.5 bg-brand-950 border border-brand-800 rounded-xl text-[10px] text-slate-400 shadow-xl opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-opacity duration-200 z-30 leading-normal">
            <span className="font-semibold text-slate-200 block mb-0.5">Hybrid Scorer Bias:</span>
            <strong>Lexical (TF-IDF)</strong> matches exact technical keywords and spellings.<br/>
            <strong>Semantic (SBERT)</strong> matches synonyms and similar contexts.
          </div>
        </div>
      </div>

      <div className="space-y-1">
        <div className="relative flex items-center">
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={alpha}
            onChange={handleSliderChange}
            onMouseUp={handleMouseUp}
            onTouchEnd={handleMouseUp}
            className="w-full h-1.5 bg-brand-950 border border-brand-800 rounded-lg appearance-none cursor-pointer accent-brand-500"
          />
        </div>

        <div className="flex justify-between items-center text-[10px] font-semibold text-slate-400">
          <div>
            Lexical: <span className="text-brand-400 font-bold">{tfidfWeight}%</span>
          </div>
          <div>
            Semantic: <span className="text-accent-cyan font-bold">{sbertWeight}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
