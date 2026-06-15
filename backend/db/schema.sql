-- schema.sql
-- SQLite Database Schema for AI-Powered Resume Ranking System

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    jd_text TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED'))
);

CREATE TABLE IF NOT EXISTS resumes (
    resume_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    parsed_skills TEXT,        -- Stored as JSON string or comma-separated list
    parsed_education TEXT,     -- Stored as JSON string
    parsed_experience TEXT,    -- Stored as JSON string
    FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS results (
    result_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    resume_id TEXT NOT NULL,
    tfidf_score REAL NOT NULL,
    sbert_score REAL NOT NULL,
    final_score REAL NOT NULL,
    missing_keywords TEXT,     -- Stored as JSON string or comma-separated list
    rank_position INTEGER NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes (resume_id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_resumes_session ON resumes (session_id);
CREATE INDEX IF NOT EXISTS idx_results_session ON results (session_id);
CREATE INDEX IF NOT EXISTS idx_results_final_score ON results (final_score DESC);
