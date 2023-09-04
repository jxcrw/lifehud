#!/usr/bin/env python3
"""LifeHUD"""

from collections import defaultdict
from datetime import timedelta, date, datetime

from colorama import Fore

# Load up data
with open('data.txt', 'r', encoding='utf-8') as f:
    data = [line.strip() for line in f]
    data = [line.split('\t')[0] for line in data]
    data = [datetime.strptime(line, '%Y/%m/%d') for line in data]
    data = [thing.date() for thing in data]
    data = set(data)


# Set up dates
now = datetime.now()
start = date(now.year, 1, 1)

end_curr = now.date()
end_year = date(now.year, 12, 31)
delta = timedelta(days=1)


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
            daychar = color + '⯀' # Alt: ●
        else:
            daychar = ' '
        daychars.append(daychar)
    weekchars.append(daychars)


# Print out year
for daynum in range(7):
    days = [weekchar[daynum] for weekchar in weekchars]
    print(' '.join(days))
