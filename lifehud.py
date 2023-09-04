#!/usr/bin/env python3
"""LifeHUD"""

import datetime
import random
from collections import defaultdict


date_start = datetime.date(2023, 1, 1)
date_end = datetime.date(2023, 12, 31)
delta = datetime.timedelta(days=1)

weeks = defaultdict(dict)
date = date_start
while date <= date_end:
    # print(date.strftime('%U %m-%d %a'))

    week = int(date.strftime('%U'))
    day = int(date.strftime('%w'))
    weeks[week][day] = date.strftime('%m-%d')

    date += delta
# print(weeks)


weekchars = []
for weeknum, week in weeks.items():
    daychars = []
    for daynum in range(7):
        daychar = '▮' if daynum in week else ' '
        daychars.append(daychar)
    weekchars.append(daychars)
    # print(''.join(daychars))

Sundays = [weekchar[0] for weekchar in weekchars]
Mondays = [weekchar[1] for weekchar in weekchars]
Tuesdays = [weekchar[2] for weekchar in weekchars]
Wednesdays = [weekchar[3] for weekchar in weekchars]
Thursdays = [weekchar[4] for weekchar in weekchars]
Fridays = [weekchar[5] for weekchar in weekchars]
Saturdays = [weekchar[6] for weekchar in weekchars]

print('Mind')
print(' '.join(Sundays))
print(' '.join(Mondays))
print(' '.join(Tuesdays))
print(' '.join(Wednesdays))
print(' '.join(Thursdays))
print(' '.join(Fridays))
print(' '.join(Saturdays))
print()

print('Body')
print(' '.join(Sundays))
print(' '.join(Mondays))
print(' '.join(Tuesdays))
print(' '.join(Wednesdays))
print(' '.join(Thursdays))
print(' '.join(Fridays))
print(' '.join(Saturdays))
print()

print('Pool')
print(' '.join(Sundays))
print(' '.join(Mondays))
print(' '.join(Tuesdays))
print(' '.join(Wednesdays))
print(' '.join(Thursdays))
print(' '.join(Fridays))
print(' '.join(Saturdays))
print()

print('Lang')
print(' '.join(Sundays))
print(' '.join(Mondays))
print(' '.join(Tuesdays))
print(' '.join(Wednesdays))
print(' '.join(Thursdays))
print(' '.join(Fridays))
print(' '.join(Saturdays))
print()

print('Work')
print(' '.join(Sundays))
print(' '.join(Mondays))
print(' '.join(Tuesdays))
print(' '.join(Wednesdays))
print(' '.join(Thursdays))
print(' '.join(Fridays))
print(' '.join(Saturdays))
print()
