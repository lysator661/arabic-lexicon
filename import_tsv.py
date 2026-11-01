#!/usr/bin/env python3
"""lexicon.tsv -> lexicon.db + arabic_lexicon/data.json"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

def clean(text):
    return text.strip()

def split_meanings(raw):
    if not raw:
        return []
    parts = [p.strip() for p in raw.replace('؛', ';').split(';') if p.strip()]
    if not parts:
        parts = [raw.strip()]
    return dedupe(parts)

def dedupe(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tsv', nargs='?', default='lexicon.tsv')
    ap.add_argument('--db', default='lexicon.db')
    ap.add_argument('--json', default='arabic_lexicon/data.json')
    args = ap.parse_args()

    tsv_path = Path(args.tsv)
    if not tsv_path.exists():
        sys.exit(f'[ERROR] 找不到 TSV 文件: {tsv_path}')

    entries = {}
    with tsv_path.open(encoding='utf-8') as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) < 3:
                print(f'[WARN] 第 {lineno} 行字段不足，跳过: {line}')
                continue
            word = clean(parts[0])
            if not word:
                continue
            pos = clean(parts[1])
            entry = entries.setdefault(word, {'pos': pos, 'meanings': [], 'examples': []})
            if pos:
                entry['pos'] = pos
            entry['meanings'].extend(split_meanings(parts[2]))
            if len(parts) >= 5 and (clean(parts[3]) or clean(parts[4])):
                entry['examples'].append({'ar': clean(parts[3]), 'en': clean(parts[4])})

    # 词义、例句去重保序
    for entry in entries.values():
        entry['meanings'] = dedupe(entry['meanings'])
        seen_examples = set()
        unique_examples = []
        for ex in entry['examples']:
            key = (ex['ar'], ex['en'])
            if key not in seen_examples:
                seen_examples.add(key)
                unique_examples.append(ex)
        entry['examples'] = unique_examples

    # 写入 SQLite
    con = sqlite3.connect(args.db)
    con.execute('CREATE TABLE IF NOT EXISTS entries (word TEXT PRIMARY KEY, pos TEXT, meanings TEXT, examples TEXT)')
    rows = [
        (word, e['pos'],
         json.dumps(e['meanings'], ensure_ascii=False),
         json.dumps(e['examples'], ensure_ascii=False))
        for word, e in entries.items()
    ]
    con.executemany('INSERT OR REPLACE INTO entries(word, pos, meanings, examples) VALUES (?, ?, ?, ?)', rows)
    con.commit()
    con.close()

    # 覆盖 GUI 读取的 data.json
    data = {
        word: {
            'pos': e['pos'],
            'meanings': e['meanings'],
            'examples': e['examples'],
        }
        for word, e in entries.items()
    }
    out = Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'[OK] 导入 {len(entries)} 个词条')
    print(f'     SQLite 词库: {args.db}')
    print(f'     GUI 数据:    {out}')

if __name__ == '__main__':
    main()
