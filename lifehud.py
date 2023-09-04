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
            data = [line.split('\t') for line in data]
            data = {datetime.datetime.strptime(line[0], '%Y/%m/%d').date(): float(line[1]) for line in data}
            datasets[name] = data

    return datasets


def build_graph(data: set, standard: int) -> str:
    """Build a contribution graph based on the given data."""
    std_lo, std_hi = standard[0], standard[1]

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
                if date in data:
                    val = data[date]
                    color = get_color(val, standard)
                else:
                    color = Fore.LIGHTBLACK_EX
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


def get_color(val: float, standard: tuple):
    """Color a value according to the given standard."""
    std_lo, std_hi = standard[0], standard[1]
    color = Fore.WHITE
    if val == 0:
        color = Fore.LIGHTBLACK_EX
    elif val <= std_lo:
        color = Fore.RED
    elif val >= std_hi:
        color = Fore.GREEN
    else:
        color = Fore.YELLOW
    return color



if __name__ == '__main__':
    cags = [('mind', (7, 8)), ('body', (1, 1)), ('pool', (1, 2))]
    datasets = load_data()

    print()
    for cag in cags:
        name, std = cag[0], cag[1]
        data = datasets[name]
        graph = build_graph(data, std)

        print(Fore.WHITE + name)
        print(graph)
        print()
