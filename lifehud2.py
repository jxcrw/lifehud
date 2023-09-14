#!/usr/bin/env python3
"""LifeHUD2"""

from datetime import date, timedelta

import click

from _cfg.config import SMART_TODAY
from project import Project


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Init
# └─────────────────────────────────────────────────────────────────────────────
PROJECTS = [
    Project('0', 'hours', 6.9, 7.9, 25, True, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
    Project('0', 'hours', 6.9, 7.9, 25, True, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
]


# ┌─────────────────────────────────────────────────────────────────────────────
# │ CLI
# └─────────────────────────────────────────────────────────────────────────────
@click.group()
def cli():
    pass


if __name__ == '__main__':
    # command()
    print()
    cli()
