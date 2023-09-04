#!/usr/bin/env python3
"""Get review stats from anki"""

import csv
import os
import sqlite3

username = os.environ.get('USERNAME')
db_path = r"C:\scoop\persist\anki\data\Jak\collection.anki2"
con = sqlite3.connect(db_path)
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

result = c.execute(query).fetchall()

with open('data/lang.txt', 'w+', newline='\n', encoding='utf-8') as f:
    data = []
    for row in result:
        date = row[0]
        reviews = row[1]
        entry = '\t'.join([date, str(reviews)])
        data.append(entry)

    f.write('\n'.join(data))

# with open("daily_stats.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Date", "Reviews", "Time (milliseconds)", "Time (seconds)", "Time (hours)"])
#     for row in result:
#         date = row[0]
#         reviews = row[1]
#         time_ms = row[2]
#         time_sec = time_ms / 1000
#         time_hours = time_sec / 3600
#         writer.writerow([date, reviews, time_ms, time_sec, time_hours])
#
# print("CSV file written successfully.")
