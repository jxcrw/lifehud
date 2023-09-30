#!/usr/bin/env python3
"""Pretty project stats"""

from datetime import timedelta

from cfg.config import FMT_NUM, FMT_PCT, FORE_INFO, SCORE_OKAY
from cfg.today import SMART_TODAY, SMART_WOY
from lib.wrappers import Chain, Period


class Stats:
    """Pretty stats for a life project."""
    def __init__(self, project: 'Project', period: Period):
        self.project = project
        self.period = period

        # Totals
        self.years = set()
        self.n_days = 0
        self.n_hours = 0
        self.calc_totals()

        # Theoretic maxes
        self.n_hours_max = 0
        self.n_days_max = 0
        self.calc_theoretic_maxes()

        # Chains
        self.chain = self.calc_chain(period)
        self.chain_all = self.calc_chain(project.get_period_all())


    def calc_totals(self) -> None:
        """Calculate contribution totals for the stats period."""
        day = self.period.start
        while day <= self.period.end:
            val = self.project.get_contribution_val(day)
            self.n_days += 1 if val else 0
            self.n_hours += val
            self.years.add(day.year)
            day += timedelta(days=1)


    def calc_theoretic_maxes(self):
        """Calculate the theoretic max contributions for the stats period."""
        n_years = len(self.years)
        n_weeks_curr = SMART_WOY if self.period.end.year == SMART_TODAY.year else 52
        n_weeks_past = (n_years - 1) * 52
        n_weeks = n_weeks_curr + n_weeks_past

        n_days_max = n_weeks * len(self.project.weekmask)
        n_days_max = n_days_max if n_days_max else self.n_days
        n_hours_max = n_days_max * self.project.standard.hi

        self.n_days_max = n_days_max
        self.n_hours_max = n_hours_max


    def calc_chain(self, period: Period) -> Chain:
        """Calculate the current/max chain of successful days recorded for the stats period."""
        chain_temp = chain_max = 0
        chain_active, is_active = 0, True

        day = period.end
        while day >= period.start:
            score = self.project.score_day(day)
            is_score_ok = score >= SCORE_OKAY
            is_req_day = self.project.is_req_day(day)

            if not is_score_ok and not is_req_day:
                day -= timedelta(days=1)
                continue
            elif is_score_ok:
                chain_temp += 1
                chain_max = max(chain_max, chain_temp)
                if is_active:
                    chain_active += 1
            else:
                chain_temp = 0
                is_active = False
            day -= timedelta(days=1)

        chain = Chain(chain_active, chain_max)
        return chain


    def format_cumulatively(self) -> tuple[str]:
        """Format stats for cumulative display."""
        hours = FORE_INFO + f'hour: {self.n_hours:{FMT_NUM}} ({self.n_hours / self.n_hours_max:{FMT_PCT}})'
        days = FORE_INFO + f'days: {self.n_days} ({self.n_days / self.n_days_max:{FMT_PCT}})'
        chain = FORE_INFO + f'chæn: {self.format_chain(self.chain)}'
        years = FORE_INFO + f'year: {len(self.years)}'
        return hours, days, chain, years


    def format_yearly(self) -> None:
        """Format stats for yearly display."""
        hours, days, chain, _ = self.format_cumulatively()
        stats = '   '.join([hours, days, chain])
        return stats


    def format_weekly(self) -> None:
        """Format stats for weekly display."""
        stats = FORE_INFO + f'  {self.n_hours:{FMT_NUM}}h  ({self.format_chain(self.chain_all)})'
        return stats


    def format_chain(self, chain: Chain) -> str:
        """Format chain stats."""
        if chain.active == chain.max:
            chain = f'{chain.active}!'
        else:
            chain = f'{chain.active}/{chain.max}'
        return chain
