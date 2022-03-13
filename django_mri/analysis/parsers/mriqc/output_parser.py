import json
from pathlib import Path

import pandas as pd


class MriqcOutputParser:
    def __init__(self, path: Path) -> None:
        self.path = path

    def parse(self) -> pd.DataFrame:
        series = []
        for json_path in self.path.rglob("*.json"):
            if json_path.stem == "dataset_description":
                continue
            with open(json_path, "r") as json_file:
                content = json.load(json_file)
                del content["bids_meta"]
                del content["provenance"]
                series.append(pd.Series(content, name=json_path.stem))
        return pd.DataFrame(series)
