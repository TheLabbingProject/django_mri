from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.pipeline.node import Node


def get_mrconvert_analysis_version():
    try:
        return AnalysisVersion.objects.get_by_string_id("mrconvert")
    except AnalysisVersion.DoesNotExist:
        raise AnalysisVersion.DoesNotExist(
            "MRconvert interface not registered in database."
        )


def get_mrconvert_node():
    configuration = {}
    analysis_version = get_mrconvert_analysis_version()
    return Node.objects.get_or_create(
        analysis_version=analysis_version, configuration=configuration
    )

