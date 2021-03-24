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
    FileInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition

#: *MRConvert* input specification dictionary.
MRCONVERT_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input DWI image.",
        "is_configuration": False,
    },
    "out_file": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output converted image.",
        "default": "converted.mif",
    },
    "coord": {
        "type": StringInputDefinition,
        "description": "extract data at the specified coordinates",
    },
    "vox": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "Change the voxel dimensions.",
    },
    "axes": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "specify the axes that will be used",
    },
    "scaling": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "specify the data scaling parameters used to rescale the intensity values.",
    },
    "json_import": {
        "type": FileInputDefinition,
        "description": "import data from a JSON file into header key-value pairs",
    },
    "json_export": {
        "type": StringInputDefinition,
        "description": "export data from an image header key-value pairs into a JSON file",
        "is_output_path": True,
    },
    "clear_property": {
        "type": StringInputDefinition,
        "description": "remove the specified key from the image header altogether.",
    },
    "set_property": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "set the value of the specified key in the image header.",
    },
    "append_property": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "append the given value to the specified key in the image header (this adds the value specified as a new line in the header value).",
    },
    "strides": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": " specify the strides of the output data in memory;",
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
    "grad": {
        "type": FileInputDefinition,
        "description": "Dw gradient scheme (MRTrix format). Mutually exclusive with inputs: grad_fsl.",
    },
    "fslgrad": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "(bvec, bval) DW gradient scheme (FSL format). Mutually exclusive with inputs: grad_file.",
    },
    "bvalue_scaling": {
        "type": StringInputDefinition,
        "description": "Specifies whether the b - values should be scaled by the square of the corresponding DW gradient norm, as often required for multishell or DSI DW acquisition schemes.",
        "choices": ["yes", "no"],
    },
    "export_grad_mrtrix": {
        "type": StringInputDefinition,
        "description": "export the diffusion-weighted gradient table to file in MRtrix format",
        "is_output_path": True,
    },
    "export_grad_fsl": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "export the diffusion-weighted gradient table to files in FSL (bvecs / bvals) format",
    },
    "import_pe_table": {
        "type": FileInputDefinition,
        "description": "import a phase-encoding table from file",
    },
    "import_pe_table": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "import phase-encoding information from an EDDY-style config / index file pair",
    },
    "export_pe_table": {
        "type": StringInputDefinition,
        "description": "export a phase-encoding table to a file",
        "is_output_path": True,
    },
    "export_pe_eddy": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "export phase-encoding information to an EDDY-style config / index file pair",
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",
    },
}

#: *MRConvert* output specification dictionary.
MRCONVERT_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "The output converted image.",
    },
}


# flake8: noqa: E501
