import React, { useState, useEffect } from 'react';
import { Sparkles, FileSearch, RefreshCw, AlertCircle, Cpu, User, CheckCircle2, XCircle, Award, Briefcase, Calendar, Info, BarChart3, ListFilter } from 'lucide-react';
import FileUpload from './components/FileUpload';
import JDInput from './components/JDInput';
import WeightSliders from './components/WeightSliders';
import ResultsTable from './components/ResultsTable';
import PoolAnalytics from './components/PoolAnalytics';
import ExportButton from './components/ExportButton';
import { rankResumes, getResults } from './api/client';

export default function App() {
  const [files, setFiles] = useState([]);
  const [jdText, setJdText] = useState('');
  const [alpha, setAlpha] = useState(0.4);
  const [sessionId, setSessionId] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('list'); // 'list' or 'analytics'

  const handleRank = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      setError('Please upload at least one resume.');
      return;
    }
    if (jdText.trim().length < 50) {
      setError('Job description must be at least 50 characters.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSelectedCandidate(null);

    try {
      const data = await rankResumes(files, jdText, alpha);
      setSessionId(data.session_id);
      setCandidates(data.candidates);
      if (data.candidates && data.candidates.length > 0) {
        setSelectedCandidate(data.candidates[0]);
      }
    } catch (err) {
      console.error(err);
      setError(err.message || 'An error occurred during resume ranking.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleWeightChange = async (newAlpha) => {
    if (!sessionId) return;
    setIsLoading(true);
    setError(null);

    try {
      const data = await getResults(sessionId, newAlpha);
      setCandidates(data.candidates);
      
      // Update selected candidate details in sync
      if (selectedCandidate) {
        const updated = data.candidates.find(c => c.filename === selectedCandidate.filename);
        if (updated) {
          setSelectedCandidate(updated);
        } else if (data.candidates.length > 0) {
          setSelectedCandidate(data.candidates[0]);
        }
      }
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to update candidate ranks.');
    } finally {
      setIsLoading(false);
    }
  };

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
    <div className="h-screen w-screen overflow-hidden flex flex-col bg-brand-950 text-slate-100 font-sans">
      
      {/* Top Header */}
      <header className="h-14 border-b border-brand-800/30 bg-brand-950/80 backdrop-blur-md px-6 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <Sparkles className="w-6 h-6 text-brand-400" />
          <div>
            <h1 className="text-md font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-brand-300 to-accent-cyan">
              Smart Hire
            </h1>
            <p className="text-[10px] text-slate-500 font-medium">AI Recruitment CRM & Match Intelligence</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {sessionId && (
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-slate-500 font-semibold tracking-wider bg-brand-900/40 px-2.5 py-1 rounded-md border border-brand-800/20">
                Session: {sessionId.substring(0, 8)}
              </span>
              <ExportButton sessionId={sessionId} />
            </div>
          )}
          <div className="flex items-center gap-1.5 px-2.5 py-1 bg-brand-900/20 border border-brand-800/35 rounded-full text-[10px] text-slate-400">
            <Sparkles className="w-3 h-3 text-accent-cyan" />
            <span>TF-IDF + SBERT Hybrid Scorer</span>
          </div>
        </div>
      </header>

      {/* Main CRM Workspace (Exactly height of screen minus header) */}
      <main className="flex-1 min-h-0 w-full grid grid-cols-1 lg:grid-cols-12 p-4 gap-4 overflow-hidden">
        
        {/* COLUMN 1: Setup & Upload (Left) */}
        <section className="lg:col-span-3 flex flex-col min-h-0 glass-panel p-4 gap-4 overflow-hidden">
          <div className="flex items-center gap-2 pb-2 border-b border-brand-850">
            <FileSearch className="w-4 h-4 text-brand-400" />
            <h2 className="text-sm font-bold text-slate-200">Setup & Input</h2>
          </div>
          
          <div className="flex-1 min-h-0 overflow-y-auto space-y-4 pr-1">
            <FileUpload files={files} setFiles={setFiles} />
            <JDInput jdText={jdText} setJdText={setJdText} />
          </div>

          <button
            onClick={handleRank}
            disabled={isLoading || files.length === 0 || jdText.trim().length < 50}
            className={`w-full py-3 rounded-xl font-bold text-xs transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shrink-0 ${
              isLoading || files.length === 0 || jdText.trim().length < 50
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50 shadow-none'
                : 'bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 active:scale-95 text-white cursor-pointer'
            }`}
          >
            {isLoading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Cpu className="w-4 h-4" />
                <span>Run Candidate Scoring</span>
              </>
            )}
          </button>
        </section>

        {/* COLUMN 2: Rankings List (Middle) */}
        <section className="lg:col-span-5 flex flex-col min-h-0 glass-panel p-4 gap-4 overflow-hidden relative">
          
          {/* Embedding loading overlay */}
          {isLoading && candidates.length > 0 && (
            <div className="absolute inset-0 bg-brand-950/60 backdrop-blur-sm flex items-center justify-center rounded-2xl z-20">
              <div className="glass-panel p-4 flex items-center gap-3">
                <RefreshCw className="w-4 h-4 animate-spin text-brand-400" />
                <span className="text-xs font-semibold text-slate-200">Recalculating match scores...</span>
              </div>
            </div>
          )}

          {sessionId && (
            <div className="shrink-0 space-y-3.5">
              <WeightSliders 
                alpha={alpha} 
                setAlpha={setAlpha} 
                onWeightChange={handleWeightChange} 
              />
              
              {/* Tab Switcher */}
              <div className="flex bg-brand-950/50 border border-brand-800/20 p-1 rounded-xl">
                <button
                  onClick={() => setActiveTab('list')}
                  className={`flex-1 py-2 rounded-lg text-[10px] font-bold tracking-wide transition-all duration-150 flex items-center justify-center gap-1.5 ${
                    activeTab === 'list'
                      ? 'bg-brand-900/60 text-slate-100 border border-brand-800/40 shadow-sm'
                      : 'text-slate-500 hover:text-slate-300 border border-transparent'
                  }`}
                >
                  <ListFilter className="w-3.5 h-3.5" />
                  Candidate Rankings
                </button>
                <button
                  onClick={() => setActiveTab('analytics')}
                  className={`flex-1 py-2 rounded-lg text-[10px] font-bold tracking-wide transition-all duration-150 flex items-center justify-center gap-1.5 ${
                    activeTab === 'analytics'
                      ? 'bg-brand-900/60 text-slate-100 border border-brand-800/40 shadow-sm'
                      : 'text-slate-500 hover:text-slate-300 border border-transparent'
                  }`}
                >
                  <BarChart3 className="w-3.5 h-3.5" />
                  Pool Analytics & Gaps
                </button>
              </div>
            </div>
          )}

          <div className="flex-1 min-h-0 flex flex-col">
            {activeTab === 'list' ? (
              <ResultsTable 
                candidates={candidates} 
                selectedCandidate={selectedCandidate} 
                setSelectedCandidate={setSelectedCandidate} 
              />
            ) : (
              <PoolAnalytics candidates={candidates} />
            )}
          </div>
        </section>

        {/* COLUMN 3: Candidate details and gaps (Right) */}
        <section className="lg:col-span-4 flex flex-col min-h-0 glass-panel p-4 gap-4 overflow-hidden">
          <div className="flex items-center gap-2 pb-2 border-b border-brand-850 shrink-0">
            <User className="w-4 h-4 text-brand-400" />
            <h2 className="text-sm font-bold text-slate-200">Candidate Details</h2>
          </div>

          <div className="flex-1 min-h-0 overflow-y-auto pr-1">
            {selectedCandidate ? (
              <div className="space-y-5 animate-fade-in">
                {/* Header Summary */}
                <div className="flex justify-between items-start gap-4 bg-brand-900/10 border border-brand-800/20 p-4 rounded-xl">
                  <div className="overflow-hidden">
                    <h3 className="font-bold text-md text-slate-100 truncate" title={selectedCandidate.filename}>
                      {selectedCandidate.filename}
                    </h3>
                    <div className="flex flex-wrap items-center gap-2 mt-1 text-[11px] text-slate-500 font-medium">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-brand-400" />
                        {selectedCandidate.years_of_experience} yrs experience
                      </span>
                    </div>
                  </div>

                  <div className={`px-2.5 py-1 rounded-lg border text-xs font-bold flex items-center gap-1.5 shrink-0 ${getScoreBg(selectedCandidate.final_score)}`}>
                    <span className="text-[9px] text-slate-500 font-semibold tracking-wider">FIT</span>
                    <span className={`text-sm font-extrabold ${getScoreColor(selectedCandidate.final_score)}`}>
                      {selectedCandidate.final_score}%
                    </span>
                  </div>
                </div>

                {/* Score Breakdown */}
                <div className="grid grid-cols-2 gap-3 text-xs bg-brand-950/40 border border-brand-800/10 rounded-xl p-3">
                  <div>
                    <span className="text-[9px] font-bold text-slate-500 uppercase tracking-wide block mb-0.5">Lexical Similarity</span>
                    <span className="text-sm font-bold text-brand-400">{selectedCandidate.tfidf_score}%</span>
                    <span className="text-[9px] text-slate-600 block mt-0.5">Exact word frequency</span>
                  </div>
                  <div>
                    <span className="text-[9px] font-bold text-slate-500 uppercase tracking-wide block mb-0.5">Semantic Similarity</span>
                    <span className="text-sm font-bold text-accent-cyan">{selectedCandidate.sbert_score}%</span>
                    <span className="text-[9px] text-slate-600 block mt-0.5">Contextual synonym fit</span>
                  </div>
                </div>

                {/* Technical Skills Matching */}
                <div className="space-y-3">
                  {/* Matched */}
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-1.5 text-[10px] font-bold text-accent-emerald uppercase tracking-wider">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span>Matched Skills ({selectedCandidate.matched_skills?.length || 0})</span>
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedCandidate.matched_skills && selectedCandidate.matched_skills.length > 0 ? (
                        selectedCandidate.matched_skills.map((skill, idx) => (
                          <span 
                            key={`${skill}-${idx}`} 
                            className="px-2 py-0.5 rounded-md text-[10px] bg-accent-emerald/10 border border-accent-emerald/20 text-slate-300 font-medium"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-slate-500 italic">No matching skills found</span>
                      )}
                    </div>
                  </div>

                  {/* Gaps */}
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-1.5 text-[10px] font-bold text-accent-rose uppercase tracking-wider">
                      <XCircle className="w-3.5 h-3.5 shrink-0" />
                      <span>Missing Skills ({selectedCandidate.missing_skills?.length || 0})</span>
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedCandidate.missing_skills && selectedCandidate.missing_skills.length > 0 ? (
                        selectedCandidate.missing_skills.map((skill, idx) => (
                          <span 
                            key={`${skill}-${idx}`} 
                            className="px-2 py-0.5 rounded-md text-[10px] bg-accent-rose/5 border border-accent-rose/20 text-slate-400 font-medium"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span className="text-[10px] text-accent-emerald font-semibold italic">Perfect skills match!</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Professional details */}
                <div className="border-t border-brand-850/50 pt-4 space-y-4 text-xs text-slate-400">
                  <div className="flex gap-2">
                    <Briefcase className="w-4 h-4 text-brand-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-semibold text-slate-300 block mb-0.5">Identified Job Roles</span>
                      {selectedCandidate.job_titles && selectedCandidate.job_titles.length > 0 ? (
                        <p className="leading-relaxed text-slate-400">{selectedCandidate.job_titles.join(', ')}</p>
                      ) : (
                        <p className="italic text-slate-600">None extracted</p>
                      )}
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Award className="w-4 h-4 text-brand-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-semibold text-slate-300 block mb-0.5">Academic Credentials</span>
                      {selectedCandidate.education && selectedCandidate.education.length > 0 ? (
                        <p className="leading-relaxed text-slate-400">{selectedCandidate.education.join(', ')}</p>
                      ) : (
                        <p className="italic text-slate-600">None extracted</p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-2">
                <User className="w-10 h-10 text-slate-700" />
                <h3 className="text-sm font-semibold text-slate-400">No Candidate Selected</h3>
                <p className="text-xs text-slate-600 max-w-[200px] leading-relaxed">
                  Click on any candidate card in the rankings list to view their detailed skills breakdown.
                </p>
              </div>
            )}
          </div>

          {error && (
            <div className="flex items-start gap-2 p-3 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-[11px] shrink-0">
              <AlertCircle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}
        </section>

      </main>
    </div>
  );
}
