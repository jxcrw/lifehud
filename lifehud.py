#!/usr/bin/env python3
"""LifeHUD2"""

from datetime import date, timedelta

import click
from colorama import Fore

from _cfg.config import SMART_TODAY, WEEKMASK_ALL, WEEKMASK_ANY, WEEKMASK_SIX
from project import Project


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Init
# └─────────────────────────────────────────────────────────────────────────────
PROJECTS = [
    Project('mind', 'hours', 6.9, 7.9, 25, False, WEEKMASK_ALL, SMART_TODAY),
    Project('body', 'hours', 0.1, 0.1, 20, True, WEEKMASK_SIX, SMART_TODAY),
    Project('pool', 'hours', 0.9, 1.9, 00, True, WEEKMASK_ALL, SMART_TODAY),
    Project('lang', 'hours', 0.1, 0.1, 00, False, WEEKMASK_ALL, SMART_TODAY),
    Project('work', 'hours', 1.0, 3.0, 00, True, WEEKMASK_ALL, SMART_TODAY),
    Project('meet', 'hours', 0.1, 0.1, 00, True, WEEKMASK_ANY, SMART_TODAY),
]
PROJECTS = {p.name: p for p in PROJECTS}


# ┌─────────────────────────────────────────────────────────────────────────────
# │ CLI
# └─────────────────────────────────────────────────────────────────────────────
class GroupInlineOrder(click.Group):
    """Keep commands in the order they are defined in code in the help page."""
    def list_commands(self, ctx):
        return self.commands.keys()

@click.group(cls=GroupInlineOrder)
def cli(): pass


@cli.command()
@click.option('--num', '-n', default=2, help="The number of weeks to render, starting from the current week.")
@click.option('--stats', '-s', is_flag=True, default=False, help="Show cumulative stats for week.")
@click.option('--opt', '-o', is_flag=True, default=False, help="Show optional projects too.")
def week(num, stats, opt):
    """Render the weekly HUD."""
    weekhuds, today, projects = [], date.today(), PROJECTS
    if not opt:
        projects = {k: v for k, v in PROJECTS.items() if v.required}
    for i in range(num):
        day = today - timedelta(days=i * 7)
        graphs = [p.render_week(day, stats) for p in projects.values()]
        weekhud = '\n'.join(graphs)
        weeknum = day.strftime('%U')
        weekhuds.append(f'{Fore.BLACK}Week {weeknum}\n{weekhud}')
    print('\n\n'.join(weekhuds))


@cli.command()
def year():
    """Render the yearly HUD."""
    year = date.today().year
    graphs = [p.render_year(year) for p in PROJECTS.values()]
    yearhud = '\n\n'.join(graphs)
    print(yearhud)


@cli.command()
@click.argument('name', nargs=1)
def project(name):
    """Render all data for the given project (by year)."""
    project = PROJECTS[name]
    projhud = project.render_project()
    print(projhud)


@cli.command()
@click.argument('name', nargs=1)
def track(name):
    """Start/stop time tracking for the specified project."""
    project = PROJECTS[name]
    project.track()


if __name__ == '__main__':
    # command()
    print()
    cli()
