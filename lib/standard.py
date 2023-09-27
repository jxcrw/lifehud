#!/usr/bin/env python3
"""A hi-lo standard"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Standard:
    """A time period."""
    lo: float
    hi: float
