#!/usr/bin/env python3
"""Settings"""

from datetime import date, time
import os
from pathlib import Path
import sys

from colorama import Fore

from lib.wrappers import DataHandler as Dh, Score


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Pathing
# └─────────────────────────────────────────────────────────────────────────────
DIR_HOME = Path.home()
DIR_ROOT = DIR_HOME / 'dev/lifehud'
DIR_SYNC = DIR_HOME / 'Dropbox/lifehud'
DIR_SCOOP = Path(os.getenv('SCOOP'))
DIR_ARCHIVE = DIR_ROOT / '_arc/data'

ENABLE_ARCHIVING = True


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Data Handling
# └─────────────────────────────────────────────────────────────────────────────
SEP = '\t'
METRIC = 'hours'

WIP_VAL = -1
WIP_TIME = time(hour=0, minute=0)

FMT_NUM = '0.0f'
FMT_PCT = '.0%'
FMTR_TIME = lambda x: format(x, '%H:%M')
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
# │ UI
# └─────────────────────────────────────────────────────────────────────────────
# TUI
DOT_STD = '⯀'  # Alt: ●
DOT_WIP = 'w'
FORE_FG = Fore.WHITE
FORE_GOOD = Fore.GREEN
FORE_OKAY = Fore.YELLOW
FORE_BAD = Fore.RED
FORE_ZERO = Fore.LIGHTBLACK_EX
FORE_INFO = Fore.BLACK

# Toasts
FONT = 'Consolas'
FONT_SIZE = 12
DURATION_MS = 3000
HEX_FG = 'c0caf5'
HEX_BG = '1a1b26'
HEX_GREEN = '9ece6a'
HEX_YELLOW = 'f7b273'
HEX_RED = 'f7768e'
HEX_CMT = '565f89'
ICON_PLAY = '▶'
ICON_STOP = '◼'


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Project Scoring
# └─────────────────────────────────────────────────────────────────────────────
SCORE_GOOD = Score(1, FORE_GOOD, HEX_GREEN)
SCORE_OKAY = Score(0.5, FORE_OKAY, HEX_YELLOW)
SCORE_BAD = Score(0.25, FORE_BAD, HEX_RED)
SCORE_ZERO = Score(0, FORE_ZERO, HEX_FG)

WEEKMASK_ANY = set()
WEEKMASK_ALL = {'0', '1', '2', '3', '4', '5', '6'}  # Where 0 is Sunday, 6 is Saturday
WEEKMASK_SIX = {'0', '1', '2', '3', '4', '5'}


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Text Editor
# └─────────────────────────────────────────────────────────────────────────────
EDITOR = 'subl.exe'
ROWCOL = ':2:28'
