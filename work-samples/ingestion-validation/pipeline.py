"""Synthetic local ingestion demonstration. No employer data or Azure credentials."""
import argparse
import json
import math
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

def ingest(rows, database):
 accepted=0; rejected=[]
 with closing(sqlite3.connect(str(database))) as db, db:
  db.execute('CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY, updated_at TEXT NOT NULL, amount REAL NOT NULL)')
  db.execute('CREATE TABLE IF NOT EXISTS quarantine(payload TEXT PRIMARY KEY, reason TEXT NOT NULL)')
  for row in rows:
   try:
    key=row['id']
    if not isinstance(key,str) or not key.strip(): raise ValueError('nonempty string id required')
    dt=datetime.fromisoformat(row['updated_at'])
    if dt.tzinfo is None: raise ValueError('timezone required')
    stamp=dt.astimezone(timezone.utc).isoformat()
    amount=float(row['amount'])
    if not math.isfinite(amount) or amount<0: raise ValueError('finite nonnegative amount required')
   except (ValueError,TypeError,KeyError) as e:
    payload=json.dumps(row,sort_keys=True);reason=str(e)
    db.execute('INSERT OR REPLACE INTO quarantine VALUES(?,?)',(payload,reason));rejected.append(reason);continue
   cur=db.execute('INSERT INTO records VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET updated_at=excluded.updated_at,amount=excluded.amount WHERE excluded.updated_at>records.updated_at',(key,stamp,amount))
   accepted+=cur.rowcount
  total=db.execute('SELECT COUNT(*) FROM records').fetchone()[0]
 return {'accepted':accepted,'rejected':len(rejected),'total':total}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',default='sample.json');p.add_argument('--database',default='demo.db');a=p.parse_args()
 print(json.dumps(ingest(json.loads(Path(a.input).read_text()),a.database),indent=2))
