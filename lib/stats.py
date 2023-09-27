#!/usr/bin/env python3
"""Pretty project stats"""

from dataclasses import dataclass

from colorama import Fore

from cfg.config import SMART_TODAY, SMART_WOY
from lib.wrappers import Chain, Period, Standard


@dataclass
class Stats:
    """Pretty stats for a life project."""
    def __init__(self,
                 period: Period,
                 standard: Standard,
                 weekmask: set[str],
                 n_hours: float,
                 n_days: int,
                 chain: Chain,
                 years: set[int],
                 ):
        self.period = period
        self.standard = standard
        self.weekmask = weekmask
        self.n_hours = n_hours
        self.n_days = n_days
        self.chain = chain
        self.years = years

        # Determine theoretic maxes
        n_years = len(years)
        n_weeks_curr = SMART_WOY if period.end.year == SMART_TODAY.year else 52
        n_weeks_past = (n_years - 1) * 52
        n_weeks = n_weeks_curr + n_weeks_past

        n_days_max = n_weeks * len(weekmask)
        n_days_max = n_days_max if n_days_max else n_days
        n_hours_max = n_days_max * standard.hi

        self.n_hours_max = n_hours_max
        self.n_days_max = n_days_max


    def format_cumulatively(self) -> tuple[str]:
        """Format stats for cumulative display."""
        hours = Fore.BLACK + f'hour: {self.n_hours:0.0f} ({self.n_hours / self.n_hours_max:.0%})'
        days = Fore.BLACK + f'days: {self.n_days} ({self.n_days / self.n_days_max:.0%})'
        chain = Fore.BLACK + f'chæn: {self.pretty_chain()}'
        years = Fore.BLACK + f'year: {len(self.years)}'
        return hours, days, chain, years


    def format_yearly(self) -> None:
        """Format stats for yearly display."""
        hours, days, _, _ = self.format_cumulatively()
        stats = '   '.join([hours, days])
        return stats


    def format_weekly(self) -> None:
        """Format stats for weekly display."""
        stats = Fore.BLACK + f'  {self.n_hours:0.0f}h  ({self.pretty_chain()})'
        return stats


    def pretty_chain(self) -> str:
        """Format chain stats."""
        if self.chain.curr == self.chain.max:
            chain = f'{self.chain.curr}!'
        else:
            chain = f'{self.chain.curr}/{self.chain.max}'
        return chain
