#!/usr/bin/env python3
"""Settings"""

from pathlib import Path
import sys


DIR_HOME = Path.home()
DIR_ROOT = Path(sys.path[1])
DIR_DATA = DIR_ROOT / '_arc/data'
DIR_SYNC = DIR_HOME / 'Dropbox/lifehud'

DIR_DATA = DIR_SYNC  # TODO
