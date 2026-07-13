import React, { useState, useRef } from 'react';
import { Upload, FileText, X, AlertCircle } from 'lucide-react';

export default function FileUpload({ files, setFiles }) {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFiles = (newFiles) => {
    setError(null);
    const validFiles = [];
    const maxSizeBytes = 5 * 1024 * 1024; // 5MB

    for (let i = 0; i < newFiles.length; i++) {
      const file = newFiles[i];
      const extension = file.name.split('.').pop().toLowerCase();
      
      if (extension !== 'pdf' && extension !== 'docx') {
        setError('Only PDF and Word (.docx) resumes are allowed.');
        continue;
      }
      
      if (file.size > maxSizeBytes) {
        setError(`"${file.name}" exceeds the 5MB size limit.`);
        continue;
      }

      // Check if file is already added
      if (files.some(f => f.name === file.name && f.size === file.size)) {
        continue;
      }

      validFiles.push(file);
    }

    if (validFiles.length > 0) {
      setFiles((prev) => [...prev, ...validFiles]);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const removeFile = (indexToRemove) => {
    setFiles((prev) => prev.filter((_, idx) => idx !== indexToRemove));
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const formatSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = 1;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-4">
      <label className="block text-sm font-semibold text-slate-300 uppercase tracking-wider">
        Upload Candidate Resumes
      </label>
      
      <div
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={triggerFileInput}
        className={`border-2 border-dashed rounded-2xl p-4 text-center cursor-pointer transition-all duration-200 glass-panel glass-panel-hover flex flex-col items-center justify-center min-h-[115px] ${
          dragActive ? 'border-brand-500 bg-brand-500/10 scale-[0.99]' : 'border-brand-800/40'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.docx"
          onChange={handleInputChange}
          className="hidden"
        />
        
        <div className="p-2 bg-brand-500/10 rounded-full text-brand-400 mb-1.5 group-hover:scale-110 transition-transform duration-200">
          <Upload className="w-5 h-5" />
        </div>
        
        <p className="text-slate-200 text-xs font-medium">
          Drag & drop resumes, or <span className="text-brand-400 hover:text-brand-300 underline font-semibold">browse</span>
        </p>
        <p className="text-[10px] text-slate-500 mt-1">
          PDF / DOCX (Max 5MB each)
        </p>
      </div>

      {error && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-accent-rose/10 border border-accent-rose/30 text-accent-rose text-sm">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {files.length > 0 && (
        <div className="space-y-2 max-h-[110px] overflow-y-auto pr-1">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex justify-between items-center px-1">
            <span>Staged Resumes ({files.length})</span>
            <button 
              type="button" 
              onClick={() => setFiles([])}
              className="text-accent-rose hover:text-rose-400 transition-colors lowercase font-normal"
            >
              Clear all
            </button>
          </div>
          
          <div className="grid gap-2">
            {files.map((file, idx) => (
              <div 
                key={`${file.name}-${idx}`} 
                className="flex items-center justify-between p-3 rounded-xl bg-brand-950/40 border border-brand-800/20 text-slate-300 animate-fade-in"
              >
                <div className="flex items-center gap-3 overflow-hidden">
                  <FileText className="w-5 h-5 text-brand-400 shrink-0" />
                  <div className="overflow-hidden">
                    <p className="text-sm font-medium truncate pr-4 text-slate-200">{file.name}</p>
                    <p className="text-xs text-slate-500">{formatSize(file.size)}</p>
                  </div>
                </div>
                
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(idx);
                  }}
                  className="p-1 hover:bg-brand-500/10 rounded-lg text-slate-400 hover:text-accent-rose transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
