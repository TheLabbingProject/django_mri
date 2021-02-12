"""
Input and output specification dictionaries for MRtrix's *5ttgen* script.

See Also
--------
* `nipype.interfaces.mrtrix3.utils.Generate5tt`_

Notes
-----
For more information, see MRtrix3's `5ttgen reference`_.

.. _dwi2response reference:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/5ttgen.html
.. _nipype.interfaces.mrtrix3.preprocess.ConstrainedSphericalDeconvolution:
    https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.mrtrix3.utils.html#generate5tt
"""
from django_analyses.models.input.definitions import (IntegerInputDefinition,
                                                      StringInputDefinition)
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition
from django_mri.models.outputs.nifti_output_definition import \
    NiftiOutputDefinition

GENERATE_5TT_INPUT_SPECIFICATION = {
    "algorithm": {
        "type": StringInputDefinition,
        "description": "Tissue segmentation algorithm.",
        "required": True,
        "choices": ["fsl", "gif", "freesurfer"],
        "default": "fsl",
    },
    "in_file": {
        "type": ScanInputDefinition,
        "description": "Input image.",
        "required": True,
        "is_configuration": False,
        "value_attribute": "nifti.path",
    },
    "out_file": {
        "type": StringInputDefinition,
        "description": "Path to output image.",
        "is_output_path": True,
        "default": "5tt.mif",
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
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
}

GENERATE_5TT_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": NiftiOutputDefinition,
        "description": "Output image.",
    },
}
