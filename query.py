#!/usr/bin/env python3
"""查询 lexicon.db"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description='查询阿拉伯语词典')
    ap.add_argument('word', help='阿拉伯语单词')
    ap.add_argument('--db', default='lexicon.db')
    ap.add_argument('--contains', action='store_true', help='模糊搜索')
    args = ap.parse_args()

    db = Path(args.db)
    if not db.exists():
        sys.exit(f'[ERROR] 找不到数据库: {db}，请先运行 python3 import_tsv.py lexicon.tsv')

    con = sqlite3.connect(db)
    if args.contains:
        rows = con.execute(
            'SELECT word, pos, meanings, examples FROM entries WHERE word LIKE ? ORDER BY word',
            (f'%{args.word}%',)
        ).fetchall()
    else:
        rows = con.execute(
            'SELECT word, pos, meanings, examples FROM entries WHERE word=?',
            (args.word,)
        ).fetchall()

    if not rows:
        print(f'未找到：{args.word}')
        sys.exit(1)

    for word, pos, meanings, examples in rows:
        print(f'{word}  [{pos}]')
        print('释义：' + '；'.join(json.loads(meanings)))
        for ex in json.loads(examples):
            print(f'  {ex["ar"]}')
            print(f'  → {ex["en"]}')
    con.close()

if __name__ == '__main__':
    main()
