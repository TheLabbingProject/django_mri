"""
Input and output specification dictionaries for FSL's fslroi_ script.

.. _fslroi:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/fslroi
"""

from django_analyses.models.input.definitions import (
    ListInputDefinition,
    StringInputDefinition,
    BooleanInputDefinition,
    IntegerInputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

#: *fslroi* input specification dictionary.
FSLROI_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "A NIfTI to extract an ROI from.",
        "is_configuration": False,
        "value_attribute": "path.__str__",
    },
    "crop_list": {
        "type": ListInputDefinition,
        "element_type": "TUP",
        "description": "list of two tuples specifying crop options.",
    },
    "ignore_exception": {
        "type": BooleanInputDefinition,
        "description": "Print an error message instead of throwing an exception in case the interface fails to run",  # noqa: E501
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
    "roi_file": {
        "type": StringInputDefinition,
        "description": "Path to output file.",
        "default": "roi.nii.gz",
        "is_output_path": True,
    },
    "t_min": {"type": IntegerInputDefinition, "description": ""},
    "t_size": {"type": IntegerInputDefinition, "description": ""},
    "x_min": {"type": IntegerInputDefinition, "description": ""},
    "x_size": {"type": IntegerInputDefinition, "description": ""},
    "y_min": {"type": IntegerInputDefinition, "description": ""},
    "y_size": {"type": IntegerInputDefinition, "description": ""},
    "z_min": {"type": IntegerInputDefinition, "description": ""},
    "z_size": {"type": IntegerInputDefinition, "description": ""},
}

#: *fslroi* output specification dictionary.
FSLROI_OUTPUT_SPECIFICATION = {
    "roi_file": {
        "type": NiftiOutputDefinition,
        "description": "Path to output file.",
    },
}
