#!/usr/bin/env python3
"""A life project"""

from datetime import datetime, timedelta

from colorama import Back
from pandas import read_csv

from _cfg.config import *
from utils import underline


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
                 today: date,
                 ):
        self.name = name
        self.metric = metric
        self.std_lo = std_lo
        self.std_hi = std_hi
        self.delayed_start = delayed_start
        self.autoopen = autoopen
        self.weekmask = weekmask
        self.today = today
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
            start = rows.iloc[0]['start']
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


    def is_wip(self) -> bool:
        """Get whether the project has a WIP entry."""
        latest = self.data.iloc[0][self.metric]
        return latest == WIP


    def build_dot(self, day: date) -> str:
        """Build a pretty contribution dot for the given day."""
        dot, score = DOT_STD, self.score_day(day)
        if day == self.today:
            if self.is_wip(): dot = DOT_WIP
            dot = underline(dot) if score != SCORE_ZERO else Back.BLACK + dot
        fore = SCORE2FORE[score]
        return fore + dot + Back.RESET


    def render_week(self, day: date) -> str:
        """Create a mini contribution graph for the week containing the given day."""
        days_since_sunday = (day.weekday() + 1) % 7
        sunday = day - timedelta(days=days_since_sunday)
        name = [Fore.WHITE + self.name]
        dots = [self.build_dot(sunday + timedelta(days=i)) for i in range(7)]
        week = ' '.join(name + dots)
        return week
