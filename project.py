#!/usr/bin/env python3
"""A life project"""

from datetime import date, datetime

from pandas import read_csv

from _cfg.config import CONVERTERS, DIR_SYNC, SCORE_BAD, SCORE_GOOD, SCORE_OKAY, SCORE_ZERO, WIP


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


    def get_day_val(self, day: date) -> float | str:
        """Get a cumulative, WIP-aware value for a day."""
        # Select rows corresponding to day
        data, metric, day_val = self.data, self.metric, 0
        rows = data.loc[data['date'] == day]

        # Add sum of values for done rows
        rows_done = rows.loc[rows[metric] != WIP]
        day_val += rows_done[metric].sum()

        # Add value for wip row (if present)
        rows_wip = rows.loc[rows[metric] == WIP]
        if len(rows_wip) > 0:
            start = rows_wip.iloc[0]['start']
            start = datetime.combine(day, start)
            now = datetime.now()
            day_val += (now - start).seconds / 3600

        return day_val


    def score_day(self, day: date) -> float:
        """Determine the contribution score for a day based on project's standards."""
        val, std_lo, std_hi = self.get_day_val(day), self.std_lo, self.std_hi
        if val >= std_hi:
            score = SCORE_GOOD
        elif val >= std_lo:
            score = SCORE_OKAY
        elif val > 0:
            score = SCORE_BAD
        else:
            score = SCORE_ZERO
        return score
