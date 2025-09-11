# db.py
import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

DB_PATH = Path("career_advisor.db")

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,                 -- 'user' | 'assistant'
  intent TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id INTEGER NOT NULL,        -- points to the assistant message
  rating INTEGER NOT NULL,            -- +1 or -1
  comment TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
);
"""

def get_convo() -> sqlite3.Connection:
    init_needed = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH.as_posix(), check_same_thread=False)
    if init_needed:
        conn.executescript(SCHEMA)
        conn.commit()
    return conn

def add_message(session_id: str, role: str, intent: str, content: str) -> int:
    conn = get_convo()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (session_id, role, intent, content) VALUES (?, ?, ?, ?)",
        (session_id, role, intent, content),
    )
    conn.commit()
    return cur.lastrowid

def get_history(session_id: str, limit: int = 10) -> List[Tuple]:
    conn = get_convo()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, role, intent, content, created_at FROM messages "
        "WHERE session_id = ? ORDER BY id DESC LIMIT ?",
        (session_id, limit),
    )
    return cur.fetchall()[::-1]

def add_feedback(message_id: int, rating: int, comment: Optional[str]) -> None:
    conn = get_convo()
    conn.execute(
        "INSERT INTO feedback (message_id, rating, comment) VALUES (?, ?, ?)",
        (message_id, rating, comment),
    )
    conn.commit()

def get_feedback_summary(session_id: str) -> Dict[str, Any]:
    conn = get_convo()
    q = """
    SELECT m.intent,
           SUM(CASE WHEN f.rating = 1 THEN 1 ELSE 0 END) as upvotes,
           SUM(CASE WHEN f.rating = -1 THEN 1 ELSE 0 END) as downvotes
    FROM messages m
    JOIN feedback f ON f.message_id = m.id
    WHERE m.session_id = ?
    GROUP BY m.intent
    ORDER BY upvotes - downvotes DESC
    """
    rows = conn.execute(q, (session_id,)).fetchall()
    return {"by_intent": rows}
