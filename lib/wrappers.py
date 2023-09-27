#!/usr/bin/env python3
"""Wrapper classes/veneers/etc."""

from dataclasses import dataclass
from datetime import date
from typing import Callable

import click


@dataclass
class Period:
    """A time period."""
    start: date
    end: date


@dataclass
class Chain:
    """A curr-max chain."""
    curr: float
    max: float


@dataclass
class Standard:
    """A lo-hi standard."""
    lo: float
    hi: float


@dataclass
class DataHandler:
    """A handler for str → obj conversion and obj → str formatting."""
    converter: Callable
    formatter: Callable


class ClickGroupInlineOrder(click.Group):
    """For keeping commands in their inline source code order on the help page."""
    def list_commands(self, ctx):
        return self.commands.keys()
