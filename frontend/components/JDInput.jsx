import React, { useRef } from 'react';

export default function JDInput({ jdText, setJdText }) {
  const fileInputRef = useRef(null);

  const handleTextChange = (e) => {
    setJdText(e.target.value);
  };

  const handleClear = () => {
    setJdText('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Check if it's a text file
    if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setJdText(event.target.result);
      };
      reader.readAsText(file);
    } else {
      alert('Local file parsing is supported for .txt files. For other formats, please copy and paste the contents.');
      // Clear input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const charCount = jdText.length;
  const isLengthValid = charCount >= 50 && charCount <= 10000;

  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
          <span>📋</span> Job Description (JD)
        </h2>
        <div className="flex items-center gap-2">
          <label className="text-xs bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg cursor-pointer transition-colors font-medium">
            📂 Import .txt File
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept=".txt"
              className="hidden"
            />
          </label>
          {jdText && (
            <button
              onClick={handleClear}
              className="text-xs text-red-400 hover:text-red-300 transition-colors font-medium px-2 py-1.5"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      <div className="relative flex-1 flex flex-col">
        <textarea
          value={jdText}
          onChange={handleTextChange}
          placeholder="Paste the target job description here (minimum 50 characters, maximum 10,000 characters)..."
          className="glass-input w-full flex-1 min-h-[160px] p-4 rounded-xl text-slate-200 text-sm placeholder-slate-500 resize-none"
        />
        
        {/* Character count tracker badge */}
        <div className="absolute bottom-3 right-3 flex items-center gap-2 bg-slate-950/80 px-2 py-1 rounded-md border border-slate-800 text-[10px]">
          <span className={isLengthValid ? 'text-emerald-400 font-semibold' : 'text-slate-500'}>
            {charCount.toLocaleString()}
          </span>
          <span className="text-slate-600">/</span>
          <span className="text-slate-500">10,000</span>
        </div>
      </div>
      
      {charCount > 0 && !isLengthValid && (
        <p className="text-[11px] text-amber-400 mt-2 flex items-center gap-1.5">
          <span>⚠️</span> 
          {charCount < 50 
            ? `Needs at least ${50 - charCount} more characters to meet validation requirements.` 
            : `Exceeded character limit by ${charCount - 10000} characters.`}
        </p>
      )}
    </div>
  );
}
