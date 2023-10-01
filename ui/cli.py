#!/usr/bin/env python3
"""Lifehud"""

from datetime import date, timedelta

import click

from cfg.config import FORE_INFO
from cfg.projdefs import PROJECTS, PROJECTS_DAILY_ORDER
from cfg.today import SMART_TODAY
from lib.wrappers import ClickGroupInlineOrder


@click.group(cls=ClickGroupInlineOrder)
def cli():
    """Visualize progress on life projects in the form of contribution graphs."""
    pass


@cli.command()
@click.option('--num', '-n', default=1, help="How many weeks to render (starting from current week).")
@click.option('--stats', '-s', is_flag=True, default=False, help="Show cumulative stats.")
@click.option('--optl', '-o', is_flag=True, default=False, help="Show optional projects.")
@click.option('--life_order', '-l', is_flag=True, default=False, help="Show projects in life order.")
def week(num, stats, optl, life_order):
    """Render a weekly lifehud."""
    weekhuds, projs = [], PROJECTS_DAILY_ORDER
    if life_order:
        projs = PROJECTS
    if not optl:
        projs = {k: p for k, p in projs.items() if p.required}

    for i in range(num):
        day = SMART_TODAY - timedelta(days=i*7)
        graphs = '\n'.join([p.render_week(day, show_stats=stats) for p in projs.values()])
        weekhud = f'{FORE_INFO}Week {day:%U}\n{graphs}'
        weekhuds.append(weekhud)
    print('\n\n'.join(weekhuds))


@cli.command()
@click.option('--stats', '-s', is_flag=True, default=False, help="Show cumulative stats.")
def year(stats):
    """Render a yearly lifehud."""
    year = SMART_TODAY.year
    graphs = [p.render_year(year, show_stats=stats) for p in PROJECTS.values()]
    yearhud = '\n\n'.join(graphs)
    print(yearhud)


@cli.command()
@click.argument('name', nargs=1)
@click.option('--stats', '-s', is_flag=True, default=False, help="Show cumulative stats.")
def project(name, stats):
    """Render all data for the specified project."""
    p = PROJECTS[name]
    projhud = p.render_project(show_stats=stats)
    print(projhud)


@cli.command()
@click.argument('name', nargs=1)
def track(name):
    """Start/stop time tracking for the specified project."""
    p = PROJECTS[name]
    p.track()


if __name__ == '__main__':
    # command(['--my_arg', '42'])
    print()
    cli()
