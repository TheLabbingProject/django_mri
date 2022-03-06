"""
Messages for the :mod:`~django_mri.models.managers` module.
"""

SCORES_EMPTY: str = "Parsed results for {run} returned empty!"
SCORES_BAD_INDEX: str = "Parsed results must return a DataFrame with three index levels (atlas, hemisphere, region), {run} return {n_levels}!"
SCORES_BAD_TYPE: str = "Score generation from parsed run output must return a pandas DataFrame, {run} returned {bad_type}!"

# flake8: noqa: E501
