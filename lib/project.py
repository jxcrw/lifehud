#!/usr/bin/env python3
"""A life project"""

from collections import defaultdict
from datetime import datetime, timedelta

from colorama import Back, Style

from cfg.config import *
from cfg.today import SMART_TODAY, SMART_TODAY_OWNER
from lib.stats import Stats
from lib.utils import autoopen, toast, underline
from lib.wrappers import Period, Standard


class Project:
    """A life project."""

    def __init__(self,
                 name: str,
                 standard: Standard,
                 delayed_start: int,
                 autoopen: bool,
                 weekmask: str,
                 ):
        self.name = name
        self.standard = standard
        self.delayed_start = delayed_start
        self.autoopen = autoopen
        self.weekmask = weekmask
        self.required = len(weekmask) > 0
        self.path = DIR_SYNC / f'{name}.tsv'
        self.data = self.read_data()


    def render_week(self, day: date, show_stats: bool = False) -> str:
        """Render contribution graph for the week containing the specified day."""
        dots = []
        days_since_sunday = (day.weekday() + 1) % 7
        sunday = day - timedelta(days=days_since_sunday)
        for i in range(7):
            day = sunday + timedelta(days=i)
            dot = self.build_dot(day)
            dots.append(dot)
        if show_stats:
            period = Period(sunday, SMART_TODAY)
            stats = Stats(self, period)
            dots[-1] += stats.format_weekly()
        graph = FORE_FG + f'{self.name} {" ".join(dots)}'
        return graph


    def render_year(self, year: int, show_stats: bool = False, show_year: bool = False) -> str:
        """Render contribution graph for the specified year."""
        # Build dict(weeknum → dict(daynum → date))
        soy = date(year, 1, 1)
        eoy = date(year, 12, 31)
        day, weeknums = soy, defaultdict(dict)
        while day <= eoy:
            weeknum = int(day.strftime('%U'))
            daynum = int(day.strftime('%w'))
            weeknums[weeknum][daynum] = day
            day += timedelta(days=1)

        # Build info for each day of each week
        dots_by_week = []
        for daynums in weeknums.values():
            dots = []
            for daynum in range(7):
                dot = self.build_dot(daynums[daynum]) if daynum in daynums else ' '
                dots.append(dot)
            dots_by_week.append(dots)

        # Regroup dots by day of week + add stats
        dots_by_dow = [list(_) for _ in zip(*dots_by_week)]
        if show_stats:
            end = SMART_TODAY if year == SMART_TODAY.year else eoy

            # Stats for current year
            period = Period(soy, end)
            stats = Stats(self, period)
            dots_by_dow.append([stats.format_yearly()])

            # Cumulative stats for all time
            period_all = Period(self.get_oldest_entry()['date'], end)
            stats = Stats(self, period_all)
            stats = stats.format_cumulatively()
            for i, stat in enumerate(stats):
                dots_by_dow[i].append(f'  {stat}')

        dots = '\n'.join([' '.join(_) for _ in dots_by_dow])

        # Put everything together
        year_label = f'-{year}' if show_year else ''
        graph = FORE_FG + f'{self.name}{year_label}\n{dots}'
        return graph


    def render_project(self, show_stats: bool = False) -> str:
        """Render all project data as yearly contribution graphs."""
        years = sorted(set([date.year for date in self.data.keys()]), reverse=True)
        graphs = [self.render_year(year, show_stats=show_stats, show_year=True) for year in years]
        projhud = '\n\n'.join(graphs)
        return projhud


    def build_dot(self, day: date) -> str:
        """Build a pretty contribution dot for the specified day."""
        dot, score = DOT_STD, self.score_day(day)
        is_req_day = self.is_req_day(day)
        if day == SMART_TODAY:
            if self.is_wip():
                dot = DOT_WIP
            if score > SCORE_ZERO:
                dot = underline(dot)
            if score == SCORE_ZERO and is_req_day:
                dot = Back.BLACK + dot
        fore = score.fore
        dot = fore + dot + Style.RESET_ALL
        return dot


    def score_day(self, day: date) -> Score:
        """Determine the contribution score for a day based on project's standards."""
        val, std = self.get_contribution_val(day), self.standard
        if val >= std.hi:
            score = SCORE_GOOD
        elif val >= std.lo:
            score = SCORE_OKAY
        elif val > 0:
            score = SCORE_BAD
        else:
            score = SCORE_ZERO
        return score


    def get_contribution_val(self, day: date) -> float | str:
        """Get a cumulative, WIP-aware contribution value for the specified day."""
        val = 0
        entries = self.data[day] if day in self.data else []
        for e in entries:
            is_done = e[METRIC] != WIP_VAL
            if is_done:
                val += e[METRIC]
            else:
                start = datetime.combine(day, e['start'])
                now = datetime.combine(SMART_TODAY, datetime.now().time())
                is_wip_valid = now > start
                if is_wip_valid:
                    val += (now - start).seconds / 3600
        return val


    def is_req_day(self, day: date) -> bool:
        """Determine whether the specified day is a required day for the project."""
        is_req = f'{day:%w}' in self.weekmask
        return is_req


    def track(self) -> None:
        """Start/stop time tracking for the project."""
        # Update project data
        now, day = datetime.now(), SMART_TODAY
        newest = self.get_newest_entry()
        is_new = newest[METRIC] != WIP_VAL
        if is_new:
            hours, end = WIP_VAL, WIP_TIME
            if self.name == SMART_TODAY_OWNER:
                day += timedelta(days=1)
            start = now + timedelta(minutes=self.delayed_start)
            vals = [day, hours, start.time(), end]
            keys = self.get_headers()
            entry = {keys[i]: vals[i] for i in range(len(vals))}
            self.data[day].insert(0, entry)
        else:
            start = datetime.combine(newest['date'], newest['start'])
            hours = (now - start).seconds / 3600
            newest[METRIC] = hours
            newest['end'] = now

        # Issue toast
        val = self.get_contribution_val(day)
        icon = ICON_PLAY if is_new else ICON_STOP
        message = f'{icon} {self.name} - {FMTR_FLOAT(val)}h'
        hex_color = self.score_day(day).hex_color
        toast(message, hex_color)

        # Write data to disk
        self.write_data()
        if self.autoopen and not is_new:
            autoopen(self.path)


    def read_data(self) -> dict:
        """Load project data up into a dict of labeled, typed objects."""
        data = defaultdict(list)
        with open(self.path, 'r', encoding='utf-8') as f:
            raw = [line.strip().split(SEP) for line in f]
            headers, entries = raw[0], raw[1:]
        for entry in entries:
            key = HANDLERS[headers[0]].converter(entry[0])
            val = {headers[i]: HANDLERS[headers[i]].converter(entry[i]) for i in range(len(entry))}
            data[key].append(val)
        return data


    def write_data(self) -> None:
        """Write project data to disk with sensible string formatting."""
        self.data = dict(sorted(self.data.items(), reverse=True))
        buffer = [self.get_headers()]
        for day in self.data:
            for entry in self.data[day]:
                vals = [HANDLERS[key].formatter(entry[key]) for key in entry]
                buffer.append(vals)
        with open(self.path, 'w+', newline='\n', encoding='utf-8') as f:
            f.write('\n'.join(['\t'.join(_) for _ in buffer]))


    def get_headers(self) -> list[str]:
        """Get a list of the headers to label a project data entry."""
        headers = list(self.get_oldest_entry().keys())
        return headers


    def is_wip(self) -> bool:
        """Get whether the project currently has a WIP entry."""
        newest_val = self.get_newest_entry()[METRIC]
        return newest_val == WIP_VAL


    def get_period_all(self) -> Period:
        """Get a period from the oldest entry through smart today."""
        period = Period(self.get_oldest_entry()['date'], SMART_TODAY)
        return period


    def get_newest_entry(self) -> dict:
        """Get the newest entry in a project dataset."""
        latest = list(self.data.values())[0][0]
        return latest


    def get_oldest_entry(self) -> dict:
        """Get the oldest entry in a project dataset."""
        oldest = list(self.data.values())[-1][0]
        return oldest
