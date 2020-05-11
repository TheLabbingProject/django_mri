from tqdm import tqdm

DESCRIPTION = "Importing MRI data"
UNIT = "scan"


def create_progressbar(iterable, **kwargs) -> tqdm:
    """
    Creates a progressbar wrapping the path generator using the tqdm_ library.

    .. _tqdm: https://github.com/tqdm/tqdm

    Parameters
    ----------
    iterable : iterable
        Iterable to iterate over

    Returns
    -------
    tqdm.std.tqdm
        Progressbar
    """

    return tqdm(
        desc=kwargs.get("desc", DESCRIPTION),
        disable=kwargs.get("disable", False),
        iterable=iterable,
        unit=kwargs.get("unit", UNIT),
    )
