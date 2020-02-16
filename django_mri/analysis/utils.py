from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion

BAD_ANALYSIS_IDENTIFIER = "Analysis identifier must be either a string representing the title, the analysis ID, or an instance of the Analysis class!"  # noqa: E501


def get_lastest_analysis_version(analysis) -> AnalysisVersion:
    if isinstance(analysis, str):
        return AnalysisVersion.objects.filter(analysis__title=analysis).first()
    elif isinstance(analysis, (int, Analysis)):
        return AnalysisVersion.objects.filter(analysis=analysis).first()
    raise ValueError(BAD_ANALYSIS_IDENTIFIER)
