"""
Input and output specification dictionaries for FSL's fslmerge_ script.

.. _fslmerge:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/fslmerge
"""

from django_analyses.models.input.definitions import (
    FloatInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)


#: *fslmerge* input specification dictionary.
FSLMERGE_INPUT_SPECIFICATION = {
    "in_files": {
        "type": ListInputDefinition,
        "required": True,
        "description": "A list of (at least 2) NIfTI format files to merge.",
        "is_configuration": False,
        "element_type": "FIL",
        "db_value_preprocessing": "path.__str__",
    },
    "dimension": {
        "type": StringInputDefinition,
        "required": True,
        "description": "Dimension along which to merge, optionally set tr inputs when dimension is 't'.",  # noqa: E501
        "choices": ["t", "x", "y", "z", "a"],
    },
    "merged_file": {
        "type": StringInputDefinition,
        "description": "Desired output file path.",
        "is_output_path": True,
        "default": "merged.nii.gz",
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
    "tr": {
        "type": FloatInputDefinition,
        "description": "Specified TR in seconds.",
        "default": 1.0,
    },
}

#: *fslmerge* output specification dictionary.
FSLMERGE_OUTPUT_SPECIFICATION = {
    "merged_file": {
        "type": NiftiOutputDefinition,
        "description": "Path of merged file",
    }
}
