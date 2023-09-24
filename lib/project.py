#!/usr/bin/env python3
"""A life project"""

from datetime import datetime, timedelta
import subprocess

from colorama import Back, Style

from cfg.config import *
from lib.utils import toast, underline


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
        self.required = len(weekmask) > 0
        self.path = DIR_SYNC / f'{name}.tsv'
        self.data = load_data(self.path)


    def is_wip(self) -> bool:
        """Get whether the project has a WIP entry."""
        latest = get_latest_entry(self.data)[self.metric]
        return latest == WIP


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
            chain_stats = self.get_chain_stats()
            _, _, total = self.get_cumulative_stats((sunday, day))
            stats = Fore.BLACK + f'  {total:0.0f}{self.metric[0]}  ({chain_stats})'
            dots[-1] += stats
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
            period = (soy, end)
            stats = self.get_cumulative_stats(period)
            val_stat, day_stat, _, _ = self.format_cumulative_stats(period, stats)
            stats = '   '.join([day_stat, val_stat])
            dots_by_dow.append([stats])

            # Cumulative stats for all time
            period = (get_oldest_entry(self.data)['date'], end)
            stats = self.get_cumulative_stats(period)
            stats = self.format_cumulative_stats(period, stats)
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


    def format_cumulative_stats(self, period: tuple[date, date], stats: tuple[int, float, int]) -> tuple:
        """Format cumulative stats into pretty strings."""
        # Unpack args
        start, end = period
        years, n_days, total = stats
        n_years = len(years)

        # Determine theoretic maxes and chains
        n_weeks_curr = SMART_WOY if end.year == SMART_TODAY.year else 52
        n_weeks_past = (n_years - 1) * 52
        n_weeks = n_weeks_curr + n_weeks_past

        n_days_max = n_weeks * len(self.weekmask)
        n_days_max = n_days_max if n_days_max else n_days
        val_max = n_days_max * self.std_hi
        chain = self.get_chain_stats()

        # Put it all together
        val_stat = Fore.BLACK + f'hour: {total:0.0f} ({total/val_max:.0%})'
        day_stat = Fore.BLACK + f'days: {n_days} ({n_days / n_days_max:.0%})'
        chain_stat = Fore.BLACK + f'chæn: {chain}'
        year_stat = Fore.BLACK + f'year: {n_years}'
        return val_stat, day_stat, chain_stat, year_stat


    def get_chain_stats(self) -> str:
        """Get current and max chain stats for the project."""
        chain_curr = self.get_chain_current()
        chain_max = self.get_chain_max()
        if chain_curr == chain_max:
            stats = f'{chain_curr}!'
        else:
            stats = f'{chain_curr}/{chain_max}'
        return stats


    def get_chain_current(self) -> int:
        """Get the chain of successful days starting from the current day."""
        chain, day, oldest_day = 0, SMART_TODAY, get_oldest_entry(self.data)['date']
        score = self.score_day(day)
        while score >= SCORE_OKAY and day >= oldest_day:
            day -= timedelta(days=1)
            score = self.score_day(day)
            if score == SCORE_ZERO and f'{day:%a}' not in self.weekmask:
                score = SCORE_OKAY
                continue
            chain += 1
        return chain


    def get_chain_max(self) -> int:
        """Get the maximum chain of successful days ever recorded for the project."""
        chain = chain_max = 0
        day = get_oldest_entry(self.data)['date']
        while day <= SMART_TODAY:
            score = self.score_day(day)
            if score == SCORE_ZERO and f'{day:%a}' not in self.weekmask:
                day += timedelta(days=1)
                continue
            elif score >= SCORE_OKAY:
                chain += 1
            else:
                chain_max = max(chain_max, chain)
                chain = 0
            day += timedelta(days=1)
        chain_max = max(chain_max, chain)
        return chain_max


    def get_cumulative_stats(self, period: tuple[date, date]) -> tuple[int, float, int]:
        """Get the cumulative number of days and total value for the given time period."""
        years, n_days, total = set(), 0, 0
        start, end = period

        day = start
        while day <= end:
            val = self.get_day_val(day)
            n_days += 1 if val else 0
            total += val
            years.add(day.year)
            day += timedelta(days=1)

        return years, n_days, total


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
