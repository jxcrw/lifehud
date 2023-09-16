#!/usr/bin/env python3
"""LifeHUD2"""

from datetime import date, timedelta

import click
from colorama import Fore

from _cfg.config import SMART_TODAY
from project import Project


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Init
# └─────────────────────────────────────────────────────────────────────────────
PROJECTS = [
    Project('mind', 'hours', 6.9, 7.9, 25, False, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
    Project('body', 'hours', 1.0, 1.0, 20, True, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
    Project('pool', 'hours', 0.9, 1.9, 00, True, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
    Project('lang', 'revs',  10,   40, 00, False, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
    Project('work', 'hours', 1.0, 3.0, 00, True, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
]
PROJECTS = {p.name: p for p in PROJECTS}


# ┌─────────────────────────────────────────────────────────────────────────────
# │ CLI
# └─────────────────────────────────────────────────────────────────────────────
@click.group()
def cli(): pass


@cli.command()
@click.option('--num', '-n', default=1, help="The number of weeks to render, starting from the current week.")
@click.option('--stats', '-s', is_flag=True, default=False, help="Show cumulative stats for week.")
def week(num, stats):
    """Render the weekly HUD."""
    weekhuds, today = [], date.today()
    for i in range(num):
        day = today - timedelta(days=i * 7)
        weeknum = day.strftime('%U')
        weekhud = [f'{p.name} {p.render_week(day, stats)}' for p in PROJECTS.values()]
        weekhud = '\n'.join(weekhud)
        weekhuds.append(f'{Fore.BLACK}Week {weeknum}{Fore.RESET}\n{weekhud}')
    print('\n\n'.join(weekhuds))


@cli.command()
def year():
    """Render the yearly HUD."""
    year = date.today().year
    yearhud = [f'{p.name}\n{p.render_year(year)}' for p in PROJECTS.values()]
    yearhud = '\n\n'.join(yearhud)
    print(yearhud)


@cli.command()
@click.argument('name', nargs=1)
def project(name):
    """Render all data for the given project (by year)."""
    proj = PROJECTS[name]
    all_years = proj.render_all_years()
    print(all_years)


@cli.command()
@click.argument('name', nargs=1)
def track(name):
    """Start/stop time tracking for the specified project."""
    proj = PROJECTS[name]
    proj.track()


if __name__ == '__main__':
    # command()
    print()
    cli()
