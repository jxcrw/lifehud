#!/usr/bin/env python3
"""LifeHUD"""

from collections import defaultdict, deque
import datetime
import os
from pathlib import Path
import subprocess
import sys

from ahk import AHK
from colorama import Back, Fore, Style
import pyperclip

from _cfg.config import DIR_DATA, DIR_ROOT, DIR_SYNC


def load_data() -> dict:
    """Load up the data to be graphed."""
    datafiles = []
    for root, dirs, files in os.walk(DIR_DATA):
        protected = ['00.tsv', '01.tsv', 'bodi.tsv', 'mynd.tsv']
        files = [os.path.join(root, file) for file in files if file not in protected]
        files = [Path(file) for file in files]
        datafiles.extend(files)

    datasets = {}
    for file in datafiles:
        with open(file, 'r', encoding='utf-8') as f:
            name = file.stem
            data = [line.strip() for line in f]
            data = [line for line in data if 'wip' not in line]
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
    today = get_smart_today()

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


def get_dot(date, data, standard) -> str:
    today = get_smart_today()
    date = date.date()
    if date in data:
        val = data[date]
        result = get_result(val, standard)
        fore = result2fore(result)
    else:
        fore = Fore.LIGHTBLACK_EX
        result = (0, 'zero')
    dot = fore + '⯀'  # Alt: ●
    if date == today and result[1] != 'zero':
        dot = "\033[4m" + dot + "\033[0m"
    elif date == today and result[1] == 'zero':
        dot = Back.BLACK + dot
    else:
        dot = Back.RESET + dot
    return dot


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
    with open(DIR_ROOT / 'work.tsv', 'r', encoding='utf-8') as f:
        data = [line.strip().split('\t')[0] for line in f]
    dataset = defaultdict(int)
    for line in data:
        dataset[line] += 1

    items = [[str(key), str(val)] for key, val in dataset.items()]
    items = ['\t'.join(item) for item in items]
    items.sort()
    with open(DIR_DATA / 'work.tsv', 'w+', newline='\n', encoding='utf-8') as f:
        f.write('\n'.join(items))


def calc_life(datasets, cags):
    # Set up dates
    now = datetime.datetime.now()
    start = datetime.date(2012, 1, 1)
    end_year = now.date()
    delta = datetime.timedelta(days=1)

    # Build dict(date → total_score)
    curr, scores = start, defaultdict(int)
    while curr <= end_year:
        total = 0
        for dataset, cag in zip(datasets, cags.keys()):
            name, std = cag, cags[cag]
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
    items.sort(reverse=True)
    with open(DIR_DATA / 'LIFE.tsv', 'w+', newline='\n', encoding='utf-8') as f:
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


def get_smart_today():
    # Get wake up time
    with open(DIR_SYNC / 'mind.tsv', 'r', encoding='utf-8') as f:
        data = [line.strip().split('\t') for line in f]
        latest = data[0]
        wake = datetime.datetime.strptime(latest[0] + latest[2], '%Y-%m-%d%H:%M')

    # Compare to now
    now = datetime.datetime.now()
    now_date = now.date()
    wake_date = wake.date()

    if now_date == wake_date:
        today = now_date
    else:
        today = now_date - datetime.timedelta(days=1)

    return today


def get_current_week_dates():
    # Get the current date
    smart_today = get_smart_today()
    current_date = datetime.datetime(year=smart_today.year, month=smart_today.month, day=smart_today.day)

    # Find the starting date (Monday) of the current week
    days_to_subtract = (current_date.weekday() + 1) % 7
    start_of_week = current_date - datetime.timedelta(days=days_to_subtract)

    # Create a list to store the datetime objects for each day in the week
    week_dates = []

    # Loop through the days of the week, adding them to the list
    for i in range(7):
        week_dates.append(start_of_week + datetime.timedelta(days=i))

    return week_dates


