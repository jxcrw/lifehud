#!/usr/bin/env python3
"""LifeHUD"""

from collections import defaultdict
import datetime
import os
from pathlib import Path

from colorama import Back, Fore, Style

USER = os.getenv('USERNAME')
DIR_ROOT = Path(r'C:\~\dev\lifehud')
DIR_DATA = DIR_ROOT / '_data'
DIR_SYNC = Path(rf'C:\Users\{USER}\Dropbox\lifehud')
DIR_DATA = DIR_SYNC


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
            data = {datetime.datetime.strptime(line[0], '%Y-%m-%d').date(): float(line[1]) for line in data}
            datasets[name] = data

    return datasets


def build_graph(name, data: set, standard: int, year: int) -> str:
    """Build a contribution graph based on the given data."""
    # Set up dates
    delta = datetime.timedelta(days=1)
    start = datetime.date(year, 1, 1)
    end_year = datetime.date(year, 12, 31)
    today = datetime.date.today() - delta

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
                    result = get_result(val, standard)
                    fore = result2fore(result)
                else:
                    fore = Fore.LIGHTBLACK_EX
                    result = (0, 'zero')
                daychar = fore + '⯀'  # Alt: ●
                if date == today and result[1] != 'zero':
                    daychar = "\033[4m" + daychar + "\033[0m"
                elif date == today and result[1] == 'zero':
                    daychar = Back.BLACK + daychar
                else:
                    daychar = Back.RESET + daychar
                # daychar = Style.RESET
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


def get_result(val: float, standard: tuple):
    """Color a value according to the given standard."""
    std_lo, std_hi = standard[0], standard[1]
    result = (0, 'zero')
    if val == 0:
        result = (0, 'zero')
    elif val <= std_lo:
        result = (0.25, 'bad')
    elif val >= std_hi:
        result = (1, 'good')
    else:
        result = (0.5, 'ok')
    return result


def result2fore(result: float):
    fores = {
        'zero': Fore.LIGHTBLACK_EX,
        'bad': Fore.RED,
        'ok': Fore.YELLOW,
        'good': Fore.GREEN
    }
    fore = fores[result[1]]
    return fore



def process_work():
    with open(DIR_ROOT / 'work.txt', 'r', encoding='utf-8') as f:
        data = [line.strip().split('\t')[0] for line in f]
    dataset = defaultdict(int)
    for line in data:
        dataset[line] += 1

    items = [[str(key), str(val)] for key, val in dataset.items()]
    items = ['\t'.join(item) for item in items]
    items.sort()
    with open(DIR_DATA / 'work.txt', 'w+', newline='\n', encoding='utf-8') as f:
        f.write('\n'.join(items))


def calc_life(datasets, cags):
    # Set up dates
    now = datetime.datetime.now()
    start = datetime.date(2012, 1, 1)
    end_year = datetime.date(now.year, 12, 31)
    delta = datetime.timedelta(days=1)

    # Build dict(date → total_score)
    curr, scores = start, defaultdict(int)
    while curr <= end_year:
        total = 0
        for dataset, cag in zip(datasets, cags):
            name, std = cag[0], cag[1]
            if name == 'life': continue
            data = datasets[name]
            val = data[curr] if curr in data else 0
            score = get_result(val, std)[0]
            total += score
        scores[curr] = total
        curr += delta

    # Write to file
    items = [[str(key), str(val)] for key, val in scores.items()]
    items = ['\t'.join(item) for item in items]
    items.sort()
    with open(DIR_DATA / 'LIFE.txt', 'w+', newline='\n', encoding='utf-8') as f:
        f.write('\n'.join(items))


def go_by_year(name: str, dataset, standard):
    years = list(set([date.year for date in dataset]))
    years.sort()
    print()
    for year in reversed(years):
        label = f'{name}-{year}'
        graph = build_graph(name, dataset, standard, year)
        print(Fore.WHITE + label)
        print(graph)
        print()


if __name__ == '__main__':
    # process_work()
    cags = [
        ('mind', (7, 7.9)),
        ('body', (1, 1)),
        ('pool', (1, 2)),
        ('lang', (10, 40)),
        ('work', (1, 3)),
        ('LIFE', (2, 4.25)),
    ]
    datasets = load_data()
    calc_life(datasets, cags)

    # Individual categories
    print()
    for cag in cags:
        name, std = cag[0], cag[1]
        data = datasets[name]
        graph = build_graph(name, data, std, 2023)

        print(Fore.WHITE + name)
        print(graph)
        print()

    # # By years
    # name = 'work'
    # dataset = datasets[name]
    # standard = (1, 3)
    # go_by_year(name, dataset, standard)
