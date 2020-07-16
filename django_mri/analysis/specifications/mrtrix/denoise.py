from django_analyses.models.input.definitions import (
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition


DENOISE_INPUT_SPECIFICATION = {
    "in_file": {
        "type": ScanInputDefinition,
        "required": True,
        "is_configuration": False,
        "description": "Input DWI image.",
        "value_attribute": "mif.__str__",
    },
    "bval_scale": {
        "type": StringInputDefinition,
        "description": "Specifies whether the b - values should be scaled by the square of the corresponding DW gradient norm, as often required for multishell or DSI DW acquisition schemes.",  # noqa: E501
        "choices": ["yes", "no"],
        "default": "yes",
    },
    "extent": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "Set the window size of the denoising filter.",  # noqa: E501
        "default": [5.0, 5.0, 5.0],
    },
    "grad_file": {
        "type": StringInputDefinition,
        "description": "Dw gradient scheme (MRTrix format). Mutually exclusive with inputs: grad_fsl.",  # noqa: E501
    },
    "grad_fsl": {
        "type": StringInputDefinition,
        "description": "dw gradient scheme (FSL format). Mutually exclusive with inputs: grad_file.",  # noqa: E501
    },
    "in_bval": {
        "type": StringInputDefinition,
        "description": "Bvals file in FSL format.",
    },
    "in_bvec": {
        "type": StringInputDefinition,
        "description": "Bvecs file in FSL format.",
    },
    "mask": {
        "type": NiftiInputDefinition,
        "description": "Mask image.",
        "value_attribute": "path.__str__",
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
    "noise": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output noise map.",
        "default": "noise.mif",
    },
    "out_file": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output denoised DWI image.",
        "default": "denoised.mif",
    },
}

DENOISE_OUTPUT_SPECIFICATION = {
    "noise": {
        "type": FileOutputDefinition,
        "description": "The output noise map.",
    },
    "out_file": {
        "type": FileOutputDefinition,
        "description": "The output denoised DWI image.",
    },
}
