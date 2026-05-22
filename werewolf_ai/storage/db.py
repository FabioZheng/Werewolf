from __future__ import annotations
import sqlite3
from pathlib import Path


def init_db(db_path: str):
    conn = sqlite3.connect(db_path)
    schema = Path(__file__).with_name("schema.sql").read_text()
    conn.executescript(schema)
    conn.commit()
    return conn
