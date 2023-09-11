#!/usr/bin/env python3
"""LifeHUD2"""

from dataclasses import dataclass

from pandas import DataFrame
import pandas as pd

from _cfg.config import DIR_SYNC


@dataclass
class Project:
    """A life project."""
    name: str
    metric: str
    std_lo: float
    std_hi: float
    delayed_start: int = 0
    autoopen: bool = False
    weekmask: str = 'Sun Mon Tue Wed Thu Fri Sat'
    data: DataFrame = None

    def load_data(self) -> None:
        """Load up the project's data."""
        path = DIR_SYNC / f'{self.name}.tsv'
        self.data = pd.read_csv(path, sep='\t')


if __name__ == '__main__':
    project_0 = Project('0', 'hours', 1, 1, 20, True, 'Sun Mon Tue Wed Thu Fri')
    project_0.load_data()
