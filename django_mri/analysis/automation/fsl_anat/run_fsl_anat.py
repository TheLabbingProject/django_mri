from typing import Dict, Iterable, List

from celery.result import AsyncResult
from django.db.models import QuerySet
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.definitions.input_definition import \
    InputDefinition
from django_analyses.models.pipeline.node import Node
from django_analyses.tasks import execute_node

from django_mri.models.scan import Scan

TITLE = "FSL Anatomical Processing Script"
NODE_CONFIGURATION = {}
INPUT_DEFINITION_KEY = "image"
ANATOMICAL_FILTER = {
    "dicom__scanning_sequence": ["GR", "IR"],
    "dicom__sequence_variant": ["SK", "SP", "MP"],
}


def get_version() -> AnalysisVersion:
    fsl_anat = Analysis.objects.get(title=TITLE)
    return fsl_anat.version_set.first()


def get_node() -> Node:
    fsl_anat_v = get_version()
    return Node.objects.get_or_create(
        analysis_version=fsl_anat_v, configuration=NODE_CONFIGURATION
    )[0]


def get_input_definition() -> InputDefinition:
    fsl_anat_v = get_version()
    return fsl_anat_v.input_definitions.get(key=INPUT_DEFINITION_KEY)


def get_existing_run_paths() -> QuerySet:
    input_definition = get_input_definition()
    return input_definition.input_set.values_list("value", flat=True)


def get_missing() -> QuerySet:
    anatomicals = Scan.objects.filter(**ANATOMICAL_FILTER)
    existing = get_existing_run_paths()
    return anatomicals.exclude(_nifti__path__in=existing)


def create_inputs(qs: QuerySet) -> List[Dict[str, str]]:
    inputs = []
    for scan in qs:
        try:
            inputs.append({INPUT_DEFINITION_KEY: str(scan.nifti.path)})
        except RuntimeError:
            pass
    return inputs


def run_fsl_anat(qs: QuerySet = None) -> AsyncResult:
    qs = qs if isinstance(qs, Iterable) else get_missing()
    node = get_node()
    inputs = create_inputs(qs)
    return execute_node.delay(node_id=node.id, inputs=inputs)
