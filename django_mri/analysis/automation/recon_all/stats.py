from pathlib import Path
from typing import List

import pandas as pd

COLUMNS_TO_INT = [
    "Number of Vertices",
    "Surface Area",
    "Gray Matter Volume",
    "Folding Index",
]
HEMISPHERES = {"Left": "lh", "Right": "rh"}
ATLASES = {
    "Desikan-Killiany": "aparc",
    "Destrieux": "aparc.a2009s",
    "DKT": "aparc.DKTatlas",
    "Brodmann": "BA_exvivo",
}
MEASUREMENTS = [
    "Surface Area",
    "Gray Matter Volume",
    "Average Thickness",
    "Thickness StdDev",
    "Integrated Rectified Mean Curvature",
    "Integrated Rectified Gaussian Curvature",
    "Folding Index",
    "Intrinsic Curvature Index",
]
COLUMN_NAMES = ["Region Name", "Number of Vertices"] + MEASUREMENTS
START_COLUMNS = ["Hemisphere", "Atlas"] + COLUMN_NAMES
FILE_NAME = "{hemisphere_code}.{atlas_code}.stats"


class ReconAllStats:
    INDICES = ["Atlas", "Hemisphere", "Region Name"]

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def to_dataframe(self) -> pd.DataFrame:
        stats = pd.DataFrame(columns=START_COLUMNS)
        for atlas_name, atlas_code in ATLASES.items():
            for hemisphere_name, hemisphere_code in HEMISPHERES.items():
                name = FILE_NAME.format(
                    hemisphere_code=hemisphere_code, atlas_code=atlas_code
                )
                partial_stats_path = self.path / name
                if partial_stats_path.is_file():
                    data = pd.read_csv(
                        partial_stats_path,
                        comment="#",
                        names=COLUMN_NAMES,
                        delim_whitespace=True,
                    )
                    data["Hemisphere"] = hemisphere_name
                    data["Atlas"] = atlas_name
                    stats = stats.append(data)
        stats.set_index(self.INDICES, inplace=True)
        # Fix `object` columns
        for column_name in COLUMNS_TO_INT:
            stats[column_name] = stats[column_name].astype("int64")
        return stats
