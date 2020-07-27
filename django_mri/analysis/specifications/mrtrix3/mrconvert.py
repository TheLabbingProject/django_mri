"""
Input and output specification dictionaries for MRtrix's *mrconvert* script.

See Also
--------
* `nipype.interfaces.mrtrix3.utils.MRConvert`_

Notes
-----
For more information, see MRtrix3's `mrconvert reference`_.

.. _mrconvert reference:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/mrconvert.html
.. _nipype.interfaces.mrtrix3.utils.MRConvert:
   https://nipype.readthedocs.io/en/1.5.0/api/generated/nipype.interfaces.mrtrix3.utils.html#mrconvert
"""

from django_analyses.models.input.definitions import (
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

#: *MRConvert* input specification dictionary.
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
        "description": "Specifies whether the b - values should be scaled by the square of the corresponding DW gradient norm, as often required for multishell or DSI DW acquisition schemes.",  # noqa: E501
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
        "description": "Dw gradient scheme (MRTrix format). Mutually exclusive with inputs: grad_fsl.",  # noqa: E501
    },
    "grad_fsl": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "(bvec, bval) DW gradient scheme (FSL format). Mutually exclusive with inputs: grad_file.",  # noqa: E501
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
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
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

#: *MRConvert* output specification dictionary.
MRCONVERT_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": NiftiOutputDefinition,
        "description": "The output converted image.",
    },
}
