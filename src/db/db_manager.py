import logging
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# 1. App-data & DB paths
APP_DIR = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData/Local")) / "EngInventory"
DB_PATH = APP_DIR / "inventory.db"
LOG_PATH = APP_DIR / "logs" / "app.log"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def ensure_app_dirs() -> Path:
    """Create %LOCALAPPDATA%\\EngInventory\\ and required subfolders."""
    for sub in ("images", "thumbnails", "backups", "logs"):
        (APP_DIR / sub).mkdir(parents=True, exist_ok=True)
    return APP_DIR


def _get_file_logger(log_path: Path = LOG_PATH) -> logging.Logger:
    logger = logging.getLogger(f"eng_inventory.audit.{log_path}")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(handler)
    return logger


# 2. Opening a connection & creating tables
def get_connection(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    ensure_app_dirs()
    if str(db_path) != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(
    db_path: str | Path = DB_PATH,
    schema_path: str | Path = SCHEMA_PATH,
) -> None:
    sql_script = Path(schema_path).read_text(encoding="utf-8")
    with get_connection(db_path) as conn:
        conn.executescript(sql_script)


# 3. Simple query/write helpers
def fetch_one(
    query: str,
    params: tuple[Any, ...] = (),
    db_path: str | Path = DB_PATH,
    conn: Optional[sqlite3.Connection] = None,
) -> Optional[dict[str, Any]]:
    if conn is not None:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None
    with get_connection(db_path) as own_conn:
        row = own_conn.execute(query, params).fetchone()
        return dict(row) if row else None


def fetch_all(
    query: str,
    params: tuple[Any, ...] = (),
    db_path: str | Path = DB_PATH,
    conn: Optional[sqlite3.Connection] = None,
) -> list[dict[str, Any]]:
    if conn is not None:
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    with get_connection(db_path) as own_conn:
        rows = own_conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]


def execute(
    query: str,
    params: tuple[Any, ...] = (),
    db_path: str | Path = DB_PATH,
    conn: Optional[sqlite3.Connection] = None,
) -> int:
    """Run an INSERT, UPDATE, or DELETE and return affected rows (rowcount)."""
    if conn is not None:
        cur = conn.execute(query, params)
        return int(cur.rowcount)
    with get_connection(db_path) as own_conn:
        cur = own_conn.execute(query, params)
        return int(cur.rowcount)


# 4. Audit logging helper
def record_audit(
    actor: str,
    action: str,
    details: str,
    conn: Optional[sqlite3.Connection] = None,
    db_path: str | Path = DB_PATH,
    log_path: str | Path = LOG_PATH,
) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()

    def _insert(c: sqlite3.Connection) -> None:
        c.execute(
            """
            INSERT INTO audit_log (timestamp, actor, action, details)
            VALUES (?, ?, ?, ?)
            """,
            (timestamp, actor, action, details),
        )

    if conn is not None:
        _insert(conn)
    else:
        with get_connection(db_path) as own_conn:
            _insert(own_conn)

    _get_file_logger(Path(log_path)).info("%s | %s | %s", actor, action, details)