"""
Input and output specification dictionaries for nipype's MeanImage_ interface,
wrapping FSL's fslmaths_.

.. _fslmaths:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Fslutils?highlight=(fslmaths)
.. _MeanImage:
   https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.fsl.maths.html#meanimage
"""

from django_analyses.models.input.definitions import (BooleanInputDefinition,
                                                      FileInputDefinition,
                                                      StringInputDefinition)
from django_analyses.models.output.definitions import FileOutputDefinition

#: *MeanImage* input specification dictionary.
MEAN_IMAGE_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "description": "Path to image to operate on.",
        "required": True,
        "is_configuration": False,
    },
    "dimension": {
        "type": StringInputDefinition,
        "required": True,
        "description": "Dimension along which to merge, optionally set TR inputs when dimension is 'T'",  # noqa: E501
        "choices": ["T", "X", "Y", "Z"],
    },
    "internal_datatype": {
        "type": StringInputDefinition,
        "description": "Datatype to use for calculations.",
        "choices": ["float", "char", "int", "short", "double", "input"],
        "default": "float",
    },
    "nan2zero": {
        "type": BooleanInputDefinition,
        "description": "Change NaNs to zeros before doing anything.",
    },
    "out_file": {
        "type": StringInputDefinition,
        "default": "mean.nii.gz",
        "description": "Path to image to write results to.",
    },
    "output_datatype": {
        "type": StringInputDefinition,
        "description": "Datatype to use for output (default uses input type).",
        "choices": ["float", "char", "int", "short", "double", "input"],
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
}

#: *MeanImage* output specification dictionary.
MEAN_IMAGE_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "Path to image containing calculation's result.",
    }
}
