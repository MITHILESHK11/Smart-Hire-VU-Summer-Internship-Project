import React, { useState } from 'react';
import { ArrowUpDown, Users, Calendar, Award, CheckCircle2 } from 'lucide-react';

export default function ResultsTable({ candidates, selectedCandidate, setSelectedCandidate }) {
  const [sortBy, setSortBy] = useState('rank'); // rank, experience, name
  const [sortOrder, setSortOrder] = useState('asc'); // asc, desc

  if (!candidates || candidates.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center p-8 space-y-3">
        <Users className="w-12 h-12 text-slate-700 mx-auto" />
        <h3 className="text-sm font-semibold text-slate-400">No Candidates Evaluated</h3>
        <p className="text-xs text-slate-600 max-w-xs leading-relaxed">
          Upload resumes and paste a job description in the left panel to execute candidate rankings.
        </p>
      </div>
    );
  }

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder(field === 'name' ? 'asc' : 'desc');
    }
  };

  const sortedCandidates = [...candidates].sort((a, b) => {
    let comparison = 0;
    if (sortBy === 'rank') {
      comparison = a.rank - b.rank;
    } else if (sortBy === 'experience') {
      comparison = b.years_of_experience - a.years_of_experience;
    } else if (sortBy === 'name') {
      comparison = a.filename.localeCompare(b.filename);
    }

    return sortOrder === 'asc' ? comparison : -comparison;
  });

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-accent-emerald';
    if (score >= 50) return 'text-accent-amber';
    return 'text-accent-rose';
  };

  const getScoreBg = (score) => {
    if (score >= 70) return 'bg-accent-emerald/10 border-accent-emerald/20';
    if (score >= 50) return 'bg-accent-amber/10 border-accent-amber/20';
    return 'bg-accent-rose/10 border-accent-rose/20';
  };

  return (
    <div className="flex-1 flex flex-col min-h-0">
      
      {/* Top filter section */}
      <div className="flex items-center justify-between pb-3 border-b border-brand-850 shrink-0">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Users className="w-3.5 h-3.5 text-brand-400" />
          Ranked Candidates ({candidates.length})
        </h3>
        
        <div className="flex items-center gap-2 text-[10px]">
          <span className="text-slate-500 font-medium">Sort:</span>
          
          <button
            onClick={() => handleSort('rank')}
            className={`px-2 py-1 rounded-md border font-semibold flex items-center gap-1 transition-colors ${
              sortBy === 'rank'
                ? 'bg-brand-500/15 border-brand-500/35 text-brand-400'
                : 'bg-brand-950/40 border-brand-800/10 text-slate-400 hover:bg-brand-900/30'
            }`}
          >
            <span>Score</span>
            <ArrowUpDown className="w-2.5 h-2.5" />
          </button>

          <button
            onClick={() => handleSort('experience')}
            className={`px-2 py-1 rounded-md border font-semibold flex items-center gap-1 transition-colors ${
              sortBy === 'experience'
                ? 'bg-brand-500/15 border-brand-500/35 text-brand-400'
                : 'bg-brand-950/40 border-brand-800/10 text-slate-400 hover:bg-brand-900/30'
            }`}
          >
            <span>Exp</span>
            <ArrowUpDown className="w-2.5 h-2.5" />
          </button>
        </div>
      </div>

      {/* Cards List container (scrolls independently) */}
      <div className="flex-1 min-h-0 overflow-y-auto space-y-2 mt-3 pr-1">
        {sortedCandidates.map((candidate) => {
          const isSelected = selectedCandidate && selectedCandidate.filename === candidate.filename;
          return (
            <div
              key={candidate.filename}
              onClick={() => setSelectedCandidate(candidate)}
              className={`p-3.5 rounded-xl border cursor-pointer transition-all duration-150 flex items-center justify-between gap-4 animate-fade-in ${
                isSelected
                  ? 'bg-brand-900/30 border-brand-500/50 shadow-inner'
                  : 'bg-brand-950/40 border-brand-800/20 hover:bg-brand-900/15 hover:border-brand-800/40'
              }`}
            >
              <div className="flex items-center gap-3 overflow-hidden">
                {/* Ranks badge */}
                <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-[11px] font-extrabold shrink-0 border ${
                  isSelected 
                    ? 'bg-brand-500/25 border-brand-500/40 text-brand-300' 
                    : 'bg-brand-950 border-brand-800/60 text-slate-400 shadow-inner'
                }`}>
                  #{candidate.rank}
                </div>

                <div className="overflow-hidden">
                  <h4 className="text-xs font-semibold text-slate-200 truncate pr-2" title={candidate.filename}>
                    {candidate.filename}
                  </h4>
                  <div className="flex items-center gap-2 mt-1 text-[10px] text-slate-500">
                    <span className="flex items-center gap-0.5">
                      <Calendar className="w-2.5 h-2.5" />
                      {candidate.years_of_experience} yrs
                    </span>
                    <span>•</span>
                    <span className="truncate max-w-[120px]" title={candidate.education?.join(', ') || 'N/A'}>
                      {candidate.education?.length > 0 ? candidate.education[0] : 'N/A'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Match Score Percentage Badge */}
              <div className={`px-2 py-1 rounded-lg border text-[10px] font-bold flex items-center gap-1 shrink-0 ${getScoreBg(candidate.final_score)}`}>
                <span className={`font-extrabold ${getScoreColor(candidate.final_score)}`}>
                  {candidate.final_score}%
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
