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
    Project('mynd', 'hours', 6.9, 7.9, 25, True, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
    Project('bodi', 'hours', 6.9, 7.9, 00, True, 'Sun Mon Tue Wed Thu Fri Sat', SMART_TODAY),
]
PROJECTS = {p.name: p for p in PROJECTS}


# ┌─────────────────────────────────────────────────────────────────────────────
# │ CLI
# └─────────────────────────────────────────────────────────────────────────────
@click.group()
def cli(): pass


@cli.command()
@click.option('--num', '-n', default=1, help="The number of weeks to render, starting from the current week.")
def week(num):
    """Render the weekly HUD."""
    weekhuds, today = [], date.today()
    for i in range(num):
        day = today - timedelta(days=i * 7)
        weeknum = day.strftime('%U')
        weekhud = [f'{p.name} {p.render_week(day)}' for p in PROJECTS.values()]
        weekhud = '\n'.join(weekhud)
        weekhuds.append(f'Week {weeknum}\n{weekhud}')
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
