#!/usr/bin/env python3
"""Settings"""

from datetime import date, time
import os
from pathlib import Path
import sys

from colorama import Fore
from pandas import read_csv


# Pathing
DIR_HOME = Path.home()
DIR_ROOT = Path(sys.path[1])
DIR_DATA = DIR_ROOT / '_arc/data'
DIR_SYNC = DIR_HOME / 'Dropbox/lifehud'
DIR_SCOOP = Path(os.getenv('SCOOP'))
DIR_DATA = DIR_SYNC  # TODO


# Contributions and scoring
WIP = 'wip'
SCORE_GOOD = 1
SCORE_OKAY = 0.5
SCORE_BAD = 0.25
SCORE_ZERO = 0


# Data formatting
def convert_hours_wip_aware(val: str) -> str | float:
    """Perform WIP-aware conversion of an hours value."""
    output = val if val == WIP else float(val)
    return output

CONVERTERS = {
    'date': date.fromisoformat,
    'hours': convert_hours_wip_aware,
    'start': time.fromisoformat,
    'end': time.fromisoformat,
}

SEP = '\t'
FMT_FLOAT = '%.2f'
FMT_TIME = '%H:%M'

EDITOR = 'subl.exe'
ROWCOL = ':2:28'


# Smart today
mind_data = read_csv(DIR_SYNC / f'0.tsv', sep='\t', converters=CONVERTERS)
SMART_TODAY = mind_data.iloc[0]['date']


# TUI
SCORE2FORE = {
    SCORE_GOOD: Fore.GREEN,
    SCORE_OKAY: Fore.YELLOW,
    SCORE_BAD: Fore.RED,
    SCORE_ZERO: Fore.LIGHTBLACK_EX,
}

DOT_STD = '⯀'  # Alt: ●
DOT_WIP = 'w'
