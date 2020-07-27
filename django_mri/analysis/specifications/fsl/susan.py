"""
Input and output specification dictionaries for FSL's SUSAN_ script.

.. _SUSAN:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/SUSAN
"""


from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    StringInputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)


#: *SUSAN* input specification dictionary.
SUSAN_INPUT_SPECIFICATION = {
    "brightness_threshold": {
        "type": FloatInputDefinition,
        "required": True,
        "description": "Should be greater than noise level and less than contrast of edges to be preserved.",  # noqa: E501
    },
    "fwhm": {
        "type": FloatInputDefinition,
        "required": True,
        "description": "FWHM of smoothing, in millimeters.",
    },
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "Filename of input time-series.",
        "value_attribute": "path.__str__",
    },
    "dimension": {
        "type": IntegerInputDefinition,
        "required": False,
        "default": 3,
        "min_value": 2,
        "max_value": 3,
    },
    "out_file": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Desired output file path.",
        "is_output_path": True,
        "default": "smooth.nii.gz",
    },
    "output_type": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
    "use_median": {
        "type": BooleanInputDefinition,
        "required": False,
        "default": True,
        "description": "Whether to use a local median filter in the cases where single-point noise is detected.",  # noqa: E501
    },
    "args": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Additional parameters to pass to the command.",
    },
}


#: *SUSAN* output specification dictionary.
SUSAN_OUTPUT_SPECIFICATION = {
    "smoothed_file": {
        "type": NiftiOutputDefinition,
        "description": "Smoothed output file.",
    }
}
