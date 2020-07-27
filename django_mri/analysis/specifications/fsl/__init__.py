"""
Input and output specification dicationaries for FSL_ analyses.

.. _FSL:
   https://fsl.fmrib.ox.ac.uk/
"""


from django_mri.analysis.specifications.fsl.bet import (
    BET_INPUT_SPECIFICATION,
    BET_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.flirt import (
    FLIRT_INPUT_SPECIFICATION,
    FLIRT_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.fnirt import (
    FNIRT_INPUT_SPECIFICATION,
    FNIRT_OUTPUT_SPECIFICATION,
)
