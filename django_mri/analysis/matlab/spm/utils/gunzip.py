import gzip
import shutil

from pathlib import Path


def gunzip(path: Path, destination: Path = None) -> Path:
    with gzip.open(path, "rb") as compressed_data:
        unzipped_path = destination or path.with_suffix("")
        with open(unzipped_path, "wb") as uncompressed_data:
            shutil.copyfileobj(compressed_data, uncompressed_data)
    return unzipped_path
