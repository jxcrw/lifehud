#!/usr/bin/env python3
"""Wrappers, veneers, helper classes, etc."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Period:
    """A time period."""
    start: date
    end: date


@dataclass
class Chain:
    """A curr-max chain"""
    curr: float
    max: float


@dataclass
class Standard:
    """A hi-lo standard."""
    lo: float
    hi: float
