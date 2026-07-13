-- schema.sql
-- Table to store session-wide information
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    jd_text TEXT NOT NULL,
    jd_skills TEXT, -- JSON string list of skills required
    alpha REAL DEFAULT 0.4,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store individual candidate resume parsing and scoring results
CREATE TABLE IF NOT EXISTS candidate_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    tfidf_score REAL NOT NULL,
    sbert_score REAL NOT NULL,
    final_score REAL NOT NULL,
    skills TEXT, -- JSON string list
    matched_skills TEXT, -- JSON string list
    missing_skills TEXT, -- JSON string list
    education TEXT, -- JSON string list
    job_titles TEXT, -- JSON string list
    years_of_experience REAL NOT NULL,
    rank INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);
