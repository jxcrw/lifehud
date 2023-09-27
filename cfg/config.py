#!/usr/bin/env python3
"""Settings"""

from datetime import date, time
import os
from pathlib import Path
import sys

from colorama import Fore

from lib.wrappers import DataHandler as Dh


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Pathing
# └─────────────────────────────────────────────────────────────────────────────
DIR_HOME = Path.home()
DIR_ROOT = Path(sys.path[1])
DIR_DATA = DIR_ROOT / '_arc/data'
DIR_SYNC = DIR_HOME / 'Dropbox/lifehud'
DIR_SCOOP = Path(os.getenv('SCOOP'))
DIR_DATA = DIR_SYNC  # TODO


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Data Handling
# └─────────────────────────────────────────────────────────────────────────────
SEP = '\t'
METRIC = 'hours'

WIP_VAL = -1
WIP_TIME = time(hour=0, minute=0)

FMTR_TIME = lambda x: x.isoformat('minutes')
FMTR_FLOAT = lambda x: format(x, '0.2f')

HANDLERS = {
    'date': Dh(date.fromisoformat, date.isoformat),
    'start': Dh(time.fromisoformat, FMTR_TIME),
    'end': Dh(time.fromisoformat, FMTR_TIME),
    'hours': Dh(float, FMTR_FLOAT),
    'cals': Dh(int, str),
    'revs': Dh(int, str),
    'note': Dh(str, str),
}


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Project Scoring
# └─────────────────────────────────────────────────────────────────────────────
SCORE_GOOD = 1
SCORE_OKAY = 0.5
SCORE_BAD = 0.25
SCORE_ZERO = 0

WEEKMASK_ANY = set()
WEEKMASK_ALL = {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'}
WEEKMASK_SIX = {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'}


# ┌─────────────────────────────────────────────────────────────────────────────
# │ UI
# └─────────────────────────────────────────────────────────────────────────────
# TUI
DOT_STD = '⯀'  # Alt: ●
DOT_WIP = 'w'

SCORE2FORE = {
    SCORE_GOOD: Fore.GREEN,
    SCORE_OKAY: Fore.YELLOW,
    SCORE_BAD: Fore.RED,
    SCORE_ZERO: Fore.LIGHTBLACK_EX,
}

# Toasts
FONT = 'Consolas'
FONT_SIZE = 12
DURATION_MS = 3000
HEX_FG = 'c0caf5'
HEX_BG = '1a1b26'
HEX_GREEN = '9ece6a'
HEX_YELLOW = 'f7b273'
HEX_RED = 'f7768e'

SCORE2HEX = {
    SCORE_GOOD: HEX_GREEN,
    SCORE_OKAY: HEX_YELLOW,
    SCORE_BAD: HEX_RED,
    SCORE_ZERO: HEX_RED,
}


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Text Editor
# └─────────────────────────────────────────────────────────────────────────────
EDITOR = 'subl.exe'
ROWCOL = ':2:28'
