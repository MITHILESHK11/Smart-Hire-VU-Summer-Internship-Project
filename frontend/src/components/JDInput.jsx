import React, { useState, useRef } from 'react';
import { FileText, FileUp, AlertCircle } from 'lucide-react';

export default function JDInput({ jdText, setJdText }) {
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleTextChange = (e) => {
    const text = e.target.value;
    setJdText(text);
    validate(text);
  };

  const validate = (text) => {
    setError(null);
    const cleaned = text.trim();
    if (cleaned.length > 0 && cleaned.length < 50) {
      setError('Job description is too short (min 50 characters).');
    } else if (cleaned.length > 10000) {
      setError('Job description exceeds the 10,000 character limit.');
    }
  };

  const handleFileUpload = (e) => {
    setError(null);
    const file = e.target.files[0];
    if (!file) return;

    if (file.type !== 'text/plain' && !file.name.endsWith('.txt')) {
      setError('Only plain text (.txt) files are supported for job descriptions.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target.result;
      setJdText(text);
      validate(text);
    };
    reader.onerror = () => {
      setError('Failed to read file.');
    };
    reader.readAsText(file);
  };

  const wordCount = jdText.trim() === '' ? 0 : jdText.trim().split(/\s+/).length;
  const charCount = jdText.length;

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <label className="block text-sm font-semibold text-slate-300 uppercase tracking-wider">
          Job Description
        </label>
        
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center gap-1.5 text-xs text-brand-400 hover:text-brand-300 font-medium transition-colors"
        >
          <FileUp className="w-3.5 h-3.5" />
          <span>Upload .txt file</span>
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".txt"
          onChange={handleFileUpload}
          className="hidden"
        />
      </div>

      <div className="relative">
        <textarea
          value={jdText}
          onChange={handleTextChange}
          placeholder="Paste the job description here, or upload a .txt file..."
          rows={4}
          className="w-full glass-input resize-y min-h-[100px] text-sm leading-relaxed"
        />
        
        <div className="absolute bottom-3 right-3 text-[11px] text-slate-500 bg-brand-950/80 px-2 py-1 rounded-md border border-brand-800/10 flex gap-3">
          <span>{wordCount} words</span>
          <span>{charCount} / 10,000 chars</span>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-sm">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
