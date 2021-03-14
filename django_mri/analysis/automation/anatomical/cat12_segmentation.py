"""
Definition of the :class:`Cat12SegmentationRunner` class.
"""
from django_mri.analysis.automation.anatomical import messages
from django_mri.analysis.automation.anatomical.preprocessing import (
    AnatomicalPreprocessing,
)


class Cat12SegmentationRunner(AnatomicalPreprocessing):
    """
    Automate CAT12 segmentation execution over a provided queryset of
    :class:`~django_mri.models.scan.Scan` instances.
    """

    #: CAT12 segmentation analysis title.
    ANALYSIS_TITLE = "CAT12 Segmentation"

    #: CAT12 segmentation analysis version title.
    ANALYSIS_VERSION_TITLE = "12.7"

    #: CAT12 segmentation configuration.
    ANALYSIS_CONFIGURATION = {
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

    #: Input definition key.
    INPUT_KEY = "path"

    #: The only required preprocessing is NIfTI coversion.
    PREPROCESSING_FAILURE: str = messages.NIFTI_CONVERSION_FAILURE
