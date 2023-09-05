#!/usr/bin/env python3
"""Get sleep data from Sleep as Android"""

import csv
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

from lifehud import DIR_DATA


# Setup
FILE_IN = Path(r'C:\Users\jak\Dropbox\Apps\Sleep Cloud Backup\Sleep as Android Data.zip')
DIR_OUT = FILE_IN.parent


# Extract data
with ZipFile(FILE_IN) as zip_file:
    zip_file.extractall(DIR_OUT)


# Parse/format data
path = DIR_OUT / 'sleep-export.csv'
with open(path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    raw = [_ for _ in csv_reader if _['Id'] != 'Id']  # Strip silly duplicate header rows

data = []
for entry in raw:
    entry['From'] = datetime.strptime(entry['From'], '%d. %m. %Y %H:%M')
    entry['To'] = datetime.strptime(entry['To'], '%d. %m. %Y %H:%M')

    date = entry['To'].strftime('%Y-%m-%d')
    start = entry['From'].strftime('%H:%M')
    stop = entry['To'].strftime('%H:%M')
    hours = entry['Hours']
    data.append([date, hours, start, stop])


# Write data
path = DIR_DATA / 'mind.txt'
with open(path, 'w+', newline='\n', encoding='utf-8') as f:
    f.writelines('\n'.join(['\t'.join(entry) for entry in data]))

