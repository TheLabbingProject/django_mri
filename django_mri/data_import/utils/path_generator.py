import os

from pathlib import Path


def path_generator(path: str, extension: str = "") -> Path:
    """
    Generates paths from the given directory tree.

    Parameters
    ----------
    extension : str
        A file extension to filter the generated files with.

    Returns
    -------
    pathlib.Path
        File path.
    """

    for directory, _, files in os.walk(path):
        if extension:
            files = [f for f in files if f.endswith(f".{extension}")]
        for file_name in files:
            yield Path(os.path.join(directory, file_name))
