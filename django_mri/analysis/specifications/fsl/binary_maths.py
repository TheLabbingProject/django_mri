"""
Input and output specification dictionaries for nipype's BinaryMaths_
interface, wrapping FSL's fslmaths_.

.. _fslmaths:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Fslutils?highlight=(fslmaths)
.. _BinaryMaths:
   https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.fsl.maths.html#binarymaths
"""

from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FloatInputDefinition,
    StringInputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)


#: *BinaryMaths* input specification dictionary.
BINARY_MATHS_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "description": "Path to image to operate on.",
        "required": True,
        "is_configuration": False,
        "value_attribute": "path.__str__",
    },
    "operand_file": {
        "type": NiftiInputDefinition,
        "description": "Path to second image to perform operation with. Mutually exclusive with inputs: operand_value.",  # noqa: E501
    },
    "operand_value": {
        "type": FloatInputDefinition,
        "description": "Value to perform operation with.",
    },
    "operation": {
        "type": StringInputDefinition,
        "description": "Operation to perform.",
        "required": True,
        "choices": ["add", "sub", "mul", "div", "rem", "max", "min"],
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
        "default": "math_out.nii.gz",
        "is_output_path": True,
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

#: *BinaryMaths* input specification dictionary.
BINARY_MATHS_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": NiftiOutputDefinition,
        "description": "Path to image containing calculation's result.",
    }
}
