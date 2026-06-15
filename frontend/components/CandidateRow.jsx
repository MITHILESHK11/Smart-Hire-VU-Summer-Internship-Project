import React, { useState } from 'react';

export default function CandidateRow({ candidate }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const formatPercent = (val) => {
    return (val * 100).toFixed(1) + '%';
  };

  const getScoreColor = (score) => {
    if (score >= 0.75) return 'text-emerald-400';
    if (score >= 0.5) return 'text-brand-400';
    return 'text-amber-500';
  };

  return (
    <>
      {/* Table Main Row */}
      <tr
        onClick={() => setIsExpanded(!isExpanded)}
        className={`border-b border-slate-800/80 hover:bg-slate-900/50 cursor-pointer transition-colors ${
          isExpanded ? 'bg-slate-900/30' : ''
        } ${candidate.rank <= 3 ? 'bg-brand-500/[0.015]' : ''}`}
      >
        <td className="px-6 py-4 text-sm font-semibold text-slate-300">
          {candidate.rank <= 3 ? (
            <span className="flex items-center gap-1.5 text-brand-400">
              🥇 {candidate.rank}
            </span>
          ) : (
            candidate.rank
          )}
        </td>
        <td className="px-6 py-4 text-sm font-medium text-slate-200 max-w-[200px] truncate">
          {candidate.filename}
        </td>
        <td className="px-6 py-4 text-sm text-slate-400 font-mono">
          {formatPercent(candidate.tfidf_score)}
        </td>
        <td className="px-6 py-4 text-sm text-slate-400 font-mono">
          {formatPercent(candidate.sbert_score)}
        </td>
        <td className="px-6 py-4">
          <div className="flex items-center gap-3">
            <span className={`text-sm font-bold font-mono ${getScoreColor(candidate.final_score)}`}>
              {formatPercent(candidate.final_score)}
            </span>
            <div className="w-24 h-1.5 bg-slate-800 rounded-full overflow-hidden hidden sm:block">
              <div
                className={`h-full rounded-full transition-all duration-500 ${
                  candidate.final_score >= 0.75 ? 'bg-emerald-500' :
                  candidate.final_score >= 0.5 ? 'bg-brand-500' : 'bg-amber-500'
                }`}
                style={{ width: `${candidate.final_score * 100}%` }}
              />
            </div>
          </div>
        </td>
        <td className="px-6 py-4 text-xs max-w-[180px] truncate text-slate-400">
          {candidate.missing_keywords && candidate.missing_keywords.length > 0
            ? candidate.missing_keywords.join(', ')
            : 'None'}
        </td>
        <td className="px-6 py-4 text-slate-500 text-xs text-right">
          {isExpanded ? '▲' : '▼'}
        </td>
      </tr>

      {/* Expanded Details Row */}
      {isExpanded && (
        <tr className="bg-slate-950/40 border-b border-slate-800/80">
          <td colSpan={7} className="px-8 py-5">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
              {/* Left Column: Skill Analysis */}
              <div className="space-y-4">
                <div>
                  <h4 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-2">
                    ✅ Skills Matched
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {candidate.skills_matched && candidate.skills_matched.length > 0 ? (
                      candidate.skills_matched.map((skill, idx) => (
                        <span
                          key={idx}
                          className="text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded"
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-slate-500 italic">No skills extracted</span>
                    )}
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-semibold text-red-400 uppercase tracking-wider mb-2">
                    ❌ Missing Keywords
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {candidate.missing_keywords && candidate.missing_keywords.length > 0 ? (
                      candidate.missing_keywords.map((skill, idx) => (
                        <span
                          key={idx}
                          className="text-xs bg-red-500/10 border border-red-500/20 text-red-400 px-2 py-0.5 rounded"
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-emerald-400 font-medium italic">No missing skills!</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Right Column: Demographics & Education */}
              <div className="space-y-4 border-t md:border-t-0 md:border-l border-slate-800/80 pt-4 md:pt-0 md:pl-6">
                <div>
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                    🎓 Education
                  </h4>
                  <p className="text-slate-300 font-medium">
                    {candidate.education && candidate.education.length > 0 
                      ? candidate.education.join(' | ') 
                      : 'Not specified'}
                  </p>
                </div>

                <div>
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                    💼 Experience
                  </h4>
                  <p className="text-slate-300 font-medium">
                    {candidate.experience_years !== null && candidate.experience_years !== undefined
                      ? `${candidate.experience_years} Year${candidate.experience_years === 1 ? '' : 's'}`
                      : 'Not specified'}
                  </p>
                </div>
              </div>
            </div>
          </td>
        </tr>
      )}
    </>
  );
}
