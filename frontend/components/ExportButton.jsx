import React, { useState } from 'react';
import { exportCSV } from '../api/client';

export default function ExportButton({ sessionId, disabled }) {
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    if (!sessionId) return;
    setExporting(true);
    try {
      await exportCSV(sessionId);
    } catch (err) {
      console.error('Failed to export CSV:', err);
      alert('Error exporting CSV: ' + (err.message || err));
    } finally {
      setExporting(false);
    }
  };

  return (
    <button
      onClick={handleExport}
      disabled={disabled || exporting || !sessionId}
      className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center gap-2 ${
        disabled || exporting || !sessionId
          ? 'bg-slate-900 border border-slate-800 text-slate-500 cursor-not-allowed'
          : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-900/20 active:scale-95'
      }`}
    >
      {exporting ? (
        <>
          <span className="animate-spin text-xs">⏳</span>
          Exporting CSV...
        </>
      ) : (
        <>
          <span>📥</span>
          Export Results to CSV
        </>
      )}
    </button>
  );
}
