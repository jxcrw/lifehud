#!/usr/bin/env python3
"""LifeHUD2"""

from datetime import date

from _cfg.config import PROJECTS


def get_smart_today() -> date:
    """Get today as the date of the user's latest wakeup event."""
    latest_wake_date = PROJECTS['0'].data.iloc[0]['date']
    return latest_wake_date


if __name__ == '__main__':
    print(get_smart_today())
