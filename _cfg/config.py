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


# Projects
@dataclass
class Project:
    """A life project."""
    name: str
    metric: str
    std_lo: float
    std_hi: float
    delayed_start: int = 0
    autoopen: bool = False
    weekmask: str = 'Sun Mon Tue Wed Thu Fri Sat'
    data: DataFrame = None

    def load_data(self):
        """Load up the project's data."""
        path = DIR_SYNC / f'{self.name}.tsv'
        self.data = pd.read_csv(path, sep='\t', converters=CONVERTERS)


PROJECTS = [Project('0', 'hours', 1, 1, 20, True, 'Sun Mon Tue Wed Thu Fri')]
PROJECTS = {p.name: p for p in PROJECTS}
[p.load_data() for p in PROJECTS.values()]


