from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.pipeline.node import Node
from django_mri.analysis.automation.recon_all.messages import (
    NO_RECON_ALL_VERSIONS,
)

ANALYSIS_TITLE = "ReconAll"
VERSION_TITLE = "6.0.0"
RECON_ALL_CONFIGURATION = {}


def get_recon_all_version(title: str = VERSION_TITLE) -> AnalysisVersion:
    if isinstance(title, str):
        return AnalysisVersion.objects.get(
            analysis__title=ANALYSIS_TITLE, title=title
        )
    else:
        version_set = AnalysisVersion.objects.filter(
            analysis__title=ANALYSIS_TITLE
        )
        if version_set:
            return version_set.first()
        else:
            raise AnalysisVersion.DoesNotExist(NO_RECON_ALL_VERSIONS)


def get_recon_all_node(
    version_title: str = VERSION_TITLE, configuration: dict = None
) -> Node:
    recon_all_v = get_recon_all_version(version_title)
    configuration = (
        configuration
        if isinstance(configuration, dict)
        else RECON_ALL_CONFIGURATION
    )
    return Node.objects.get_or_create(
        analysis_version=recon_all_v, configuration=configuration
    )[0]
