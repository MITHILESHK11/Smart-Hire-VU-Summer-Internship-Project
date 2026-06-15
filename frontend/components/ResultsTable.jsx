import React from 'react';
import CandidateRow from './CandidateRow';

export default function ResultsTable({ candidates }) {
  if (!candidates || candidates.length === 0) {
    return (
      <div className="glass-panel text-center p-8 rounded-xl border border-slate-800">
        <p className="text-slate-500 text-sm">No candidates processed yet. Upload resumes and click "Rank Resumes" to view results.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/10 backdrop-blur-md">
        <table className="min-w-full divide-y divide-slate-800">
          <thead className="bg-slate-900/60">
            <tr>
              <th scope="col" className="px-6 py-3.5 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Rank
              </th>
              <th scope="col" className="px-6 py-3.5 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Filename
              </th>
              <th scope="col" className="px-6 py-3.5 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                TF-IDF %
              </th>
              <th scope="col" className="px-6 py-3.5 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                SBERT %
              </th>
              <th scope="col" className="px-6 py-3.5 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Final Score %
              </th>
              <th scope="col" className="px-6 py-3.5 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Missing Keywords
              </th>
              <th scope="col" className="relative px-6 py-3.5">
                <span className="sr-only">Toggle</span>
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 bg-transparent">
            {candidates.map((candidate, idx) => (
              <CandidateRow key={`${candidate.filename}-${idx}`} candidate={candidate} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
