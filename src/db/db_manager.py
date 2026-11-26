import os
import sqlite3
from pathlib import Path

# Create %LOCALAPPDATA%\EngInventory\ and required subfolders
APP_DIR = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData/Local")) / "EngInventory"
for sub in ("images", "thumbnails", "backups", "logs"):
    (APP_DIR / sub).mkdir(parents=True, exist_ok=True)

DB_PATH = APP_DIR / "inventory.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS items (
    item_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
	manufacturer TEXT NOT NULL DEFAULT '',
	model TEXT NOT NULL DEFAULT '',
	serial_no TEXT,
    quantity_total INTEGER NOT NULL CHECK (quantity_total >= 0),
    quantity_available INTEGER NOT NULL CHECK (quantity_available >= 0),
    location TEXT NOT NULL DEFAULT '',
    condition TEXT NOT NULL DEFAULT 'Good',
    image_path TEXT,
    thumbnail_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
	
	CHECK (quantity_available <= quantity_total)
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL,
    borrower_name TEXT NOT NULL,
    borrower_contact TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    borrowed_at TEXT NOT NULL,
    due_at TEXT NOT NULL,
    returned_at TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    FOREIGN KEY (item_id) REFERENCES items (item_id)
);

CREATE TABLE IF NOT EXISTS waitlist (
    entry_id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL,
    requester_name TEXT NOT NULL,
    requester_contact TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 1,
    requested_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'waiting',
    FOREIGN KEY (item_id) REFERENCES items (item_id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'staff',
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    details TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_items_name ON items (name);
CREATE INDEX IF NOT EXISTS idx_loans_status_due ON loans (status, due_at);
CREATE INDEX IF NOT EXISTS idx_waitlist_item_status ON waitlist (item_id, status);
CREATE INDEX IF NOT EXISTS idx_items_category ON items (category);

PRAGMA table_info(items);
"""

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Automatically build the database and tables when this file is run or imported
with get_connection() as conn:
    conn.executescript(SCHEMA)