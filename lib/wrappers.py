#!/usr/bin/env python3
"""Wrapper classes/veneers/etc."""

from dataclasses import dataclass
from datetime import date
from typing import Callable

import click
from colorama import Fore


@dataclass
class Period:
    """A time period."""
    start: date
    end: date


@dataclass
class Chain:
    """An active-max chain."""
    active: float
    max: float


@dataclass
class Standard:
    """A lo-hi standard."""
    lo: float
    hi: float


@dataclass
class Score:
    """A contribution score and its styling."""
    val: float
    fore: Fore
    color_hex: str

    def __gt__(self, other) -> bool:
        return self.val > other.val

    def __ge__(self, other) -> bool:
        return self.val >= other.val


@dataclass
class DataHandler:
    """A handler for str → obj conversion and obj → str formatting."""
    converter: Callable
    formatter: Callable


class ClickGroupInlineOrder(click.Group):
    """For keeping commands in their inline source code order on the help page."""
    def list_commands(self, ctx):
        return self.commands.keys()
