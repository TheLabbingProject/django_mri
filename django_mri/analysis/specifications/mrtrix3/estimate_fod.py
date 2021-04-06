"""
Input and output specification dictionaries for MRtrix's *dwi2fod* script.

See Also
--------
* `nipype.interfaces.mrtrix3.preprocess.ConstrainedSphericalDeconvolution`_

Notes
-----
For more information, see MRtrix3's `dwi2fod reference`_.

.. _dwi2fod reference:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/dwi2fod.html
.. _nipype.interfaces.mrtrix3.preprocess.ConstrainedSphericalDeconvolution:
    https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.mrtrix3.reconst.html#constrainedsphericaldeconvolution
"""
from django_analyses.models.input.definitions import (
    FileInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition

DWI2FOD_INPUT_SPECIFICATION = {
    "algorithm": {
        "type": StringInputDefinition,
        "description": "FOD algorithm.",
        "required": True,
        "choices": ["csd", "msmt_csd"],
    },
    "in_file": {
        "type": FileInputDefinition,
        "description": "Input DWI image.",
        "required": True,
        "is_configuration": False,
    },
    "wm_odf": {
        "type": StringInputDefinition,
        "description": "Output WM ODF.",
        "required": True,
        "is_output_path": True,
        "default": "wm_fod.mif",
    },
    "wm_txt": {
        "type": StringInputDefinition,
        "description": "WM response text.",
        "is_output_path": True,
        "default": "wm_fod.txt",
    },
    "csf_odf": {
        "type": StringInputDefinition,
        "description": "Output CSF ODF.",
        "is_output_path": True,
        "default": "csf_fod.mif",
    },
    "csf_txt": {
        "type": StringInputDefinition,
        "description": "CSF response text.",
        "is_output_path": True,
        "default": "csf_fod.txt",
    },
    "gm_odf": {
        "type": StringInputDefinition,
        "description": "Output GM ODF.",
        "is_output_path": True,
        "default": "csf_fod.mif",
    },
    "gm_txt": {
        "type": StringInputDefinition,
        "description": "GM response text.",
        "is_output_path": True,
        "default": "gm_fod.txt",
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
    "in_dirs": {
        "type": StringInputDefinition,
        "description": "pecify the directions over which to apply the non-negativity constraint (by default, the built-in 300 direction set is used). These should be supplied as a text file containing the [ az el ] pairs for the directions.",  # noqa: E501
    },
    "mask_file": {"type": StringInputDefinition, "description": "Mask image."},
    "max_sh": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "Maximum harmonic degree of response function - single value for single-shell response, list for multi-shell response.",  # noqa: E501
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
    "shell": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "Specify one or more dw gradient shells.",
    },
}

DWI2FOD_OUTPUT_SPECIFICATION = {
    "csf_odf": {
        "type": FileOutputDefinition,
        "description": "Output CSF ODF.",
    },
    "gm_odf": {"type": FileOutputDefinition, "description": "Output GM ODF."},
    "wm_odf": {"type": FileOutputDefinition, "description": "Output WM ODF."},
}
