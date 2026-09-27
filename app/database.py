import sqlite3
from pathlib import Path
from typing import Any, List, Optional
from app.config import DATABASE_PATH, DATABASE_DIR


def get_connection() -> sqlite3.Connection:
    """Create a connection to the SQLite database with row factory enabled."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_database_exists() -> None:
    """Ensure database file exists and is populated."""
    if not DATABASE_PATH.exists():
        from scripts.init_db import init_database
        init_database(DATABASE_PATH)


def query_all(query: str, params: tuple = ()) -> List[dict]:
    """Execute a query and return all matching rows as dictionaries."""
    ensure_database_exists()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def query_one(query: str, params: tuple = ()) -> Optional[dict]:
    """Execute a query and return a single matching row as a dictionary."""
    ensure_database_exists()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None


def execute(query: str, params: tuple = ()) -> int:
    """Execute an INSERT/UPDATE/DELETE query and return the last row ID."""
    ensure_database_exists()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
