"""
Input and output specification dictionaries for FreeSurfer's mri_ca_label_ script.

.. _mri_ca_label:
   https://surfer.nmr.mgh.harvard.edu/fswiki/mri_ca_label
"""

from django.conf import settings
from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    DirectoryInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    ListOutputDefinition,
)

#: *mri_ca_label_* input specification.
CA_LABEL_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": " Input volume for CALabel.",  # noqa: E501
        "is_configuration": False,
    },
    "out_file": {
        "type": FileInputDefinition,
        "description": "Output file for CALabel.",  # noqa: E501
        "required": True,
    },
    "template": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input template for CALabel. ",
    },
    "transform": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input transform for CALabel. ",  # noqa: E501
    },
    "align": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": " Align CALabel.",  # noqa: E501
    },
    "aseg": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Undocumented flag. Autorecon3 uses ../mri/aseg.presurf.mgz as input file. ",  # noqa: E501
    },
    "in_vol": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Set input volume.",  # noqa: E501
    },
    "intensities": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Input label intensities file(used in longitudinal processing).",  # noqa: E501
    },
    "label": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Undocumented flag. Autorecon3 uses ../label/{hemisphere}.cortex.label as input file.",
    },
    "no_big_ventricles": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "No big ventricles.",  # noqa: E501
    },
    "prior": {
        "type": FloatInputDefinition,
        "required": False,
        "description": "Prior for CALabel.",  # noqa: E501
    },
    "subjects_dir": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Subjects directory.",  # noqa: E501
    },
}

#: *mri_ca_label_* output specification.
CA_LABEL_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "Output volume from CALabel.",
    },
}


# flake8: noqa: E501
