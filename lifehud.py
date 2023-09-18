#!/usr/bin/env python3
"""Lifehud"""

from datetime import date, timedelta

import click
from colorama import Fore

from cfg.projects import PROJECTS


class GroupInlineOrder(click.Group):
    """Keep commands in the order they are defined in code in the help page."""
    def list_commands(self, ctx):
        return self.commands.keys()

@click.group(cls=GroupInlineOrder)
def cli():
    """Visualize progress on life projects in the form of contribution graphs."""
    pass


@cli.command()
@click.option('--num', '-n', default=2, help="The number of weeks to render, starting from the current week.")
@click.option('--stats', '-s', is_flag=True, default=False, help="Show cumulative stats for week.")
@click.option('--opt', '-o', is_flag=True, default=False, help="Show optional projects too.")
def week(num, stats, opt):
    """Render a weekly lifehud."""
    weekhuds, today, projects = [], date.today(), PROJECTS
    if not opt:
        projects = {k: v for k, v in PROJECTS.items() if v.required}
    for i in range(num):
        day = today - timedelta(days=i*7)
        graphs = [p.render_week(day, stats) for p in projects.values()]
        weekhud = '\n'.join(graphs)
        weeknum = day.strftime('%U')
        weekhuds.append(f'{Fore.BLACK}Week {weeknum}\n{weekhud}')
    print('\n\n'.join(weekhuds))


@cli.command()
def year():
    """Render a yearly lifehud."""
    year = date.today().year
    graphs = [p.render_year(year) for p in PROJECTS.values()]
    yearhud = '\n\n'.join(graphs)
    print(yearhud)


@cli.command()
@click.argument('name', nargs=1)
def project(name):
    """Render all data for the specified project (by year)."""
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
