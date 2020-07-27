"""
Definition of the :class:`django_mri.utils.scan_type.ScanType` Enum.
"""

from enum import Enum


class ScanType(Enum):
    """
    Supported scan file formats.
    """

    DICOM = "DICOM"
    NIFTI = "NIfTI"
