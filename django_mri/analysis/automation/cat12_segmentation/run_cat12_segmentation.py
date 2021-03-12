"""
Utility functions facilitating batch CAT12 segmentation using celery.
"""
import warnings
from typing import Dict, List

from celery.result import AsyncResult
from django.db.models import QuerySet
from django_analyses.tasks import execute_node
from django_dicom.models.utils.progressbar import create_progressbar
from django_mri.analysis.automation.cat12_segmentation import messages
from django_mri.analysis.automation.cat12_segmentation.utils import (
    get_existing,
    get_missing,
    get_node,
)
from django_mri.analysis.automation.utils import get_t1_weighted
from django_mri.models.scan import Scan

# tqdm progressbar configuration.
_PROGRESSBAR_KWARGS = {"unit": "scan", "desc": "Preparing NIfTI file inputs"}


def create_input_specification(scan: Scan) -> dict:
    """
    Returns an input specification dictionary which will be used to run CAT12's
    segmentation node.

    Parameters
    ----------
    scan : Scan
        The anatomical scan to be segmented

    Returns
    -------
    dict
        Input specification dictionary
    """
    try:
        return {"path": str(scan.nifti.path)}
    # Report and skip scans that raise RuntimeError on NIfTI conversion.
    except RuntimeError:
        coversion_failure = messages.CONVERSION_FAILURE.format(scan_id=scan.id)
        print(coversion_failure)


def create_inputs(
    scans: QuerySet, progressbar: bool = True
) -> List[Dict[str, List[str]]]:
    """
    Returns a list of dictionary input specifications.

    Parameters
    ----------
    scans : QuerySet
        Batch of scans to run CAT12 segmentation on
    progressbar : bool, optional
        Whether to display a progressbar, by default True

    Returns
    -------
    List[Dict[str, List[str]]]
        Input specifications
    """
    iterable = create_progressbar(
        scans, disable=not progressbar, **_PROGRESSBAR_KWARGS
    )
    # Filter any scans with existing results from a user-provided queryset.
    existing = get_existing(scans)
    inputs = [
        create_input_specification(scan)
        for scan in iterable
        if scan not in existing
    ]
    # Report scans that could not be converted to NIfTI.
    n_invalid = inputs.count(None)
    if n_invalid:
        invalid_message = messages.INVALID_INPUTS.format(
            n_invalid=n_invalid, n_total=len(inputs)
        )
        warnings.warn(invalid_message)
    # Return `None`-filtered input specifications.
    return [
        specification for specification in inputs if specification is not None
    ]


def report_empty_inputs(queryset: QuerySet, db_run: bool) -> None:
    """
    Prints a message reporting an empty queryset of pending scans.

    Parameters
    ----------
    queryset : QuerySet
        Scans without CAT12 segmentation results
    db_run : bool
        Whether :func:`run_cat12_segmentation` was run over the entire
        anatomical dataset or not
    """
    if db_run:
        message = messages.NO_PENDING_ANATOMICALS
    else:
        message = messages.NO_PENDING_IN_QUERYSET.format(
            n_scans=queryset.count()
        )
    print(message)


def run_cat12_segmentation(
    queryset: QuerySet = None,
    max_total: int = None,
    prep_progressbar: bool = True,
) -> AsyncResult:
    """
    Run CAT12 segmentation on an entire anatomical queryset using celery. If no
    queryset is provided, queries all anatomical scans in the database.

    Parameters
    ----------
    queryset : QuerySet, optional
        Anatomical scans to be processed, by default None
    max_total : int, optional
        Maximal total number of scans to process, by default None
    prep_progressbar : bool, optional
        Whether to display a progerssbar to monitor the preparation of the
        required input specifications, by default True

    Returns
    -------
    celery.result.AsyncResult
        Created celery asynchronous result instance
    """
    # Modify/query T1-weighted queryset
    db_run = queryset is None
    queryset = get_missing() if db_run else queryset
    queryset = queryset[:max_total]
    # Generate input specifications and execute.
    if queryset:
        inputs = create_inputs(queryset, prep_progressbar)
        if inputs:
            node = get_node()
            return execute_node.delay(node_id=node.id, inputs=inputs)
        # Handle user-provided queryset with none pending.
        else:
            report_empty_inputs(queryset, db_run)
    # Report no T1-weighted scans found in the database.
    elif not get_t1_weighted():
        print(messages.NO_T1_WEIGHTED)
    # Handle default run over T1-weighted dataset with none pending.
    else:
        report_empty_inputs(queryset, db_run)
