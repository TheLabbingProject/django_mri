from pathlib import Path
from typing import List, Union

import pandas as pd

from django_mri.analysis.automation.recon_all.stats import ReconAllStats


class ReconAllResults:
    STATS_DIR = "stats"

    def __init__(self, path: Path):
        self.path = Path(path)
        self.stats = ReconAllStats(path / self.STATS_DIR)

    @classmethod
    def extract_stats(cls, path: Union[Path, List[Path]]) -> pd.DataFrame:
        if isinstance(path, Path):
            return ReconAllStats(path).to_dataframe()
        else:
            all_stats = None
            for run_path in path:
                stats_path = run_path / cls.STATS_DIR
                stats = ReconAllStats(stats_path).to_dataframe()
                if not stats.empty:
                    stats["Subject ID"] = stats_path.parent.name
                    if all_stats is None:
                        all_stats = stats.copy()
                    else:
                        all_stats = all_stats.append(stats)
            indices = ["Subject ID"] + ReconAllStats.INDICES
            return all_stats.reset_index().set_index(indices)
