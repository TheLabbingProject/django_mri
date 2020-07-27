"""
Input and output specification dictionaries for MRtrix's *mrdegibbs* script.

See Also
--------
* `nipype.interfaces.mrtrix3.preprocess.MRDeGibbs`_

Notes
-----
For more information, see MRtrix3's `mrdegibbs reference`_.

.. _mrdegibbs reference:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/mrdegibbs.html
.. _nipype.interfaces.mrtrix3.preprocess.MRDeGibbs:
   https://nipype.readthedocs.io/en/1.4.1/api/generated/nipype.interfaces.mrtrix3.preprocess.html#mrdegibbs
"""

from django_analyses.models.input.definitions import (
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition


#: *MRDeGibbs* input specification.
DEGIBBS_INPUT_SPECIFICATION = {
    "in_file": {
        "type": ScanInputDefinition,
        "required": True,
        "is_configuration": False,
        "value_attribute": "mif.__str__",
    },
    "axes": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "Indicate the plane in which the data was acquired (axial = 0,1; coronal = 0,2; sagittal = 1,2).",  # noqa: E501
        "default": [0, 1],
    },
    "bval_scale": {
        "type": StringInputDefinition,
        "description": "Specifies whether the b - values should be scaled by the square of the corresponding DW gradient norm, as often required for multishell or DSI DW acquisition schemes.",  # noqa: E501
        "choices": ["yes", "no"],
        "default": "yes",
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
    "maxW": {
        "type": IntegerInputDefinition,
        "description": "Right border of window used for total variation (TV) computation.",  # noqa: E501
        "default": 3,
    },
    "minW": {
        "type": IntegerInputDefinition,
        "description": "Left border of window used for total variation (TV) computation.",  # noqa: E501
        "default": 1,
    },
    "nshifts": {
        "type": IntegerInputDefinition,
        "description": "Discretization of subpixel spacing.",
        "default": 20,
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

#: *MRDeGibbs* output specification.
DEGIBBS_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "The output denoised DWI image.",
    },
}
