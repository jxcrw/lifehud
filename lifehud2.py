#!/usr/bin/env python3
"""LifeHUD2"""

import os
from pathlib import Path

from pandas import DataFrame
import pandas as pd

from _cfg.config import DIR_SYNC


def load_dataframes() -> dict[str, DataFrame]:
    """Load up dataframes of life data."""
    dfs = {}
    for root, dirs, files in os.walk(DIR_SYNC):
        files = [Path(root, file) for file in files if '0' in file]
        for file in files:
            df = pd.read_csv(file, sep='\t')
            dfs[file.stem] = df
    return dfs


if __name__ == '__main__':
    dfs = load_dataframes()
