#!/usr/bin/env python3
"""Project definitions"""

from cfg.config import WEEKMASK_ALL, WEEKMASK_ANY, WEEKMASK_SIX
from lib.project import Project
from lib.wrappers import Standard as Std


# Project definitions, in order of life importance
PROJECTS = [
    Project('mind', Std(6.9, 7.9), 25, False, WEEKMASK_ALL),
    Project('body', Std(0.9, 1.5), 20, True, WEEKMASK_SIX),
    Project('pool', Std(2.0, 3.5), 00, False, WEEKMASK_ALL),
    Project('lang', Std(0.2, 0.4), 00, False, WEEKMASK_ALL),
    Project('work', Std(2.0, 4.0), 00, False, WEEKMASK_ALL),
    Project('meet', Std(0.1, 1.0), 00, True, WEEKMASK_ANY),
]
PROJECTS = {p.name: p for p in PROJECTS}


# Project definitions, in order of daily completion
PROJECTS_DAILY_ORDER = ['mind', 'lang', 'work', 'pool', 'body', 'meet']
PROJECTS_DAILY_ORDER = {name: PROJECTS[name] for name in PROJECTS_DAILY_ORDER}
