#!/usr/bin/env python3
"""A life project"""

from datetime import date

from pandas import read_csv

from _cfg.config import CONVERTERS, DIR_SYNC, SCORE_BAD, SCORE_GOOD, SCORE_OKAY, SCORE_ZERO


class Project:
    """A life project."""

    def __init__(self,
                 name: str,
                 metric: str,
                 std_lo: float,
                 std_hi: float,
                 delayed_start: int,
                 autoopen: bool,
                 weekmask: str,
                 ):
        self.name = name
        self.metric = metric
        self.std_lo = std_lo
        self.std_hi = std_hi
        self.delayed_start = delayed_start
        self.autoopen = autoopen
        self.weekmask = weekmask
        self.data = read_csv(DIR_SYNC / f'{name}.tsv', sep='\t', converters=CONVERTERS)

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
