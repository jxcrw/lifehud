#!/usr/bin/env python3
"""A curr-max chain"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Chain:
    """A curr-max chain"""
    curr: float
    max: float
