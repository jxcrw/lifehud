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
SCORE_GOOD = 1
SCORE_OKAY = 0.5
SCORE_BAD = 0.25
SCORE_ZERO = 0


# Data formatting
SEP = '\t'
WIP = 0.00
WIP_TIME = time(hour=0, minute=0)
FMT_TIME = '%H:%M'
FMT_FLOAT = '%.2f'
CONVERTERS = {
    'date': date.fromisoformat,
    'start': time.fromisoformat,
    'end': time.fromisoformat,
}

EDITOR = 'subl.exe'
ROWCOL = ':2:28'


# Special date stuff
SMART_TODAY_OWNER = 'mind'
mind_data = read_csv(DIR_SYNC / f'{SMART_TODAY_OWNER}.tsv', sep='\t', converters=CONVERTERS)
SMART_TODAY = mind_data.iloc[0]['date']
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
