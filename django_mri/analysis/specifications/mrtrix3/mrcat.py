"""
Input and output specification dictionaries for MRtrix's *mrcat* script.


Notes
-----
For more information, see MRtrix3's `mrcat reference`_.

.. _mrconvert reference:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/mrcat.html
"""

from django_analyses.models.input.definitions import (
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
    FileInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import NiftiInputDefinition
from django_mri.models.outputs.nifti_output_definition import NiftiOutputDefinition

#: *MRCat* input specification dictionary.
MRCAT_INPUT_SPECIFICATION = {
    "in_files": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "required": True,
        "description": "Input images.",
        "is_configuration": False,
    },
    "out_file": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output denoised DWI image.",
        "default": "concatenated.mif",
    },
    "axis": {
        "type": IntegerInputDefinition,
        "description": "specify axis along which concatenation should be performed.",
    },
    "datatype": {
        "type": StringInputDefinition,
        "description": "specify output image data type.",
        "choices": [
            "float32",
            "float32le",
            "float32be",
            "float64",
            "float64le",
            "float64be",
            "int64",
            "uint64",
            "int64le",
            "uint64le",
            "int64be",
            "uint64be",
            "int32",
            "uint32",
            "int32le",
            "uint32le",
            "int32be",
            "uint32be",
            "int16",
            "uint16",
            "int16le",
            "uint16le",
            "int16be",
            "uint16be",
            "cfloat32",
            "cfloat32le",
            "cfloat32be",
            "cfloat64",
            "cfloat64le",
            "cfloat64be",
            "int8",
            "uint8",
            "bit",
        ],
    },
}

#: *MRCat* output specification dictionary.
MRCAT_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "The output concatenated image.",
    },
}
