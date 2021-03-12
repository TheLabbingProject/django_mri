from pathlib import Path

import nibabel as nib
import numpy as np
from django.db.models import QuerySet
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.definitions.input_definition import (
    InputDefinition,
)
from django_analyses.models.pipeline.node import Node
from django_mri.analysis.automation.utils import get_anatomicals

TITLE = "CAT12 Segmentation"
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
    return AnalysisVersion.objects.filter(analysis__title=TITLE).first()


def get_input_definition() -> InputDefinition:
    cat_version = get_cat_version()
    return cat_version.input_definitions.get(key="path")


def get_node() -> Node:
    cat_version = get_cat_version()
    return Node.objects.get_or_create(
        analysis_version=cat_version, configuration=CONFIGURATION
    )[0]


def get_missing() -> QuerySet:
    anatomicals = get_anatomicals()
    input_definition = get_input_definition()
    existing = [
        scan.id
        for scan in anatomicals
        if scan._nifti
        and input_definition.input_set.filter(value=scan.nifti.path)
    ]
    return anatomicals.exclude(id__in=existing)


def get_run_set() -> QuerySet:
    return get_node().run_set.filter(status="SUCCESS")


def read_nifti(path: Path) -> np.ndarray:
    return np.asarray(nib.load(str(path)).dataobj)
    # return np.nan_to_num(data.flatten())
