from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)

from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import NiftiInputDefinition
from django_mri.models.outputs.nifti_output_definition import NiftiOutputDefinition

MEAN_IMAGE_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "description": "Path to image to operate on.",
        "required": True,
        "is_configuration": False,
        "value_attribute": "path.__str__",
    },
    "dimension": {
        "type": StringInputDefinition,
        "required": True,
        "description": "Dimension along which to merge, optionally set tr inputs when dimension is 't'",
        "choices": ["t", "x", "y", "z", "a"],
    },
    "internal_datatype": {
        "type": StringInputDefinition,
        "description": "Datatype to use for calculations.",
        "choices": ["float", "char", "int", "short", "double", "input"],
        "default": "float",
    },
    "nan2zero": {
        "type": BooleanInputDefinition,
        "description": "Change NaNs to zeros before doing anything.",
    },
    "out_file": {
        "type": StringInputDefinition,
        "description": "Path to image to write results to.",
    },
    "output_datatype": {
        "type": StringInputDefinition,
        "description": "Datatype to use for output (default uses input type).",
        "choices": ["float", "char", "int", "short", "double", "input"],
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
}
MEAN_IMAGE_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": NiftiOutputDefinition,
        "description": "Path to image containing calculation's result.",
    }
}
