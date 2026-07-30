import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import settings

DB_PATH = Path(settings.HISTORY_DB_PATH)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

_local = threading.local()


def _get_conn() -> sqlite3.Connection:
    if not hasattr(_local, "conn") or _local.conn is None:
        _local.conn = sqlite3.connect(str(DB_PATH))
        _local.conn.row_factory = sqlite3.Row
        _local.conn.execute("PRAGMA journal_mode=WAL")
        _local.conn.execute("PRAGMA synchronous=NORMAL")
    return _local.conn


def _init_db():
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id TEXT PRIMARY KEY,
            tool_slug TEXT NOT NULL,
            input TEXT NOT NULL,
            output TEXT NOT NULL,
            provider TEXT NOT NULL DEFAULT '',
            model TEXT NOT NULL DEFAULT '',
            duration_ms INTEGER DEFAULT 0,
            temperature REAL DEFAULT 0.0,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_history_tool_slug
        ON history(tool_slug)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_history_created_at
        ON history(created_at DESC)
    """)
    conn.commit()


_init_db()


def save_run(
    id: str,
    tool_slug: str,
    input: str,
    output: str,
    provider: str = "",
    model: str = "",
    duration_ms: int = 0,
    temperature: float = 0.0,
):
    conn = _get_conn()
    conn.execute(
        """INSERT INTO history (id, tool_slug, input, output, provider, model, duration_ms, temperature, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (id, tool_slug, input, output, provider, model, duration_ms, temperature, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()


def list_history(page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
    conn = _get_conn()
    total = conn.execute("SELECT COUNT(*) FROM history").fetchone()[0]
    offset = (page - 1) * page_size
    rows = conn.execute(
        "SELECT * FROM history ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (page_size, offset),
    ).fetchall()
    items = [dict(r) for r in rows]
    return items, total


def search_history(query: str, page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
    conn = _get_conn()
    like = f"%{query}%"
    total = conn.execute(
        "SELECT COUNT(*) FROM history WHERE input LIKE ? OR output LIKE ?",
        (like, like),
    ).fetchone()[0]
    offset = (page - 1) * page_size
    rows = conn.execute(
        "SELECT * FROM history WHERE input LIKE ? OR output LIKE ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (like, like, page_size, offset),
    ).fetchall()
    items = [dict(r) for r in rows]
    return items, total


def delete_entry(entry_id: str) -> bool:
    conn = _get_conn()
    cur = conn.execute("DELETE FROM history WHERE id = ?", (entry_id,))
    conn.commit()
    return cur.rowcount > 0
