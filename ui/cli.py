#!/usr/bin/env python3
"""Lifehud"""

from datetime import date, timedelta

import click

from cfg.config import FORE_INFO
from cfg.projdefs import PROJECTS, PROJECTS_DAILY_ORDER
from cfg.today import SMART_TODAY
from lib.wrappers import ClickGroupInlineOrder, RenderOpts


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
    opts = RenderOpts(show_stats=stats)

    for i in range(num):
        day = SMART_TODAY - timedelta(days=i*7)
        graphs = '\n'.join([p.render_week(day, opts) for p in projs.values()])
        weekhud = f'{FORE_INFO}Week {day:%U}\n{graphs}'
        weekhuds.append(weekhud)
    print('\n\n'.join(weekhuds))


@cli.command()
@click.option('--stats', '-s', is_flag=True, default=False, help="Show cumulative stats.")
@click.option('--quarters', '-q', is_flag=True, default=False, help="Split year into quarters.")
def year(stats, quarters):
    """Render a yearly lifehud."""
    year = SMART_TODAY.year
    opts = RenderOpts(show_stats=stats, split_quarters=quarters)
    graphs = [p.render_year(year, opts) for p in PROJECTS.values()]
    yearhud = '\n\n'.join(graphs)
    print(yearhud)


@cli.command()
@click.argument('name', nargs=1)
@click.option('--stats', '-s', is_flag=True, default=False, help="Show cumulative stats.")
@click.option('--quarters', '-q', is_flag=True, default=False, help="Split year into quarters.")
def project(name, stats, quarters):
    """Render all data for the specified project."""
    p = PROJECTS[name]
    opts = RenderOpts(show_year=True, show_stats=stats, split_quarters=quarters)
    projhud = p.render_project(opts)
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
