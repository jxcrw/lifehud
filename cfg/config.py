#!/usr/bin/env python3
"""Settings"""

from collections import defaultdict
from datetime import date, time
import os
from pathlib import Path
import sys

from colorama import Fore


# Pathing
DIR_HOME = Path.home()
DIR_ROOT = Path(sys.path[1])
DIR_DATA = DIR_ROOT / '_arc/data'
DIR_SYNC = DIR_HOME / 'Dropbox/lifehud'
DIR_SCOOP = Path(os.getenv('SCOOP'))
DIR_DATA = DIR_SYNC  # TODO


# Contributions and scoring
SCORE_GOOD = 1
SCORE_OKAY = 0.5
SCORE_BAD = 0.25
SCORE_ZERO = 0


# Data formatting
SEP = '\t'
WIP = -1
WIP_TIME = time(hour=0, minute=0)
FMT_TIME = '%H:%M'
FMT_FLOAT = '%.2f'
CONVERTERS = {
    'date': date.fromisoformat,
    'start': time.fromisoformat,
    'end': time.fromisoformat,
    'hours': float,
    'cals': int,
    'note': str,
    'revs': int,
}
FORMATTERS = {
    'date': str,
    'start': lambda x: x.strftime(FMT_TIME),
    'end': lambda x: x.strftime(FMT_TIME),
    'hours': lambda x: f'{x:0.2f}',
    'cals': str,
    'note': str,
    'revs': str,
}

EDITOR = 'subl.exe'
ROWCOL = ':2:28'


# Special date stuff
def load_data(path: str) -> dict:
    """Load project data up into a dict of labeled, typed objects."""
    data = defaultdict(list)
    with open(path, 'r', encoding='utf-8') as f:
        raw = [line.strip().split(SEP) for line in f]
        headers, entries = raw[0], raw[1:]
    for entry in entries:
        key = CONVERTERS[headers[0]](entry[0])
        val = {headers[i]: CONVERTERS[headers[i]](entry[i]) for i in range(len(entry))}
        data[key].append(val)
    return data


def get_latest_entry(data: dict) -> dict:
    """Get the latest entry in a project dataset."""
    latest = list(data.values())[0][0]
    return latest


def get_oldest_entry(data: dict) -> dict:
    """Get the oldest entry in a project dataset."""
    oldest = list(data.values())[-1][0]
    return oldest


SMART_TODAY_OWNER = 'mind'
SMART_TODAY_DATA = load_data(DIR_SYNC / f'{SMART_TODAY_OWNER}.tsv')
SMART_TODAY = get_latest_entry(SMART_TODAY_DATA)['date']
SMART_DOY = int(SMART_TODAY.strftime('%j'))
SMART_WOY = int(SMART_TODAY.strftime('%U'))

WEEKMASK_ANY = set()
WEEKMASK_ALL = {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'}
WEEKMASK_SIX = {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'}


# TUI
SCORE2FORE = {
    SCORE_GOOD: Fore.GREEN,
    SCORE_OKAY: Fore.YELLOW,
    SCORE_BAD: Fore.RED,
    SCORE_ZERO: Fore.LIGHTBLACK_EX,
}

DOT_STD = '⯀'  # Alt: ●
DOT_WIP = 'w'


# Toast styling
COLOR_FG = 'c0caf5'
COLOR_BG = '1a1b26'
COLOR_GREEN = '9ece6a'
COLOR_YELLOW = 'f7b273'
COLOR_RED = 'f7768e'

SCORE2COLOR = {
    SCORE_GOOD: COLOR_GREEN,
    SCORE_OKAY: COLOR_YELLOW,
    SCORE_BAD: COLOR_RED,
    SCORE_ZERO: COLOR_RED,
}
