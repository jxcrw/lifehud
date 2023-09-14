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


@cli.command()
@click.option('--num', '-n', default=1, help="The number of weeks to render, starting from the current week.")
def week(num):
    """Render the weekly HUD."""
    weekhuds, today = [], date.today()
    for i in range(num):
        day = today - timedelta(days=i * 7)
        weeknum = day.strftime('%U')
        weekhud = [p.render_week(day) for p in PROJECTS]
        weekhud = '\n'.join(weekhud)
        weekhuds.append(f'Week {weeknum}\n{weekhud}')
    print('\n', '\n\n'.join(weekhuds))


@cli.command()
def year():
    """Render the yearly HUD."""
    year = date.today().year
    yearhud = [p.render_year(year) for p in PROJECTS]
    yearhud = '\n\n'.join(yearhud)
    print('\n', yearhud)


if __name__ == '__main__':
    # command()
    cli()
