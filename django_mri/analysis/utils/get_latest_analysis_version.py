"""
Definition of the
:func:`~django_mri.analysis.utils.get_lastest_analysis_version.get_lastest_analysis_version`
function.
"""

from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from typing import Union

_BAD_ANALYSIS_IDENTIFIER = "Analysis identifier must be either a string representing the title, the analysis ID, or an instance of the Analysis class!"  # noqa: E501


def get_lastest_analysis_version(
    analysis: Union[str, int, Analysis]
) -> AnalysisVersion:
    """
    Returns the "lastest" (first by descending title order) analysis version
    of the provided analysis.

    Analysis may be specified providing either its primary key, title, or an
    actual :class:`~django_analyses.models.analysis.Analysis` instance.

    Parameters
    ----------
    analysis : Union[str, int, ~django_analyses.models.analysis.Analysis]
        The desired analysis

    Returns
    -------
    ~django_analyses.models.analysis_version.AnalysisVersion
        First analysis version

    Raises
    ------
    ValueError
        No analysis version found
    """

    if isinstance(analysis, str):
        return AnalysisVersion.objects.filter(analysis__title=analysis).first()
    elif isinstance(analysis, (int, Analysis)):
        return AnalysisVersion.objects.filter(analysis=analysis).first()
    raise ValueError(_BAD_ANALYSIS_IDENTIFIER)
