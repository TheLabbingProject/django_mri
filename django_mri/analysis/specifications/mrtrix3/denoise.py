"""
Input and output specification dictionaries for MRtrix's *dwidenoise* script.

See Also
--------
* `nipype.interfaces.mrtrix3.preprocess.DWIDenoise`_

Notes
-----
For more information, see MRtrix3's `dwidenoise reference`_.

.. _dwidenoise reference:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/dwidenoise.html
.. _nipype.interfaces.mrtrix3.preprocess.DWIDenoise:
   https://nipype.readthedocs.io/en/1.4.1/api/generated/nipype.interfaces.mrtrix3.preprocess.html#dwidenoise
"""

from django_analyses.models.input.definitions import (
    FileInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition


DENOISE_INPUT_SPECIFICATION = {
    "in_file": {
        "type": ScanInputDefinition,
        "required": True,
        "is_configuration": False,
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
        "description": "Set the window size of the denoising filter.",
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
    "mask": {"type": FileInputDefinition, "description": "Mask image."},
    "noise": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output noise map.",
        "default": "noise.mif",
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
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
