#!/usr/bin/env python3
"""Lifehud"""
import shutil

from cfg.config import ENABLE_ARCHIVING, DIR_ARCHIVE, DIR_SYNC
from ui.cli import cli


if __name__ == '__main__':
    if ENABLE_ARCHIVING:
        shutil.copytree(DIR_SYNC, DIR_ARCHIVE, dirs_exist_ok=True)
    print()
    cli()
