#!/usr/bin/env python3
"""Smart today initialization"""

from datetime import date

from cfg.config import DIR_SYNC, SEP


SMART_TODAY_OWNER = 'mind'


with open(f'{DIR_SYNC / SMART_TODAY_OWNER}.tsv', 'r', encoding='utf-8') as f:
    raw = [line.strip().split(SEP) for line in f]

SMART_TODAY = date.fromisoformat(raw[1][0])
SMART_WOY = int(SMART_TODAY.strftime('%U'))
