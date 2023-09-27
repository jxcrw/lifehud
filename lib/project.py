#!/usr/bin/env python3
"""A life project"""

from datetime import datetime, timedelta
import subprocess

from colorama import Back, Style

from cfg.config import *
from lib.wrappers import Chain, Period, Standard
from lib.stats import Stats
from lib.utils import toast, underline


class Project:
    """A life project."""

    def __init__(self,
                 name: str,
                 metric: str,
                 standard: Standard,
                 delayed_start: int,
                 autoopen: bool,
                 weekmask: str,
                 today: date,
                 ):
        self.name = name
        self.metric = metric
        self.standard = standard
        self.delayed_start = delayed_start
        self.autoopen = autoopen
        self.weekmask = weekmask
        self.today = today
        self.required = len(weekmask) > 0
        self.path = DIR_SYNC / f'{name}.tsv'
        self.data = load_data(self.path)


    def is_wip(self) -> bool:
        """Get whether the project currently has a WIP entry."""
        latest = get_latest_entry(self.data)[self.metric]
        return latest == WIP


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
            period = Period(sunday, day)
            stats = self.calc_stats(period)
            dots[-1] += stats.format_weekly()
        graph = Fore.WHITE + f'{self.name} {" ".join(dots)}'
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
            prd = Period(soy, end)
            stats = self.calc_stats(prd)
            dots_by_dow.append([stats.format_yearly()])

            # Cumulative stats for all time
            prd_all = Period(get_oldest_entry(self.data)['date'], end)
            stats = self.calc_stats(prd_all)
            stats = stats.format_cumulatively()
            for i, stat in enumerate(stats):
                dots_by_dow[i].append(f'  {stat}')

        dots = '\n'.join([' '.join(_) for _ in dots_by_dow])

        # Put everything together
        year_label = f'-{year}' if show_year else ''
        graph = Fore.WHITE + f'{self.name}{year_label}\n{dots}'
        return graph


    def render_project(self, show_stats: bool = False) -> str:
        """Render all project data into yearly contribution graphs."""
        years = sorted(set([date.year for date in self.data.keys()]), reverse=True)
        graphs = [self.render_year(year, show_stats=show_stats, show_year=True) for year in years]
        projhud = '\n\n'.join(graphs)
        return projhud


    def get_day_val(self, day: date) -> float | str:
        """Get a cumulative, WIP-aware value for a day."""
        # Select entries corresponding to day
        data, metric, day_val = self.data, self.metric, 0
        entries = data[day] if day in data else []

        # Add sum of values for done entries
        vals_done = [e[metric] for e in entries if e[metric] != WIP]
        day_val += sum(vals_done)

        # Add value for wip entry (if present)
        entries_wip = [e for e in entries if e[metric] == WIP]
        if len(entries_wip) > 0:
            start = datetime.combine(day, entries_wip[0]['start'])
            now = datetime.now()
            day_val += (now - start).seconds / 3600

        return day_val


    def score_day(self, day: date) -> float:
        """Determine the contribution score for a day based on project's standards."""
        val, std = self.get_day_val(day), self.standard
        if val >= std.hi:
            score = SCORE_GOOD
        elif val >= std.lo:
            score = SCORE_OKAY
        elif val > 0:
            score = SCORE_BAD
        else:
            score = SCORE_ZERO
        return score


    def build_dot(self, day: date) -> str:
        """Build a pretty contribution dot for the specified day."""
        dot, score, day_of_week = DOT_STD, self.score_day(day), f'{day:%a}'
        if day == self.today:
            if self.is_wip():
                dot = DOT_WIP
            if score > SCORE_ZERO:
                dot = underline(dot)
            if score == SCORE_ZERO and day_of_week in self.weekmask:
                dot = Back.BLACK + dot
        fore = SCORE2FORE[score]
        return fore + dot + Style.RESET_ALL


    def calc_stats(self, period: Period) -> Stats:
        """Get comprehensive project stats for the given time period."""
        years, n_days, n_hours = set(), 0, 0
        day = period.start
        while day <= period.end:
            hours = self.get_day_val(day)
            n_days += 1 if hours else 0
            n_hours += hours
            years.add(day.year)
            day += timedelta(days=1)

        chain = self.calc_chain(period)
        stats = Stats(period, self.standard, self.weekmask, n_hours, n_days, chain, years)
        return stats


    def calc_chain(self, period: Period) -> Chain:
        """Get the chain of successful days recorded for the specified period."""
        chain = chain_curr = chain_max = 0
        day = period.end
        while day >= period.start:
            score = self.score_day(day)
            is_zero = (score == SCORE_ZERO)
            is_req = f'{day:%a}' in self.weekmask
            if is_zero and is_req:
                chain_curr = chain
            elif is_zero and not is_req:
                day -= timedelta(days=1)
                continue
            elif score >= SCORE_OKAY:
                chain += 1
            else:
                chain_max = max(chain_max, chain)
                chain = 0
            day -= timedelta(days=1)
        chain = Chain(chain_curr, chain_max)
        return chain


    def track(self) -> None:
        """Start/stop time tracking for the project."""
        metric, data, now = self.metric, self.data, datetime.now()
        latest = get_latest_entry(self.data)
        is_new = latest[metric] != WIP
        if is_new:
            date, hours, end = self.today, WIP, WIP_TIME
            if self.name == SMART_TODAY_OWNER:
                date += timedelta(days=1)
            start = now + timedelta(minutes=self.delayed_start)
            vals = [date, hours, start, end]
            keys = self.get_headers()
            entry = {keys[i]: vals[i] for i in range(len(vals))}
            data[date].insert(0, entry)
            toast(self.name, COLOR_FG)
        else:
            start = datetime.combine(latest['date'], latest['start'])
            hours = (now - start).seconds / 3600
            latest[metric] = hours
            latest['end'] = now
            score = self.score_day(latest['date'])
            color = SCORE2COLOR[score]
            toast(f'{self.name} ({hours:0.2f}h)', color)

        self.save_to_disk()
        if self.autoopen and not is_new:
            subprocess.run([EDITOR, f'{self.path}{ROWCOL}'])


    def save_to_disk(self) -> None:
        """Save the project to disk."""
        self.data = dict(sorted(self.data.items(), reverse=True))
        buffer = [self.get_headers()]
        for day in self.data:
            for entry in self.data[day]:
                vals = [FORMATTERS[key](entry[key]) for key in entry]
                buffer.append(vals)
        with open(self.path, 'w+', newline='\n', encoding='utf-8') as f:
            f.write('\n'.join(['\t'.join(_) for _ in buffer]))


    def get_headers(self) -> list[str]:
        """Get a list of the headers to label a project data entry."""
        headers = list(get_oldest_entry(self.data).keys())
        return headers
