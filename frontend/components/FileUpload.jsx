import React from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileUpload({ files, setFiles, error, setError }) {
  const onDrop = (acceptedFiles, rejectedFiles) => {
    setError('');

    // Handle rejections from dropzone validator
    if (rejectedFiles.length > 0) {
      setError('Invalid file type. Only PDF and DOCX documents are accepted.');
      return;
    }

    // Check count limit
    const totalFiles = files.length + acceptedFiles.length;
    if (totalFiles > 50) {
      setError('Maximum limit of 50 resumes exceeded. Please remove some files.');
      return;
    }

    // Append to existing files list
    setFiles((prev) => [...prev, ...acceptedFiles]);
  };

  const removeFile = (indexToRemove) => {
    setFiles((prev) => prev.filter((_, idx) => idx !== indexToRemove));
    setError('');
  };

  const clearFiles = () => {
    setFiles([]);
    setError('');
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 50,
  });

  const formatSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="flex flex-col h-full">
      <h2 className="text-lg font-semibold text-slate-200 mb-3 flex items-center gap-2">
        <span>📁</span> Upload Candidate Resumes
      </h2>
      
      {/* Dropzone container */}
      <div
        {...getRootProps()}
        className={`glass-input flex-1 flex flex-col items-center justify-center border-2 border-dashed p-6 rounded-xl cursor-pointer hover:border-brand-400 hover:bg-slate-900/40 transition-all ${
          isDragActive ? 'border-brand-500 bg-brand-500/5' : 'border-slate-700'
        }`}
      >
        <input {...getInputProps()} />
        <div className="text-4xl mb-3 animate-pulse-slow">📤</div>
        <p className="text-sm font-medium text-slate-300 text-center">
          {isDragActive ? 'Drop files here...' : 'Drag & drop resumes here, or click to browse'}
        </p>
        <p className="text-xs text-slate-500 mt-2">
          Accepts PDF and DOCX only (Max 50 files, 5MB each)
        </p>
      </div>

      {error && (
        <div className="mt-3 text-xs bg-red-500/10 border border-red-500/20 text-red-400 p-2.5 rounded-lg flex items-center gap-2">
          <span>⚠️</span> {error}
        </div>
      )}

      {/* Selected File list */}
      {files.length > 0 && (
        <div className="mt-4 flex flex-col flex-1 max-h-[220px]">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Selected Files ({files.length}/50)
            </span>
            <button
              onClick={clearFiles}
              className="text-xs text-red-400 hover:text-red-300 transition-colors font-medium"
            >
              Clear All
            </button>
          </div>
          
          <div className="overflow-y-auto pr-1 flex-1 space-y-1.5">
            {files.map((file, idx) => (
              <div
                key={`${file.name}-${idx}`}
                className="flex items-center justify-between p-2 rounded-lg bg-slate-900/60 border border-slate-800/80 hover:border-slate-700/80 transition-all group"
              >
                <div className="flex items-center gap-2 min-w-0 pr-3">
                  <span className="text-lg">
                    {file.name.endsWith('.docx') ? '📝' : '📄'}
                  </span>
                  <div className="min-w-0">
                    <p className="text-xs font-medium text-slate-200 truncate">{file.name}</p>
                    <p className="text-[10px] text-slate-500">{formatSize(file.size)}</p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(idx)}
                  className="text-slate-500 hover:text-red-400 p-1 rounded transition-colors"
                  title="Remove file"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
