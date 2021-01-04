from celery import shared_task
from django_analyses.tasks import execute_node
from django_analyses.models.pipeline.node import Node
from django_mri.models.data_directory import DataDirectory
from django_mri.models.scan import Scan
from django_mri.models.sequence_type import SequenceType
from pathlib import Path
from typing import Union


@shared_task(name="django_mri.import-data")
def import_data(data_directory: Union[int, str, Path]) -> list:
    """
    Imports new data (unfamiliar subdirectories) from the provided
    :class:`~django_mri.models.data_directory.DataDirectory` instance.

    Parameters
    ----------
    data_directory : Union[int, str, Path]
        Directory path or DataDirectory instance ID

    Returns
    -------
    list
        The names of the subdirectories within the DataDirectory that were
        imported
    """

    if isinstance(data_directory, int):
        source = DataDirectory.objects.get(id=data_directory)
        imported_subdirectories = source.sync(progressbar=False, report=True)
        return imported_subdirectories
    else:
        Scan.objects.import_path(
            data_directory, progressbar=False, report=False
        )


@shared_task(name="django_mri.run-recon-all")
def run_recon_all(scan_ids: list):
    scans = Scan.objects.filter(id__in=scan_ids)
    recon_all_node, _ = Node.objects.get_or_create(
        analysis_version__analysis__title="ReconAll", configuration={}
    )
    mprage = SequenceType.objects.get(title="MPRAGE")
    inputs = [
        {"T1_files": [str(scan.nifti.path)]}
        for scan in scans
        if scan.sequence_type == mprage
    ]
    return execute_node.delay(node_id=recon_all_node.id, inputs=inputs)
