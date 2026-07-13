import React from 'react';
import { Download } from 'lucide-react';
import { getExportUrl } from '../api/client';

export default function ExportButton({ sessionId }) {
  const handleExport = () => {
    if (!sessionId) return;
    const url = getExportUrl(sessionId);
    window.open(url, '_blank');
  };

  return (
    <button
      onClick={handleExport}
      disabled={!sessionId}
      className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 shadow-md ${
        sessionId
          ? 'bg-accent-emerald text-white hover:bg-emerald-600 active:scale-95 cursor-pointer'
          : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50 shadow-none'
      }`}
    >
      <Download className="w-4 h-4" />
      <span>Export Ranked CSV</span>
    </button>
  );
}
