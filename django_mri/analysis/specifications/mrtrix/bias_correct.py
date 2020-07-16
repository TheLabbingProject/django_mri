from django_analyses.models.input.definitions import (
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
    BooleanInputDefinition,
)

from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    ListOutputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import NiftiInputDefinition
from django_mri.models.outputs.nifti_output_definition import NiftiOutputDefinition

BIAS_CORRECT_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "Input DWI image.",
        "is_configuration": False,
    },
    "use_ants": {
        "type": BooleanInputDefinition,
        "description": "Use ANTS N4 to estimate the inhomogeneity field. Mutually exclusive with inputs: use_fsl.",
    },
    "use_fsl": {
        "type": BooleanInputDefinition,
        "description": "Use FSL FAST to estimate the inhomogeneity field. Mutually exclusive with inputs: use_ants.",
    },
    "bias": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output noise map.",
        "default": "bias.nii.gz",
    },
    "bval_scale": {
        "type": StringInputDefinition,
        "description": "Specifies whether the b - values should be scaled by the square of the corresponding DW gradient norm, as often required for multishell or DSI DW acquisition schemes.",
        "choices": ["yes", "no"],
        "default": "yes",
    },
    "grad_file": {
        "type": StringInputDefinition,
        "description": "Dw gradient scheme (MRTrix format). Mutually exclusive with inputs: grad_fsl.",
    },
    "grad_fsl": {
        "type": StringInputDefinition,
        "description": "dw gradient scheme (FSL format). Mutually exclusive with inputs: grad_file.",
    },
    "in_bval": {
        "type": StringInputDefinition,
        "description": "Bvals file in FSL format.",
    },
    "in_bvec": {
        "type": StringInputDefinition,
        "description": "Bvecs file in FSL format.",
    },
    "in_mask": {
        "type": NiftiInputDefinition,  ########## Check with Zvi - Nifti or String #########
        "description": "Mask image.",
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",
    },
    "out_file": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output denoised DWI image.",
        "default": "bias_corrected.nii.gz",
    },
}

BIAS_CORRECT_OUTPUT_SPECIFICATION = {
    "bias": {"type": NiftiOutputDefinition, "description": "The output bias field."},
    "out_file": {
        "type": NiftiOutputDefinition,
        "description": "The output denoised DWI image.",
    },
}

