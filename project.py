#!/usr/bin/env python3
"""A life project"""

from dataclasses import dataclass

from pandas import DataFrame, read_csv

from _cfg.config import CONVERTERS, DIR_SYNC


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
        self.data = read_csv(path, sep='\t', converters=CONVERTERS)
