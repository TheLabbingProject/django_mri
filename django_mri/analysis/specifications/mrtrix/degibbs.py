from django_analyses.models.input.definitions import (
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)

from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    ListOutputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

DEGIBBS_INPUT_SPECIFICATION = {
    "in_file": {
        "type": ScanInputDefinition,
        "required": True,
        "description": "Input DWI image.",
        "is_configuration": False,
        "value_attribute": "mif.__str__",
    },
    "axes": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "Indicate the plane in which the data was acquired (axial = 0,1; coronal = 0,2; sagittal = 1,2).",
        "default": [0, 1],
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
    "maxW": {
        "type": IntegerInputDefinition,
        "description": "Right border of window used for total variation (TV) computation.",
        "default": 3,
    },
    "minW": {
        "type": IntegerInputDefinition,
        "description": "Left border of window used for total variation (TV) computation.",
        "default": 1,
    },
    "nshifts": {
        "type": IntegerInputDefinition,
        "description": "Discretization of subpixel spacing.",
        "default": 20,
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",
    },
    "out_file": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output denoised DWI image.",
        "default": "denoised.nii.gz",
    },
}

DEGIBBS_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "The output denoised DWI image.",
    },
}

