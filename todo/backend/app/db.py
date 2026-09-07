from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[1] / "data" / "todo.db"


@contextmanager
def connect(database_path: Path | str = DEFAULT_DATABASE_PATH) -> Iterator[sqlite3.Connection]:
    """Open a short-lived SQLite connection and commit or roll back its work."""

    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db(database_path: Path | str = DEFAULT_DATABASE_PATH) -> None:
    """Create the database schema if it does not exist yet."""

    with connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL
                    CHECK (length(trim(text)) BETWEEN 1 AND 200),
                done INTEGER NOT NULL DEFAULT 0
                    CHECK (done IN (0, 1))
            )
            """
        )
