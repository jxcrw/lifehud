#!/usr/bin/env python3
"""Settings"""

from dataclasses import dataclass
from datetime import date
import os
from pathlib import Path
import sys

from pandas import DataFrame
import pandas as pd


# Pathing
DIR_HOME = Path.home()
DIR_ROOT = Path(sys.path[1])
DIR_DATA = DIR_ROOT / '_arc/data'
DIR_SYNC = DIR_HOME / 'Dropbox/lifehud'
DIR_SCOOP = Path(os.getenv('SCOOP'))
DIR_DATA = DIR_SYNC  # TODO


# Data formatting
CONVERTERS = {
    'date': date.fromisoformat
}
