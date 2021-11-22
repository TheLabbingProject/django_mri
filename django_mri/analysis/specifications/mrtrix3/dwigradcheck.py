"""
Input and output specification dictionaries for MRtrix's *dwigradcheck* script.

Notes
-----
For more information, see MRtrix3's `dwigradcheck reference`_.

.. _mrconvert reference:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/dwigradcheck.html
"""

from django_analyses.models.input.definitions import (FileInputDefinition,
                                                      IntegerInputDefinition,
                                                      ListInputDefinition,
                                                      StringInputDefinition)
from django_analyses.models.output.definitions import FileOutputDefinition

#: *dwigradcheck* input specification dictionary.
DWIGRADCHECK_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input DWI image.",
        "is_configuration": False,
    },
    "mask": {
        "type": FileInputDefinition,
        "description": "Provide a brain mask image.",
    },
    "number": {
        "type": IntegerInputDefinition,
        "description": "Set the number of tracks to generate for each test.",
    },
    "grad": {
        "type": FileInputDefinition,
        "description": "Dw gradient scheme (MRTrix format). Mutually exclusive with inputs: grad_fsl.",  # noqa: E501
    },
    "fslgrad": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "(bvec, bval) DW gradient scheme (FSL format). Mutually exclusive with inputs: grad_file.",  # noqa: E501
    },
    "export_grad_mrtrix": {
        "type": StringInputDefinition,
        "description": "export the diffusion-weighted gradient table to file in MRtrix format",
        "is_output_path": True,
    },
    "export_fsl_bvec": {
        "type": StringInputDefinition,
        "description": "Export the diffusion-weighted gradient b-vector in FSL format",
        "is_output_path": True,
        "default": "dwi.bvec",
    },
    "export_fsl_bval": {
        "type": StringInputDefinition,
        "description": "Export the diffusion-weighted gradient b-value in FSL format",
        "is_output_path": True,
        "default": "dwi.bval",
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
}

#: *MRConvert* output specification dictionary.
DWIGRADCHECK_OUTPUT_SPECIFICATION = {
    "grad_fsl_bvec": {
        "type": FileOutputDefinition,
        "description": "The final gradient b-vector file in FSL format.",
    },
    "grad_fsl_bval": {
        "type": FileOutputDefinition,
        "description": "The final gradient b-value file in FSL format.",
    },
    "grad_mrtrix": {
        "type": FileOutputDefinition,
        "description": "The final gradient table in MRtrix format",
    },
}
