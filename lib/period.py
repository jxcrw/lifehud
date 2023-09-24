#!/usr/bin/env python3
"""A time period"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Period:
    """A time period."""
    start: date
    end: date
