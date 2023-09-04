#!/usr/bin/env python3
"""LifeHUD"""

from collections import defaultdict
import datetime
import os
from pathlib import Path

from colorama import Fore


DIR_ROOT = Path(r'C:\~\dev\lifehud')
DIR_DATA = DIR_ROOT / 'data'


def load_data() -> dict:
    """Load up the data to be graphed."""
    datafiles = []
    for root, dirs, files in os.walk(DIR_DATA):
        files = [os.path.join(root, file) for file in files]
        files = [Path(file) for file in files]
        datafiles.extend(files)

    datasets = {}
    for file in datafiles:
        with open(file, 'r', encoding='utf-8') as f:
            name = file.stem
            data = [line.strip() for line in f]
            data = [line.split('\t')[0] for line in data]
            data = [datetime.datetime.strptime(line, '%Y/%m/%d') for line in data]
            data = [thing.date() for thing in data]
            data = set(data)
            datasets[name] = data

    return datasets


def build_graph(data: set) -> str:
    """Build a contribution graph based on the given data."""
    # Set up dates
    now = datetime.datetime.now()
    start = datetime.date(now.year, 1, 1)
    end_year = datetime.date(now.year, 12, 31)
    delta = datetime.timedelta(days=1)

    # Build dict(weeknum → dict(daynum → date))
    curr, weeks = start, defaultdict(dict)
    while curr <= end_year:
        weeknum = int(curr.strftime('%U'))
        daynum = int(curr.strftime('%w'))
        weeks[weeknum][daynum] = curr
        curr += delta

    # Convert weeks to string reps
    weekchars = []
    for weeknum, week in weeks.items():
        daychars = []
        for daynum in range(7):
            if daynum in week:
                date = week[daynum]
                color = Fore.GREEN if date in data else Fore.LIGHTBLACK_EX
                daychar = color + '⯀'  # Alt: ●
            else:
                daychar = ' '
            daychars.append(daychar)
        weekchars.append(daychars)

    # Build up by day of week
    daysof = []
    for daynum in range(7):
        days = [weekchar[daynum] for weekchar in weekchars]
        dayof = ' '.join(days)
        daysof.append(dayof)

    graph = '\n'.join(daysof)
    return graph


if __name__ == '__main__':
    cags = ['mind', 'body', 'pool']
    datasets = load_data()

    print()
    for cag in cags:
        data = datasets[cag]
        graph = build_graph(data)

        print(Fore.WHITE + cag)
        print(graph)
        print()
