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
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

MRCONVERT_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "Input DWI image.",
        "is_configuration": False,
    },
    "out_file": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output denoised DWI image.",
        "default": "denoised.nii.gz",
    },
    "axes": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "specify the axes that will be used",
    },
    "bval_scale": {
        "type": StringInputDefinition,
        "description": "Specifies whether the b - values should be scaled by the square of the corresponding DW gradient norm, as often required for multishell or DSI DW acquisition schemes.",
        "choices": ["yes", "no"],
        "default": "yes",
    },
    "coord": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "extract data at the specified coordinates",
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
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",
    },
    "scaling": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "specify the data scaling parameter",
    },
    "vox": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "Change the voxel dimensions.",
    },
}

MRCONVERT_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": NiftiOutputDefinition,
        "description": "The output converted image.",
    },
}

