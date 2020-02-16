import gzip
import shutil

from pathlib import Path


def uncompress(
    source: Path, destination: Path = None, keep_source: bool = True
) -> Path:
    destination = destination or source.with_suffix("")
    with gzip.open(source, "rb") as compressed_data:
        with open(destination, "wb") as uncompressed_data:
            shutil.copyfileobj(compressed_data, uncompressed_data)
    if not keep_source:
        source.unlink()
    return destination


def compress(source: Path, destination: Path = None, keep_source: bool = True) -> Path:
    destination = destination or source.with_suffix(source.suffix + ".gz")
    with open(source, "rb") as uncompressed_data:
        with gzip.open(destination, "wb") as compressed_file:
            shutil.copyfileobj(uncompressed_data, compressed_file)
    if not keep_source:
        source.unlink()
    return destination
