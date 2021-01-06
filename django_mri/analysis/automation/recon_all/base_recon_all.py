from django.db.models import QuerySet
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.pipeline.node import Node
from django_analyses.tasks import execute_node
from django_mri.models.scan import Scan


RECON_ALL_VERSION = AnalysisVersion.objects.filter(
    analysis__title="ReconAll"
).first()

RECON_ALL_NODE = Node.objects.get(
    analysis_version=RECON_ALL_VERSION, configuration={}
)


def get_mprage() -> QuerySet:
    return Scan.objects.filter(description__icontains="mprage").order_by(
        "-time"
    )


def has_base_result(scan: Scan) -> bool:
    t1_files_definition = RECON_ALL_VERSION.input_definitions.get(
        key="T1_files"
    )
    return scan._nifti and t1_files_definition.input_set.filter(
        value=f"[{scan.nifti.path}]"
    )


def get_missing_base_recon_all() -> QuerySet:
    scan_ids = [scan.id for scan in get_mprage() if not has_base_result(scan)]
    return Scan.objects.filter(id__in=scan_ids)


def run_base_recon_all(scans: QuerySet):
    scans = scans if scans is not None else get_missing_base_recon_all()
    inputs = [{"T1_files": [str(scan.nifti.path)]} for scan in scans]
    return execute_node.delay(node_id=RECON_ALL_NODE.id, inputs=inputs)
