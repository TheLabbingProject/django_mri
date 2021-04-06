"""
Input and output specification dictionaries for nipype's Reorient2Std_
interface, wrapping FSL's fslreorient2std_.

.. _fslreorient2std:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Fslutils?highlight=%28fslreorient2std%29
.. _Reorient2Std:
   https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.fsl.utils.html#reorient2std
"""

from django_analyses.models.input.definitions import (
    FileInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition

#: *Reorient2Std* input specification dictionary.
REORIENT2STD_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "description": "Path to NIfTI format image file to reorient.",
        "required": True,
        "is_configuration": False,
    },
    "args": {
        "type": StringInputDefinition,
        "description": "Additional parameters to the command.",
        "required": False,
    },
    "out_file": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Desired output file path.",
        "is_output_path": True,
        "default": "reoriented.nii.gz",
    },
    "output_type": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
        "is_configuration": False,
    },
}

#: *Reorient2Std* output specification dictionary.
REORIENT2STD_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "Reorient output file.",
    }
}
