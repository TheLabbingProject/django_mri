"""
Utilties for CAT12 segmentation automation.
"""

from pathlib import Path

import nibabel as nib
import numpy as np
from django.db.models import QuerySet
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.definitions.input_definition import (
    InputDefinition,
)
from django_analyses.models.pipeline.node import Node
from django_mri.analysis.automation.utils import get_t1_weighted
from django_mri.models.scan import Scan

#: :class:`~django_analyses.models.analysis.Analysis` instance title.
TITLE = "CAT12 Segmentation"

#: :class:`~django_analyses.models.pipeline.node.Node` instance configuration.
CONFIGURATION = {
    "cobra": True,
    "lpba40": True,
    "hammers": True,
    "native_grey_matter": True,
    "surface_estimation": True,
    "native_white_matter": True,
    "jacobian_determinant": True,
    "dartel_grey_matter": True,
    "dartel_white_matter": True,
    "modulated_grey_matter": True,
    "modulated_white_matter": True,
    "warped_image": True,
    "neuromorphometrics": True,
    "native_pve": True,
}


def get_cat_version() -> AnalysisVersion:
    """
    Returns the latest version of CAT12 segmentation.

    Returns
    -------
    AnalysisVersion
        Latest CAT12 segmentation version
    """
    return AnalysisVersion.objects.filter(analysis__title=TITLE).first()


def get_input_definition() -> InputDefinition:
    """
    Returns the
    :class:`~django_analyses.models.input.definitions.file_input_definition.FileInputDefinition`
    instance associated with CAT12 segmentation's input file.

    Returns
    -------
    InputDefinition
        CAT12 segmentation's input file definition instance
    """
    cat_version = get_cat_version()
    return cat_version.input_definitions.get(key="path")


def get_node() -> Node:
    """
    Returns the default CAT12 segmentation node.

    Returns
    -------
    Node
        Default CAT12 segmentation version and configuration
    """
    cat_version = get_cat_version()
    return Node.objects.get_or_create(
        analysis_version=cat_version, configuration=CONFIGURATION
    )[0]


def get_existing(anatomicals: QuerySet) -> QuerySet:
    """
    Returns a queryset of scans detected as anatomical and not having existing
    results for the default CAT12 segmentation node.

    Returns
    -------
    QuerySet
        Pending anatomical scans to be processed
    """
    input_definition = get_input_definition()
    scan_ids = [
        scan.id
        for scan in anatomicals
        if scan._nifti
        and input_definition.input_set.filter(value=scan.nifti.path)
    ]
    return Scan.objects.filter(id__in=scan_ids)


def get_missing() -> QuerySet:
    """
    Returns a queryset of scans detected as anatomical and not having existing
    results for the default CAT12 segmentation node.

    Returns
    -------
    QuerySet
        Pending anatomical scans to be processed
    """
    anatomicals = get_t1_weighted()
    existing = get_existing(anatomicals)
    return anatomicals.exclude(id__in=existing)


def get_run_set() -> QuerySet:
    """
    Returns a queryset of existing (successful) CAT12 segmentation runs.

    Returns
    -------
    QuerySet
        Existing CAT12 segmentation runs
    """
    return get_node().run_set.filter(status="SUCCESS")


def read_nifti(path: Path) -> np.ndarray:
    return np.asarray(nib.load(str(path)).dataobj)
    # return np.nan_to_num(data.flatten())
