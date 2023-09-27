#!/usr/bin/env python3
"""Get study data from Anki database"""

import os
from pathlib import Path
import shutil
import sqlite3

from cfg.config import DIR_DATA, DIR_SCOOP, DIR_SYNC, FMTR_FLOAT


# Setup
FILE = DIR_SYNC / 'lang.tsv'
FILE_ORIG = DIR_SCOOP / 'persist/anki/data/Jak/collection.anki2'
FILE_WORK = Path(DIR_DATA / 'collection.anki2')
shutil.copy(FILE_ORIG, FILE_WORK)


# Extract data
query = """
SELECT
    DATE(STRFTIME('%s', DATETIME(((id/1000)+strftime('%s', '1970-01-01')), 'unixepoch', 'localtime')), 'unixepoch') AS "date",
    COUNT(*) as "reviews",
    SUM(time) as "time_ms"
FROM revlog
GROUP BY date
ORDER BY date
"""

con = sqlite3.connect(FILE_WORK)
cur = con.cursor()
raw = cur.execute(query).fetchall()
con.close()


# Parse/format data
data = [['date', 'hours', 'revs']]
for entry in reversed(raw):
    date = entry[0]
    revs = entry[1]
    hours = entry[2] / 1000 / 3600
    data.append([date, FMTR_FLOAT(hours), str(revs)])


# Write data
with open(FILE, 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(['\t'.join(_) for _ in data]))


# Clean up
os.remove(FILE_WORK)
