#!/usr/bin/env python3
"""Pretty project stats"""

from datetime import timedelta

from colorama import Fore

from cfg.config import SCORE_OKAY, SCORE_ZERO
from cfg.today import SMART_TODAY, SMART_WOY
from lib.wrappers import Chain, Period, Standard


class Stats:
    """Pretty stats for a life project."""
    def __init__(self, project: 'Project', period: Period):
        self.project = project
        self.period = period

        self.years = set()
        self.chain = None
        self.n_hours = 0
        self.n_days = 0
        self.n_hours_max = 0
        self.n_days_max = 0

        self.calc_totals()
        self.calc_chain()
        self.determine_maxes()


    def calc_totals(self) -> None:
        """Calculate contribution totals for the given time period."""
        day = self.period.start
        while day <= self.period.end:
            c_val = self.project.get_contribution_val(day)
            self.n_days += 1 if c_val else 0
            self.n_hours += c_val
            self.years.add(day.year)
            day += timedelta(days=1)


    def calc_chain(self) -> Chain:
        """Get the chain of successful days recorded for the specified period."""
        chain = chain_curr = chain_max = 0
        day = self.period.end
        while day >= self.period.start:
            score = self.project.score_day(day)
            is_zero = (score == SCORE_ZERO)
            is_req = f'{day:%a}' in self.project.weekmask
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
        self.chain = chain


    def determine_maxes(self):
        """Determine the theoretic max contributions for the stats' time period."""
        n_years = len(self.years)
        n_weeks_curr = SMART_WOY if self.period.end.year == SMART_TODAY.year else 52
        n_weeks_past = (n_years - 1) * 52
        n_weeks = n_weeks_curr + n_weeks_past

        n_days_max = n_weeks * len(self.project.weekmask)
        n_days_max = n_days_max if n_days_max else self.n_days
        n_hours_max = n_days_max * self.project.standard.hi

        self.n_days_max = n_days_max
        self.n_hours_max = n_hours_max


    def format_cumulatively(self) -> tuple[str]:
        """Format stats for cumulative display."""
        hours = Fore.BLACK + f'hour: {self.n_hours:0.0f} ({self.n_hours / self.n_hours_max:.0%})'
        days = Fore.BLACK + f'days: {self.n_days} ({self.n_days / self.n_days_max:.0%})'
        chain = Fore.BLACK + f'chæn: {self.format_chain()}'
        years = Fore.BLACK + f'year: {len(self.years)}'
        return hours, days, chain, years


    def format_yearly(self) -> None:
        """Format stats for yearly display."""
        hours, days, _, _ = self.format_cumulatively()
        stats = '   '.join([hours, days])
        return stats


    def format_weekly(self) -> None:
        """Format stats for weekly display."""
        stats = Fore.BLACK + f'  {self.n_hours:0.0f}h  ({self.format_chain()})'
        return stats


    def format_chain(self) -> str:
        """Format chain stats."""
        if self.chain.curr == self.chain.max:
            chain = f'{self.chain.curr}!'
        else:
            chain = f'{self.chain.curr}/{self.chain.max}'
        return chain
