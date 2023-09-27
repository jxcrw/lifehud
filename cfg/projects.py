#!/usr/bin/env python3
"""Project definitions"""

from cfg.config import SMART_TODAY, WEEKMASK_ALL, WEEKMASK_ANY, WEEKMASK_SIX
from lib.project import Project
from lib.wrappers import Standard as Std


PROJECTS = [
    Project('mind', 'hours', Std(6.9, 7.9), 25, False, WEEKMASK_ALL, SMART_TODAY),
    Project('body', 'hours', Std(0.9, 1.5), 20, True, WEEKMASK_SIX, SMART_TODAY),
    Project('pool', 'hours', Std(0.9, 1.9), 00, True, WEEKMASK_ALL, SMART_TODAY),
    Project('lang', 'hours', Std(0.2, 0.4), 00, False, WEEKMASK_ALL, SMART_TODAY),
    Project('work', 'hours', Std(2.0, 4.0), 00, True, WEEKMASK_ALL, SMART_TODAY),
    Project('meet', 'hours', Std(0.1, 1.0), 00, True, WEEKMASK_ANY, SMART_TODAY),
]
PROJECTS = {p.name: p for p in PROJECTS}


PROJECTS_DAILY_ORDER = ['mind', 'lang', 'work', 'pool', 'body', 'meet']
PROJECTS_DAILY_ORDER = {name: PROJECTS[name] for name in PROJECTS_DAILY_ORDER}
