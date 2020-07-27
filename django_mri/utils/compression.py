"""
Definition of the :func:`~django_mri.utils.compression.compress` and
:func:`~django_mri.utils.compression.uncompress` utility functions.
"""

import gzip
import shutil

from pathlib import Path


def uncompress(
    source: Path, destination: Path = None, keep_source: bool = True
) -> Path:
    """
    Uncompresses the provided (compressed) *source* file.

    Parameters
    ----------
    source : Path
        File to uncompress
    destination : Path, optional
        Uncompressed output file path, by default None
    keep_source : bool, optional
        Whether to keep the source file or not, by default True

    Returns
    -------
    Path
        Output file path
    """

    destination = destination or source.with_suffix("")
    with gzip.open(source, "rb") as compressed_data:
        with open(destination, "wb") as uncompressed_data:
            shutil.copyfileobj(compressed_data, uncompressed_data)
    if not keep_source:
        source.unlink()
    return destination


def compress(
    source: Path, destination: Path = None, keep_source: bool = True
) -> Path:
    """
    Compresses the provided *source* file.

    Parameters
    ----------
    source : Path
        File to compress
    destination : Path, optional
        Compressed output file path, by default None
    keep_source : bool, optional
        Whether to keep the source file or not, by default True

    Returns
    -------
    Path
        Output file path
    """

    destination = destination or source.with_suffix(source.suffix + ".gz")
    with open(source, "rb") as uncompressed_data:
        with gzip.open(destination, "wb") as compressed_file:
            shutil.copyfileobj(uncompressed_data, compressed_file)
    if not keep_source:
        source.unlink()
    return destination
