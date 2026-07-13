import React, { useState } from 'react';
import { BarChart3, TrendingUp, Users, Calendar, Award, AlertTriangle, Layers } from 'lucide-react';

export default function PoolAnalytics({ candidates }) {
  const [hoveredDot, setHoveredDot] = useState(null);

  if (!candidates || candidates.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center p-8 space-y-3">
        <BarChart3 className="w-12 h-12 text-slate-700 mx-auto" />
        <h3 className="text-sm font-semibold text-slate-400">No Analytics Data</h3>
        <p className="text-xs text-slate-600 max-w-xs leading-relaxed">
          Upload resumes and analyze candidate scores to view aggregate talent pool metrics.
        </p>
      </div>
    );
  }

  // 1. Calculate General Pool Stats
  const totalPool = candidates.length;
  const avgScore = Math.round(candidates.reduce((sum, c) => sum + c.final_score, 0) / totalPool);
  const avgExperience = Number((candidates.reduce((sum, c) => sum + c.years_of_experience, 0) / totalPool).toFixed(1));
  
  // Find top fit
  const topFit = [...candidates].sort((a, b) => b.final_score - a.final_score)[0];

  // 2. Score Categories Distribution
  const highMatch = candidates.filter(c => c.final_score >= 70).length;
  const midMatch = candidates.filter(c => c.final_score >= 50 && c.final_score < 70).length;
  const lowMatch = candidates.filter(c => c.final_score < 50).length;

  const highPct = Math.round((highMatch / totalPool) * 100) || 0;
  const midPct = Math.round((midMatch / totalPool) * 100) || 0;
  const lowPct = Math.round((lowMatch / totalPool) * 100) || 0;

  // 3. Extract Target Skills and Match Coverage Frequencies
  const allTargetSkills = Array.from(new Set(
    candidates.flatMap(c => [...(c.matched_skills || []), ...(c.missing_skills || [])])
  ));

  const skillCoverage = allTargetSkills.map(skill => {
    const matchedCount = candidates.filter(c => c.matched_skills?.includes(skill)).length;
    const matchPct = Math.round((matchedCount / totalPool) * 100);
    return { skill, matchedCount, matchPct };
  }).sort((a, b) => b.matchPct - a.matchPct);

  // 4. Determine Scatterplot Coordinates for Experience vs Fit
  // Experience limits: 0 to maxExp (minimum 5 for scale)
  const maxExp = Math.max(...candidates.map(c => c.years_of_experience), 5);
  
  return (
    <div className="flex-1 flex flex-col min-h-0 space-y-4 overflow-y-auto pr-1">
      
      {/* Top Row: KPI Cards */}
      <div className="grid grid-cols-4 gap-3 shrink-0">
        <div className="p-3 bg-brand-900/10 border border-brand-800/10 rounded-xl flex flex-col justify-between">
          <span className="text-[9px] text-slate-500 font-bold uppercase tracking-wider block">Candidate Pool</span>
          <div className="flex items-baseline gap-1 mt-1">
            <span className="text-xl font-black text-slate-200">{totalPool}</span>
            <span className="text-[10px] text-slate-500 font-medium">resumes</span>
          </div>
        </div>

        <div className="p-3 bg-brand-900/10 border border-brand-800/10 rounded-xl flex flex-col justify-between">
          <span className="text-[9px] text-slate-500 font-bold uppercase tracking-wider block">Avg Match Fit</span>
          <div className="flex items-baseline gap-1 mt-1">
            <span className="text-xl font-black text-brand-400">{avgScore}%</span>
            <span className="text-[10px] text-slate-500 font-medium">score</span>
          </div>
        </div>

        <div className="p-3 bg-brand-900/10 border border-brand-800/10 rounded-xl flex flex-col justify-between">
          <span className="text-[9px] text-slate-500 font-bold uppercase tracking-wider block">Avg Experience</span>
          <div className="flex items-baseline gap-1 mt-1">
            <span className="text-xl font-black text-accent-cyan">{avgExperience}</span>
            <span className="text-[10px] text-slate-500 font-medium">yrs</span>
          </div>
        </div>

        <div className="p-3 bg-brand-900/10 border border-brand-800/10 rounded-xl flex flex-col justify-between overflow-hidden">
          <span className="text-[9px] text-slate-500 font-bold uppercase tracking-wider block truncate">Best Candidate</span>
          <div className="mt-1">
            <span className="text-xs font-black text-accent-emerald block truncate" title={topFit.filename}>
              {topFit.filename.split('.')[0]}
            </span>
            <span className="text-[9px] text-slate-500 font-medium">{topFit.final_score}% match</span>
          </div>
        </div>
      </div>

      {/* Middle Grid: Score Distribution & Scatterplot */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 shrink-0">
        
        {/* Score Distribution Chart */}
        <div className="bg-brand-950/20 border border-brand-800/10 rounded-xl p-3.5 flex flex-col">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <TrendingUp className="w-3.5 h-3.5 text-brand-400" />
            Fit Score Breakdown
          </h4>
          
          <div className="flex-1 flex flex-col justify-center space-y-3">
            {/* High Fit */}
            <div className="space-y-1">
              <div className="flex justify-between text-[10px] font-medium text-slate-400">
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-accent-emerald" />
                  Strong Match (&ge; 70%)
                </span>
                <span className="font-bold text-accent-emerald">{highMatch} candidates ({highPct}%)</span>
              </div>
              <div className="w-full h-2.5 bg-brand-900/20 rounded-full overflow-hidden border border-brand-800/10">
                <div 
                  className="h-full bg-accent-emerald rounded-full transition-all duration-500" 
                  style={{ width: `${highPct}%` }}
                />
              </div>
            </div>

            {/* Mid Fit */}
            <div className="space-y-1">
              <div className="flex justify-between text-[10px] font-medium text-slate-400">
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-accent-amber" />
                  Good Match (50% - 69%)
                </span>
                <span className="font-bold text-accent-amber">{midMatch} candidates ({midPct}%)</span>
              </div>
              <div className="w-full h-2.5 bg-brand-900/20 rounded-full overflow-hidden border border-brand-800/10">
                <div 
                  className="h-full bg-accent-amber rounded-full transition-all duration-500" 
                  style={{ width: `${midPct}%` }}
                />
              </div>
            </div>

            {/* Low Fit */}
            <div className="space-y-1">
              <div className="flex justify-between text-[10px] font-medium text-slate-400">
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-accent-rose" />
                  Weak Match (&lt; 50%)
                </span>
                <span className="font-bold text-accent-rose">{lowMatch} candidates ({lowPct}%)</span>
              </div>
              <div className="w-full h-2.5 bg-brand-900/20 rounded-full overflow-hidden border border-brand-800/10">
                <div 
                  className="h-full bg-accent-rose rounded-full transition-all duration-500" 
                  style={{ width: `${lowPct}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Experience vs. Fit Scatterplot */}
        <div className="bg-brand-950/20 border border-brand-800/10 rounded-xl p-3.5 flex flex-col relative">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-brand-400" />
            Experience vs. Match Fit
          </h4>

          {/* Chart Area */}
          <div className="relative w-full h-[105px] border-b border-l border-brand-800/40 mt-1 flex items-end">
            {/* Grid Line Guides */}
            <div className="absolute inset-0 flex flex-col justify-between pointer-events-none opacity-20">
              <div className="w-full border-t border-dashed border-slate-600 text-[8px] text-slate-500 pl-1 pt-0.5">100% Fit</div>
              <div className="w-full border-t border-dashed border-slate-600 text-[8px] text-slate-500 pl-1 pt-0.5">50% Fit</div>
              <div className="w-full text-[8px] text-slate-500 pl-1 pt-0.5">0% Fit</div>
            </div>

            {/* Candidate Dots */}
            {candidates.map((c, i) => {
              // Calculate relative positioning
              // X: Experience (from 0 to maxExp)
              const xPct = maxExp > 0 ? (c.years_of_experience / maxExp) * 85 + 5 : 50;
              // Y: Match Score (from 0 to 100)
              const yPct = c.final_score;

              let dotColor = 'bg-accent-rose shadow-accent-rose/30';
              if (c.final_score >= 70) dotColor = 'bg-accent-emerald shadow-accent-emerald/30';
              else if (c.final_score >= 50) dotColor = 'bg-accent-amber shadow-accent-amber/30';

              return (
                <div
                  key={c.filename}
                  className={`absolute w-3.5 h-3.5 rounded-full border-2 border-brand-950 hover:scale-150 cursor-pointer shadow-md transition-all duration-150 ${dotColor} ${
                    hoveredDot && hoveredDot.filename === c.filename ? 'scale-150 ring-2 ring-brand-300' : ''
                  }`}
                  style={{
                    left: `${xPct}%`,
                    bottom: `calc(${yPct}% - 7px)`
                  }}
                  onMouseEnter={() => setHoveredDot(c)}
                  onMouseLeave={() => setHoveredDot(null)}
                />
              );
            })}
          </div>

          {/* X-Axis labels */}
          <div className="flex justify-between px-1.5 mt-1 text-[8px] text-slate-500 font-bold">
            <span>0 yrs exp</span>
            <span>{Math.round(maxExp / 2)} yrs</span>
            <span>{maxExp} yrs exp</span>
          </div>

          {/* Hover tooltips */}
          <div className="h-6 mt-1.5 flex items-center justify-center">
            {hoveredDot ? (
              <span className="text-[10px] font-semibold text-slate-300 bg-brand-900/50 px-2 py-0.5 rounded-md border border-brand-800/30 truncate max-w-[280px]">
                {hoveredDot.filename}: {hoveredDot.final_score}% match ({hoveredDot.years_of_experience} yrs)
              </span>
            ) : (
              <span className="text-[9px] text-slate-600 italic">Hover over candidate dots to identify sweet spots</span>
            )}
          </div>
        </div>

      </div>

      {/* Bottom Area: Skills Gap & Recruiting Focus */}
      <div className="bg-brand-950/20 border border-brand-800/10 rounded-xl p-3.5 flex flex-col flex-1 min-h-0">
        <div className="flex items-center justify-between mb-3 shrink-0">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-brand-400" />
            Candidate Pool Skills Gap
          </h4>
          <span className="text-[9px] text-slate-500 font-bold bg-brand-900/40 px-2 py-0.5 rounded-md border border-brand-800/20 uppercase">
            Recruiting Priority
          </span>
        </div>

        {/* Skill Coverage Progress Bars */}
        <div className="flex-1 min-h-0 overflow-y-auto space-y-2.5 pr-1">
          {skillCoverage.length > 0 ? (
            skillCoverage.map(({ skill, matchedCount, matchPct }) => {
              // Priority label and color logic based on pool gap
              let priorityText = 'High Coverage';
              let priorityColor = 'text-accent-emerald bg-accent-emerald/10 border-accent-emerald/20';
              let progressColor = 'bg-accent-emerald';

              if (matchPct <= 30) {
                priorityText = 'Critical Gap';
                priorityColor = 'text-accent-rose bg-accent-rose/10 border-accent-rose/20';
                progressColor = 'bg-accent-rose';
              } else if (matchPct <= 60) {
                priorityText = 'Moderate Gap';
                priorityColor = 'text-accent-amber bg-accent-amber/10 border-accent-amber/20';
                progressColor = 'bg-accent-amber';
              }

              return (
                <div key={skill} className="space-y-1 text-xs">
                  <div className="flex justify-between items-center text-[10px] font-bold">
                    <span className="text-slate-300 font-semibold">{skill}</span>
                    <div className="flex items-center gap-2">
                      <span className={`text-[8px] font-extrabold uppercase px-1.5 py-0.2 rounded border ${priorityColor}`}>
                        {priorityText}
                      </span>
                      <span className="text-slate-400 font-black">{matchPct}% match ({matchedCount}/{totalPool})</span>
                    </div>
                  </div>
                  <div className="w-full h-2 bg-brand-900/20 rounded-full overflow-hidden border border-brand-800/10">
                    <div 
                      className={`h-full rounded-full transition-all duration-500 ${progressColor}`}
                      style={{ width: `${matchPct}%` }}
                    />
                  </div>
                </div>
              );
            })
          ) : (
            <span className="text-xs text-slate-500 italic block text-center py-4">
              No target skills extracted from candidate resumes yet.
            </span>
          )}
        </div>
      </div>

    </div>
  );
}
