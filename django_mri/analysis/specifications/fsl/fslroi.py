from django_analyses.models.input.definitions import (
    FloatInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
    BooleanInputDefinition,
    IntegerInputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import NiftiInputDefinition
from django_mri.models.outputs.nifti_output_definition import NiftiOutputDefinition

FSLROI_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "A NIfTI to extract an ROI from.",
        "is_configuration": False,
    },
    "crop_list": {
        "type": ListInputDefinition,
        "description": "list of two tuples specifying crop options.",
    },
    "ignore_exception": {
        "type": BooleanInputDefinition,
        "description": "Print an error message instead of throwing an exception in case the interface fails to run",
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
    "roi_file": {"type": StringInputDefinition, "description": "Path to output file."},
    "t_min": {"type": IntegerInputDefinition, "description": ""},
    "t_size": {"type": IntegerInputDefinition, "description": ""},
    "x_min": {"type": IntegerInputDefinition, "description": ""},
    "x_size": {"type": IntegerInputDefinition, "description": ""},
    "y_min": {"type": IntegerInputDefinition, "description": ""},
    "y_size": {"type": IntegerInputDefinition, "description": ""},
    "z_min": {"type": IntegerInputDefinition, "description": ""},
    "z_size": {"type": IntegerInputDefinition, "description": ""},
}
FSLROI_OUTPUT_SPECIFICATION = {
    "roi_file": NiftiOutputDefinition,
    "description": "Path to output file.",
}

