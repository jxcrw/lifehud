#!/usr/bin/env python3
"""Track sleep data"""

from collections import deque
from datetime import datetime, timedelta
import sys

import pyperclip

PATH = r'C:\~\dev\lifehud'
sys.path.append(PATH)

from lifehud import DIR_SYNC


# Setup
FILE = DIR_SYNC / 'mind.txt'


# Load data
with open(FILE, 'r', encoding='utf-8') as f:
    data = deque([line.strip().split('\t') for line in f])


# Act
now = datetime.now()
latest = data[0]
is_new = latest[2] != 'wip'

if is_new:
    start = now + timedelta(minutes=30)
    date = now.strftime('%Y-%m-%d')
    start = start.strftime('%H:%M')
    hours = end = 'wip'
    sesh = [date, start, end, hours]
    data.appendleft(sesh)
    message = 'sleep_9ece6a'
else:
    start = datetime.strptime(latest[0] + latest[1], '%Y-%m-%d%H:%M')
    duration = (now - start).seconds / 3600
    latest[3] = f'{duration:0.2f}'
    latest[2] = now.strftime('%H:%M')
    message = f'sleep ({latest[3]}h)_f7768e'


# Write data
with open(FILE, 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(['\t'.join(entry) for entry in data]))
pyperclip.copy(message)
print(message)
