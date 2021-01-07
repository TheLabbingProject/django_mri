from django.db.models import QuerySet
from django_analyses.tasks import execute_node
from django_dicom.models.utils.progressbar import create_progressbar
from django_mri.analysis.automation.recon_all.utils import get_recon_all_node
from django_mri.analysis.automation.utils import get_mprage
from django_mri.models.scan import Scan
from typing import Dict, Iterable, List


RECON_ALL_NODE = get_recon_all_node()
T1_FILES_KEY = "T1_files"
T1_FILES = RECON_ALL_NODE.analysis_version.input_definitions.get(
    key=T1_FILES_KEY
)
PROGRESSBAR_KWARGS = {"unit": "scan", "desc": "Preparing NIfTI file inputs"}


def has_base_result(scan: Scan) -> bool:
    return scan._nifti and T1_FILES.input_set.filter(
        value=f"[{scan.nifti.path}]"
    )


def get_missing_base_recon_all() -> QuerySet:
    scan_ids = [scan.id for scan in get_mprage() if not has_base_result(scan)]
    return Scan.objects.filter(id__in=scan_ids)


def create_inputs(
    scans: QuerySet, progressbar: bool = True
) -> List[Dict[str, List[str]]]:
    iterable = create_progressbar(
        scans, disable=not progressbar, **PROGRESSBAR_KWARGS
    )
    inputs = []
    for scan in iterable:
        try:
            item = {"T1_files": [str(scan.nifti.path)]}
        except RuntimeError:
            print(f"Failed to convert scan #{scan.id} to NIfTI.")
        else:
            inputs.append(item)
    return inputs


def run_base_recon_all(scans: QuerySet = None, progressbar: bool = True):
    scans = (
        scans if isinstance(scans, Iterable) else get_missing_base_recon_all()
    )
    inputs = create_inputs(scans, progressbar)
    return execute_node.delay(node_id=RECON_ALL_NODE.id, inputs=inputs)
