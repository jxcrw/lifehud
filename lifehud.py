#!/usr/bin/env python3
"""LifeHUD"""

from collections import defaultdict
import datetime

from colorama import Fore

# Set up
now = datetime.datetime.now()
start = datetime.date(now.year, 1, 1)

end_curr = now.date()
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
            color = Fore.GREEN if date <= end_curr else Fore.BLACK
            daychar = color + '⯀' # Alt: ●
        else:
            daychar = ' '
        daychars.append(daychar)
    weekchars.append(daychars)


# Print out year
for daynum in range(7):
    days = [weekchar[daynum] for weekchar in weekchars]
    print(' '.join(days))
