import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".local" / "share" / "arabic-lexicon" / "lexicon.db"

def get_connection(db_path=None):
    db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    # 注意：WAL 模式在 virtiofs 等共享文件系统中会因共享内存(-shm)报错
    # 故使用 DELETE 模式保证跨环境兼容性
    conn.execute("PRAGMA journal_mode=DELETE")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            arabic TEXT NOT NULL,
            type TEXT,
            meaning TEXT,
            example_ar TEXT,
            example_en TEXT,
            lemma TEXT
        );
    """)
    conn.commit()

def get_all_entries(conn):
    return conn.execute("SELECT * FROM entries ORDER BY id").fetchall()

def clear_and_insert(conn, rows):
    """rows: list of (arabic, type, meaning, example_ar, example_en, lemma)"""
    conn.execute("DELETE FROM entries")
    conn.executemany("""
        INSERT INTO entries (arabic, type, meaning, example_ar, example_en, lemma)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
