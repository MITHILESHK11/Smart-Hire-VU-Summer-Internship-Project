import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import JDInput from './components/JDInput';
import WeightSliders from './components/WeightSliders';
import ResultsTable from './components/ResultsTable';
import ExportButton from './components/ExportButton';
import { rankResumes } from './api/client';

export default function App() {
  const [files, setFiles] = useState([]);
  const [jdText, setJdText] = useState('');
  const [alpha, setAlpha] = useState(0.3); // Default weight from Phase 1/3 (0.3)
  const [uploadError, setUploadError] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [results, setResults] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [processingTime, setProcessingTime] = useState(null);

  // Trigger ranking
  const handleRank = async (currentAlpha = alpha) => {
    if (files.length === 0) {
      setUploadError('Please upload at least one resume file first.');
      return;
    }
    if (!jdText || jdText.trim().length < 50) {
      setUploadError('Job description must be at least 50 characters long.');
      return;
    }

    setUploadError('');
    setLoading(true);
    setResults(null);
    
    // Simulate multi-step progress for premium UX feeling
    const steps = [
      'Ingesting documents...',
      'Preprocessing text & extracting lemmas...',
      'Extracting skills & experience (spaCy NER)...',
      'Computing TF-IDF cosine similarity...',
      'Generating Sentence-BERT semantic embeddings...',
      'Calculating hybrid scores & keyword gaps...'
    ];

    let currentStep = 0;
    setLoadingStep(steps[currentStep]);
    const stepInterval = setInterval(() => {
      if (currentStep < steps.length - 1) {
        currentStep++;
        setLoadingStep(steps[currentStep]);
      }
    }, 700);

    try {
      const data = await rankResumes(files, jdText, currentAlpha);
      clearInterval(stepInterval);
      setResults(data.ranked_candidates);
      setSessionId(data.session_id);
      setProcessingTime(data.processing_time_ms);
    } catch (err) {
      clearInterval(stepInterval);
      console.error(err);
      const detail = err.response?.data?.detail || err.message || 'Unknown processing error.';
      setUploadError(`Failed to process resumes: ${detail}`);
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  // Re-trigger ranking when alpha changes and results are already present
  const handleAlphaChange = (newAlpha) => {
    if (results && results.length > 0) {
      handleRank(newAlpha);
    }
  };

  // Calculate statistics for the results dashboard
  const getStats = () => {
    if (!results || results.length === 0) return null;
    const total = results.length;
    const topScore = (results[0].final_score * 100).toFixed(1) + '%';
    const topName = results[0].filename;
    const avgScore = (results.reduce((acc, curr) => acc + curr.final_score, 0) / total * 100).toFixed(1) + '%';
    return { total, topScore, topName, avgScore };
  };

  const stats = getStats();

  return (
    <div className="min-h-screen bg-slate-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black text-slate-100 p-4 md:p-8 flex flex-col">
      {/* Premium Header */}
      <header className="max-w-7xl mx-auto w-full mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-900 pb-6">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="text-3xl">🎯</span>
            <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight bg-gradient-to-r from-brand-400 via-brand-200 to-white bg-clip-text text-transparent">
              AI Resume Ranking Engine
            </h1>
          </div>
          <p className="text-slate-400 text-sm mt-1">
            Lexical TF-IDF + Semantic Sentence-BERT Hybrid Screening System
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Backend API Online
          </span>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto w-full flex-1 flex flex-col gap-6">
        
        {/* Row 1: Ingestion & JD Inputs */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-panel p-6 rounded-2xl flex flex-col">
            <FileUpload
              files={files}
              setFiles={setFiles}
              error={uploadError}
              setError={setUploadError}
            />
          </div>
          
          <div className="glass-panel p-6 rounded-2xl flex flex-col">
            <JDInput
              jdText={jdText}
              setJdText={setJdText}
            />
          </div>
        </section>

        {/* Row 2: Weights Sliders & Run CTA */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 items-end">
          <div className="md:col-span-2">
            <WeightSliders
              alpha={alpha}
              setAlpha={setAlpha}
              onAlphaChange={handleAlphaChange}
            />
          </div>
          <div>
            <button
              onClick={() => handleRank(alpha)}
              disabled={loading || files.length === 0 || jdText.length < 50}
              className={`w-full py-4 px-6 rounded-xl font-bold transition-all duration-300 shadow-xl flex items-center justify-center gap-2 text-base ${
                loading || files.length === 0 || jdText.length < 50
                  ? 'bg-slate-900 border border-slate-800 text-slate-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-brand-600 to-brand-500 text-white hover:from-brand-500 hover:to-brand-400 active:scale-98 shadow-brand-900/10'
              }`}
            >
              {loading ? (
                <>
                  <span className="animate-spin text-lg">⚙️</span>
                  <span>Processing...</span>
                </>
              ) : (
                <>
                  <span>⚡</span>
                  <span>Rank Resumes</span>
                </>
              )}
            </button>
          </div>
        </section>

        {/* Loading Progress State */}
        {loading && (
          <div className="glass-panel p-6 rounded-2xl border border-brand-500/10 flex flex-col items-center justify-center text-center animate-pulse">
            <div className="text-3xl mb-3 animate-spin">⏳</div>
            <p className="text-sm font-semibold text-brand-300">{loadingStep}</p>
            <p className="text-xs text-slate-500 mt-1">This takes only a few seconds. SBERT generates dense embeddings on-the-fly.</p>
          </div>
        )}

        {/* Row 3: Stats Dashboard (when results are available) */}
        {stats && !loading && (
          <section className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-fadeIn">
            <div className="glass-panel p-4 rounded-xl border border-slate-800/80 flex items-center gap-4">
              <div className="text-2xl p-2 bg-brand-500/10 rounded-lg text-brand-400">📊</div>
              <div>
                <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Total Evaluated</p>
                <p className="text-lg font-bold text-slate-200">{stats.total} Resumes</p>
              </div>
            </div>
            
            <div className="glass-panel p-4 rounded-xl border border-slate-800/80 flex items-center gap-4">
              <div className="text-2xl p-2 bg-emerald-500/10 rounded-lg text-emerald-400">🏆</div>
              <div className="min-w-0">
                <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Top Match</p>
                <p className="text-lg font-bold text-slate-200 truncate" title={stats.topName}>
                  {stats.topScore} ({stats.topName})
                </p>
              </div>
            </div>

            <div className="glass-panel p-4 rounded-xl border border-slate-800/80 flex items-center gap-4">
              <div className="text-2xl p-2 bg-purple-500/10 rounded-lg text-purple-400">📈</div>
              <div>
                <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Average Score</p>
                <p className="text-lg font-bold text-slate-200">{stats.avgScore}</p>
              </div>
            </div>
          </section>
        )}

        {/* Row 4: Results Display Section */}
        {results && !loading && (
          <section className="flex flex-col gap-4 animate-fadeIn">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                  <span>📊</span> Candidate Rankings
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Processed in {processingTime}ms. Click any row to expand details.
                </p>
              </div>
              <ExportButton sessionId={sessionId} disabled={loading} />
            </div>

            <ResultsTable candidates={results} />
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto w-full mt-12 pt-6 border-t border-slate-900 text-center text-xs text-slate-600">
        AI-Powered Resume Ranking System © {new Date().getFullYear()} — Built using FastAPI, spaCy, and Sentence-BERT.
      </footer>
    </div>
  );
}
