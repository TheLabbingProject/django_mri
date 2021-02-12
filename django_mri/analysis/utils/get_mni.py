"""
Definition of the :func:`get_mni` utility function.
"""

from pathlib import Path

from django_mri.models.nifti import NIfTI

MNI_TEMPLATE_PATH = (
    Path(__file__).parent.parent.parent
    / "utils"
    / "atlases"
    / "MNI152_T1_2mm_brain.nii.gz"
)


def get_mni() -> NIfTI:
    return NIfTI.objects.get_or_create(path=MNI_TEMPLATE_PATH)[0]
