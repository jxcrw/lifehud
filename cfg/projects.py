#!/usr/bin/env python3
"""Project definitions"""

from cfg.config import SMART_TODAY, WEEKMASK_ALL, WEEKMASK_ANY, WEEKMASK_SIX
from lib.project import Project


PROJECTS = [
    Project('mind', 'hours', 6.9, 7.9, 25, False, WEEKMASK_ALL, SMART_TODAY),
    Project('body', 'hours', 0.1, 0.1, 20, True, WEEKMASK_SIX, SMART_TODAY),
    Project('pool', 'hours', 0.9, 1.9, 00, True, WEEKMASK_ALL, SMART_TODAY),
    Project('lang', 'hours', 0.1, 0.1, 00, False, WEEKMASK_ALL, SMART_TODAY),
    Project('work', 'hours', 1.0, 3.0, 00, True, WEEKMASK_ALL, SMART_TODAY),
    Project('meet', 'hours', 0.1, 0.1, 00, True, WEEKMASK_ANY, SMART_TODAY),
]
PROJECTS = {p.name: p for p in PROJECTS}