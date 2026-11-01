import csv
from pathlib import Path
from arabic_lexicon.db import get_connection, init_db, clear_and_insert

def migrate_tsv_to_sqlite(tsv_path="lexicon.tsv"):
    p = Path(tsv_path)
    if not p.exists():
        print("未找到 lexicon.tsv")
        return

    rows = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split("\t")
            # 对齐字段: arabic, type, meaning, example_ar, example_en, lemma
            while len(parts) < 6:
                parts.append("")
            rows.append(tuple(parts[:6]))

    conn = get_connection()
    init_db(conn)
    clear_and_insert(conn, rows)
    print(f"成功迁移 {len(rows)} 条词条到 SQLite")

if __name__ == "__main__":
    migrate_tsv_to_sqlite()
