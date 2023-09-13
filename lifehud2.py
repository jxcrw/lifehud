#!/usr/bin/env python3
"""LifeHUD2"""

from datetime import date

from _cfg.config import SMART_TODAY
from project import Project


if __name__ == '__main__':
    # ┌─────────────────────────────────────────────────────────────────────────────
    # │ Setup
    # └─────────────────────────────────────────────────────────────────────────────
    # Determine smart today
    mind = Project('0', 'hours', 6.9, 7.9, 25, False, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY)

    # Initialize other projects
    PROJECTS = [
        mind,
        # Project('0', 'hours', 6.9, 7.9, 25, False, 'Sun Mon Tue Wed Thu Fri Sat', date.today()),
        # Project('0', 'hours', 6.9, 7.9, 25, False, 'Sun Mon Tue Wed Thu Fri Sat', date.today()),
    ]
    PROJECTS = {p.name: p for p in PROJECTS}
