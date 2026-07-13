import sqlite3
import json
import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("DATABASE_PATH", "resume_ranking.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection():
    """Returns a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database using schema.sql if it doesn't already exist."""
    conn = get_connection()
    try:
        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, 'r') as f:
                schema_script = f.read()
            conn.executescript(schema_script)
            conn.commit()
            logger.info("Database initialized successfully.")
        else:
            logger.error(f"Schema file not found at {SCHEMA_PATH}")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        conn.close()

def save_session(session_id: str, jd_text: str, jd_skills: List[str], alpha: float = 0.4):
    """Saves the session configuration to the database."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT OR REPLACE INTO sessions (session_id, jd_text, jd_skills, alpha)
            VALUES (?, ?, ?, ?)
            """,
            (session_id, jd_text, json.dumps(jd_skills), alpha)
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to save session {session_id}: {e}")
        raise
    finally:
        conn.close()

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves session details by session_id."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        if row:
            res = dict(row)
            res["jd_skills"] = json.loads(res["jd_skills"]) if res["jd_skills"] else []
            return res
        return None
    finally:
        conn.close()

def update_session_alpha(session_id: str, alpha: float):
    """Updates the alpha scoring weight for a session."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE sessions SET alpha = ? WHERE session_id = ?",
            (alpha, session_id)
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to update alpha for session {session_id}: {e}")
        raise
    finally:
        conn.close()

def save_candidate_results(session_id: str, candidates: List[Dict[str, Any]]):
    """Saves candidate results to the database in bulk."""
    conn = get_connection()
    try:
        # Clear existing candidates for this session to avoid duplicates
        conn.execute("DELETE FROM candidate_results WHERE session_id = ?", (session_id,))
        
        # Batch insert
        for cand in candidates:
            conn.execute(
                """
                INSERT INTO candidate_results (
                    session_id, filename, raw_text, tfidf_score, sbert_score, final_score,
                    skills, matched_skills, missing_skills, education, job_titles, 
                    years_of_experience, rank
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    cand["filename"],
                    cand.get("raw_text", ""),
                    cand["tfidf_score"],
                    cand["sbert_score"],
                    cand["final_score"],
                    json.dumps(cand.get("skills", [])),
                    json.dumps(cand.get("matched_skills", [])),
                    json.dumps(cand.get("missing_skills", [])),
                    json.dumps(cand.get("education", [])),
                    json.dumps(cand.get("job_titles", [])),
                    cand["years_of_experience"],
                    cand["rank"]
                )
            )
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to save candidate results for session {session_id}: {e}")
        raise
    finally:
        conn.close()

def get_candidate_results(session_id: str) -> List[Dict[str, Any]]:
    """Retrieves ranked candidate results for a session."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM candidate_results WHERE session_id = ? ORDER BY rank ASC",
            (session_id,)
        )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            d = dict(row)
            d["skills"] = json.loads(d["skills"]) if d["skills"] else []
            d["matched_skills"] = json.loads(d["matched_skills"]) if d["matched_skills"] else []
            d["missing_skills"] = json.loads(d["missing_skills"]) if d["missing_skills"] else []
            d["education"] = json.loads(d["education"]) if d["education"] else []
            d["job_titles"] = json.loads(d["job_titles"]) if d["job_titles"] else []
            results.append(d)
        return results
    finally:
        conn.close()
