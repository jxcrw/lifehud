#!/usr/bin/env python3
"""Get study data from Anki"""

from pathlib import Path
import sqlite3

from lifehud import DIR_DATA


# Setup
FILE_IN = Path(r'C:\scoop\persist\anki\data\Jak\collection.anki2')


# Extract data
con = sqlite3.connect(FILE_IN)
c = con.cursor()

query = """
SELECT
    DATE(STRFTIME('%s', DATETIME(((id/1000)+strftime('%s', '1970-01-01')), 'unixepoch', 'localtime')), 'unixepoch') AS "date",
    COUNT(*) as "reviews",
    SUM(time) as "time_ms"
FROM revlog
GROUP BY date
ORDER BY date
"""

raw = c.execute(query).fetchall()


# Parse/format data
data = []
for entry in reversed(raw):
    date = entry[0]
    revs = entry[1]
    hours = entry[2] / 1000 / 3600
    data.append([date, str(revs), f'{hours:0.2f}'])


# Write data
path = DIR_DATA / 'lang.txt'
with open(path, 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(['\t'.join(entry) for entry in data]))
