#!/usr/bin/env python3
"""Unit tests"""

from datetime import date

from cfg.config import WEEKMASK_SIX
from lib.project import Project
from lib.wrappers import Standard as Std


p = Project('test', Std(0.9, 1.5), 0, False, WEEKMASK_SIX)
week = p.render_week(date(2023, 9, 28), show_stats=True)
year = p.render_year(2023, show_stats=True)
print()
print(week)
print(year)
