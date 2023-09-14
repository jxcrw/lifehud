#!/usr/bin/env python3
"""A life project"""

from collections import defaultdict
from datetime import datetime, timedelta
import subprocess

from colorama import Back

from _cfg.config import *
from utils import toast, underline


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
        self.path = DIR_SYNC / f'{name}.tsv'
        self.data = read_csv(self.path, sep=SEP, converters=CONVERTERS)


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
            start = datetime.combine(day, rows_wip.iloc[0]['start'])
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
        return fore + dot + Fore.RESET + Back.RESET


    def render_week(self, day: date) -> str:
        """Create a mini contribution graph for the week containing the given day."""
        days_since_sunday = (day.weekday() + 1) % 7
        sunday = day - timedelta(days=days_since_sunday)
        dots = [self.build_dot(sunday + timedelta(days=i)) for i in range(7)]
        week = ' '.join([self.name] + dots)
        return week


    def render_year(self, year: int) -> str:
        """Create a full contribution graph for the given year."""
        # Build dict(weeknum → dict(daynum → date))
        soy = date(year, 1, 1)
        eoy = date(year, 12, 31)
        day, weeknums = soy, defaultdict(dict)
        while day <= eoy:
            weeknum = int(day.strftime('%U'))
            daynum = int(day.strftime('%w'))
            weeknums[weeknum][daynum] = day
            day += timedelta(days=1)

        # Build dots for each day of each week
        weekdots = []
        for daynums in weeknums.values():
            daydots = []
            for daynum in range(7):
                daydot = self.build_dot(daynums[daynum]) if daynum in daynums else ' '
                daydots.append(daydot)
            weekdots.append(daydots)

        # Regroup weekdots by day of week
        daysof = [dayof for dayof in zip(*weekdots)]
        dots = '\n'.join([' '.join(dayof) for dayof in daysof])
        year = f'{self.name}\n{dots}'
        return year


    def track(self) -> None:
        """Start/stop time tracking for the project."""
        metric, data, now = self.metric, self.data, datetime.now()
        latest = data.iloc[0]
        is_new = latest[metric] != WIP
        if is_new:
            date, hours, end = self.today, WIP, WIP_TIME
            start = now + timedelta(minutes=self.delayed_start)
            row = [date, hours, start, end]
            data.loc[-1] = row
            data.index = data.index + 1
            data.sort_index(inplace=True)
            toast(self.name, COLOR_FG)
        else:
            start = datetime.combine(latest['date'], latest['start'])
            hours = (now - start).seconds / 3600
            data.loc[0, metric] = hours
            data.loc[0, 'end'] = now
            score = self.score_day(latest['date'])
            color = SCORE2COLOR[score]
            toast(f'{self.name} ({hours:0.2f}h)', color)

        self.save_to_disk()
        if self.autoopen and not is_new:
            subprocess.run([EDITOR, f'{self.path}{ROWCOL}'])


    def save_to_disk(self) -> None:
        """Save the project to disk."""
        data, path = self.data, self.path
        format_times = lambda x: x.strftime(FMT_TIME)
        data['start'] = data['start'].apply(format_times)
        data['end'] = data['end'].apply(format_times)
        data.to_csv(path, sep=SEP, index=False, float_format=FMT_FLOAT)

