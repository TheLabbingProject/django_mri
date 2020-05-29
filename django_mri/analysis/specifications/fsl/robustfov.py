from django_analyses.models.input.definitions import (
    IntegerInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import NiftiInputDefinition
from django_mri.models.outputs.nifti_output_definition import NiftiOutputDefinition


ROBUSTFOV_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "description": "Path to NIfTI format image file to crop.",
        "value_attribute": "path.__str__",
        "required": True,
    },
    "args": {
        "type": StringInputDefinition,
        "description": "Additional parameters to the command.",
        "required": False,
    },
    "brainsize": {
        "type": IntegerInputDefinition,
        "description": "Size of brain (in millimiteres) in the z-dimension.",
        "default": 170,
        "required": False,
    },
    "out_roi": {
        "type": StringInputDefinition,
        "required": False,
        "description": "ROI volume output file path.",
        "is_output_path": True,
        "default": "roi.nii.gz",
    },
    "out_transform": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Tranformation matrix output file path.",
        "is_output_path": True,
        "default": "transform",
    },
    "output_type": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
}

ROBUSTFOV_OUTPUT_SPECIFICATION = {
    "out_roi": {"type": NiftiOutputDefinition, "description": "ROI volume."},
    "out_transform": {
        "type": FileOutputDefinition,
        "description": "Transformation matrix in_file to out_roi output name.",
    },
}
