import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "chat_history.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES sessions(id),
    panel TEXT NOT NULL CHECK(panel IN ('baseline', 'injected')),
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    template_id TEXT,
    created_at TEXT NOT NULL
);
"""


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def create_session():
    conn = _connect()
    cur = conn.execute(
        "INSERT INTO sessions (created_at) VALUES (?)",
        (datetime.now(timezone.utc).isoformat(),),
    )
    conn.commit()
    session_id = cur.lastrowid
    conn.close()
    return session_id


def save_message(session_id, panel, role, content, template_id=None):
    conn = _connect()
    conn.execute(
        """INSERT INTO messages (session_id, panel, role, content, template_id, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (session_id, panel, role, content, template_id, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()


def get_history(session_id, panel):
    conn = _connect()
    rows = conn.execute(
        """SELECT role, content FROM messages
           WHERE session_id = ? AND panel = ?
           ORDER BY id ASC""",
        (session_id, panel),
    ).fetchall()
    conn.close()
    return [{"role": r["role"], "content": r["content"]} for r in rows]


def list_sessions():
    conn = _connect()
    rows = conn.execute(
        """SELECT s.id, s.created_at,
                  (SELECT content FROM messages
                   WHERE session_id = s.id AND panel = 'baseline' AND role = 'user'
                   ORDER BY id ASC LIMIT 1) AS first_message
           FROM sessions s
           ORDER BY s.id DESC"""
    ).fetchall()
    conn.close()
    return [
        {"id": r["id"], "created_at": r["created_at"], "first_message": r["first_message"]}
        for r in rows
    ]