def track(proj: str, delay: int = 0, smart_today: bool = True, autoopen: bool = False) -> None:
    """Start/stop time tracking for the given project (with an optional start delay in mins)."""
    # Setup
    path = DIR_SYNC / f'{proj}.tsv'
    with open(path, 'r', encoding='utf-8') as f:
        data = deque([line.strip().split('\t') for line in f])

    now = datetime.datetime.now()
    today = get_smart_today() if smart_today else datetime.datetime.today()
    now = now.replace(year=today.year, month=today.month, day=today.day)
    latest = data[0]
    is_new = latest[1] != 'wip'

    # Start or stop tracker
    if is_new:
        start = now + datetime.timedelta(minutes=delay)
        date = now.strftime('%Y-%m-%d')
        start = start.strftime('%H:%M')
        hours = end = 'wip'
        sesh = [date, hours, start, end]
        data.appendleft(sesh)

        message = proj
        color = '9ece6a'
        toast(message, color)
    else:
        start = datetime.datetime.strptime(latest[0] + latest[2], '%Y-%m-%d%H:%M')
        duration = (now - start).seconds / 3600
        latest[1] = f'{duration:0.2f}'
        latest[3] = now.strftime('%H:%M')

        if autoopen:
            subprocess.run(['subl.exe', f'{path}:1:29'])

        message = f'{proj} ({latest[1]}h)'
        color = 'f7768e'
        toast(message, color)

    # Write data
    with open(path, 'w+', newline='\n', encoding='utf-8') as f:
        f.write('\n'.join(['\t'.join(entry) for entry in data]))
    pyperclip.copy(message)
    print(message)


def toast(message: str, color: str) -> None:
    """Display a toast message."""
    ahk = AHK()
    script = f'''
        SplashImage,, B1 FS12 CW1a1b26 CT{color}, {message},,, Consolas
        Sleep, 3000
        SplashImage
        SplashImage, Off
    '''
    ahk.run_script(script)




if __name__ == '__main__':
    # ┌─────────────────────────────────────────────────────────────────────────────
    # │ Setup
    # └─────────────────────────────────────────────────────────────────────────────
    # process_work()
    cags = {
        'mind': (7, 7.9),
        'body': (1, 1),
        'pool': (1, 2),
        'lang': (10, 40),
        'work': (1, 3),
        'LIFE': (2, 4.25),
    }
    datasets = load_data()
    calc_life(datasets, cags)


    # ┌─────────────────────────────────────────────────────────────────────────────
    # │ UI
    # └─────────────────────────────────────────────────────────────────────────────
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'

    match mode:
        case 'all':
            # Individual categories
            print()
            graphs = []
            for cag, std in cags.items():
                data = datasets[cag]
                graph = build_graph(cag, data, std, 2023)
                string = f'{Fore.WHITE + cag}\n{graph}'
                graphs.append(string)
            print('\n\n'.join(graphs))
        case 'week':
            # Current week
            print()
            dates = get_current_week_dates()
            strings = []
            for cag, std in cags.items():
                project = [Fore.WHITE + cag]
                data = datasets[cag]
                for date in dates:
                    dot = get_dot(date, data, std)
                    project.append(dot + Back.RESET)
                strings.append(project)
            print('\n'.join([' '.join(entry) for entry in strings]))
        case 'track':
            # Start/end a tracker
            proj = sys.argv[2]
            smart_today = False if proj == 'mind' else True
            delay, autoopen = 0, False
            match proj:
                case 'mind':
                    delay = 30
                case 'body':
                    delay = 20
                    autoopen = True
                case 'lang':
                    delay = None
                    print('lang cannot be manually tracked!')
                case 'social':
                    autoopen = True
                case _:
                    print('something probably went wrong!')
            track(proj, delay, smart_today, autoopen)
        case _:
            name = mode
            dataset = datasets[name]
            standard = cags[name]
            go_by_year(name, dataset, standard)
