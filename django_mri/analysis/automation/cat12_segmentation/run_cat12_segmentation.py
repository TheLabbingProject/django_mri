from typing import Dict, List

from django.db.models import QuerySet
from django_analyses.tasks import execute_node
from django_dicom.models.utils.progressbar import create_progressbar
from django_mri.analysis.automation.cat12_segmentation.utils import (
    get_missing,
    get_node,
)

PROGRESSBAR_KWARGS = {"unit": "scan", "desc": "Preparing NIfTI file inputs"}


def create_inputs(
    scans: QuerySet, progressbar: bool = True
) -> List[Dict[str, List[str]]]:
    iterable = create_progressbar(
        scans, disable=not progressbar, **PROGRESSBAR_KWARGS
    )
    inputs = []
    for scan in iterable:
        try:
            item = {"path": str(scan.nifti.path)}
        except RuntimeError:
            print(f"Failed to convert scan #{scan.id} to NIfTI.")
        else:
            inputs.append(item)
    return inputs


def run_cat12_segmentation(
    queryset: QuerySet = None,
    max_total: int = None,
    prep_progressbar: bool = True,
):
    queryset = queryset or get_missing()
    if max_total:
        queryset = queryset[:max_total]
    inputs = create_inputs(queryset, prep_progressbar)
    node = get_node()
    return execute_node.delay(node_id=node.id, inputs=inputs)
