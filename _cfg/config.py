#!/usr/bin/env python3
"""Settings"""

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


# Contribution scoring
SCORE_GOOD = 1
SCORE_OKAY = 0.5
SCORE_BAD = 0.25
SCORE_ZERO = 0


# TUI
SCORE2FORE = {
    SCORE_GOOD: Fore.GREEN,
    SCORE_OKAY: Fore.YELLOW,
    SCORE_BAD: Fore.RED,
    SCORE_ZERO: Fore.LIGHTBLACK_EX,
}

DOT_STD = '⯀'  # Alt: ●
DOT_WIP = 'w'


# Misc
WIP = 'wip'
