import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.core.config import settings

DB_PATH = Path(settings.HISTORY_DB_PATH).parent / "kanban.db"
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
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS kanban_boards (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS kanban_tasks (
            id TEXT PRIMARY KEY,
            board_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            column TEXT NOT NULL DEFAULT 'todo',
            position INTEGER NOT NULL DEFAULT 0,
            priority TEXT NOT NULL DEFAULT 'medium',
            created_at TEXT NOT NULL,
            FOREIGN KEY (board_id) REFERENCES kanban_boards(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_kanban_tasks_board
            ON kanban_tasks(board_id);
    """)
    conn.commit()


_init_db()


def create_board(name: str) -> dict:
    import uuid
    conn = _get_conn()
    board_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO kanban_boards (id, name, created_at) VALUES (?, ?, ?)",
        (board_id, name, now),
    )
    conn.commit()
    return get_board(board_id)


def get_board(board_id: str) -> Optional[dict]:
    conn = _get_conn()
    row = conn.execute(
        "SELECT * FROM kanban_boards WHERE id = ?", (board_id,)
    ).fetchone()
    if not row:
        return None
    board = dict(row)
    tasks = conn.execute(
        "SELECT * FROM kanban_tasks WHERE board_id = ? ORDER BY position",
        (board_id,),
    ).fetchall()
    board["tasks"] = [dict(t) for t in tasks]
    return board


def list_boards() -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM kanban_boards ORDER BY created_at DESC"
    ).fetchall()
    return [dict(r) for r in rows]


def delete_board(board_id: str) -> bool:
    conn = _get_conn()
    conn.execute("DELETE FROM kanban_tasks WHERE board_id = ?", (board_id,))
    cur = conn.execute("DELETE FROM kanban_boards WHERE id = ?", (board_id,))
    conn.commit()
    return cur.rowcount > 0


def add_task(
    board_id: str,
    title: str,
    description: str = "",
    column: str = "todo",
    priority: str = "medium",
    position: Optional[int] = None,
) -> dict:
    import uuid
    conn = _get_conn()
    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    if position is None:
        max_pos = conn.execute(
            "SELECT COALESCE(MAX(position), -1) FROM kanban_tasks WHERE board_id = ? AND column = ?",
            (board_id, column),
        ).fetchone()[0]
        position = max_pos + 1
    conn.execute(
        """INSERT INTO kanban_tasks (id, board_id, title, description, column, position, priority, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (task_id, board_id, title, description, column, position, priority, now),
    )
    conn.commit()
    return dict(conn.execute("SELECT * FROM kanban_tasks WHERE id = ?", (task_id,)).fetchone())


def update_task(task_id: str, **kwargs) -> Optional[dict]:
    conn = _get_conn()
    allowed = {"title", "description", "column", "position", "priority"}
    updates = {k: v for k, v in kwargs.items() if k in allowed}
    if not updates:
        return get_task(task_id)
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    vals = list(updates.values()) + [task_id]
    conn.execute(f"UPDATE kanban_tasks SET {set_clause} WHERE id = ?", vals)
    conn.commit()
    return get_task(task_id)


def get_task(task_id: str) -> Optional[dict]:
    conn = _get_conn()
    row = conn.execute(
        "SELECT * FROM kanban_tasks WHERE id = ?", (task_id,)
    ).fetchone()
    return dict(row) if row else None


def delete_task(task_id: str) -> bool:
    conn = _get_conn()
    cur = conn.execute("DELETE FROM kanban_tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cur.rowcount > 0


def add_tasks_bulk(board_id: str, tasks: list[dict]) -> list[dict]:
    created = []
    for task in tasks:
        created.append(add_task(board_id, **task))
    return created
