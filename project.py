#!/usr/bin/env python3
"""A life project"""

from dataclasses import dataclass
from datetime import date

from pandas import DataFrame, read_csv

from _cfg.config import CONVERTERS, DIR_SYNC, SCORE_BAD, SCORE_GOOD, SCORE_OKAY, SCORE_ZERO


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

    def score_day(self, day: date) -> float:
        """Determine the contribution score for a day based on project's standards."""
        data, std_lo, std_hi = self.data, self.std_lo, self.std_hi
        values = data.loc[data['date'] == day][self.metric]
        total = values.sum()

        if total >= std_hi:
            score = SCORE_GOOD
        elif total >= std_lo:
            score = SCORE_OKAY
        elif total > 0:
            score = SCORE_BAD
        else:
            score = SCORE_ZERO

        return score
