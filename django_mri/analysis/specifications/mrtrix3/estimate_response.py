"""
Input and output specification dictionaries for MRtrix's *dwi2response* script.

See Also
--------
* `nipype.interfaces.mrtrix3.preprocess.ResponseSD`_

Notes
-----
For more information, see MRtrix3's `dwi2response reference`_.

.. _dwi2response reference:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/dwi2response.html
.. _nipype.interfaces.mrtrix3.preprocess.ConstrainedSphericalDeconvolution:
    https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.mrtrix3.preprocess.html#responsesd
"""
from django_analyses.models.input.definitions import (
    FileInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition

DWI2RESPONSE_INPUT_SPECIFICATION = {
    "algorithm": {
        "type": StringInputDefinition,
        "description": "Response estimation algorithm (multi-tissue)",
        "required": True,
        "choices": ["msmt_5tt", "dhollander", "tournier", "tax"],
    },
    "in_file": {
        "type": FileInputDefinition,
        "description": "Input DWI image.",
        "required": True,
        "is_configuration": False,
    },
    "bval_scale": {
        "type": StringInputDefinition,
        "description": "Specifies whether the b - values should be scaled by the square of the corresponding DW gradient norm, as often required for multishell or DSI DW acquisition schemes.",  # noqa: E501
        "choices": ["yes", "no"],
        "default": "yes",
    },
    "wm_file": {
        "type": StringInputDefinition,
        "description": "Output WM response text file.",
        "is_output_path": True,
        "default": "wm_response.txt",
    },
    "csf_file": {
        "type": StringInputDefinition,
        "description": "Output CSF response text file.",
        "is_output_path": True,
        "default": "csf_response.txt",
    },
    "gm_file": {
        "type": StringInputDefinition,
        "description": "Output GM response text file.",
        "is_output_path": True,
        "default": "gm_response.txt",
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
    "in_mask": {"type": StringInputDefinition, "description": "Mask image."},
    "max_sh": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "Maximum harmonic degree of response function - single value for single-shell response, list for multi-shell response.",  # noqa: E501
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
    "mtt_file": {
        "type": FileInputDefinition,
        "description": "Input 5tt image.",
    },
}

DWI2RESPONSE_OUTPUT_SPECIFICATION = {
    "csf_file": {
        "type": FileOutputDefinition,
        "description": "Output CSF response text file.",
    },
    "gm_file": {
        "type": FileOutputDefinition,
        "description": "Output WM response text file.",
    },
    "wm_file": {
        "type": FileOutputDefinition,
        "description": "Output WM response text file.",
    },
}
