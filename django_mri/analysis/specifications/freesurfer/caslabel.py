"""
Input and output specification dictionaries for FreeSurfer's mris_ca_label_ script.

.. _mris_ca_label:
   https://surfer.nmr.mgh.harvard.edu/fswiki/mris_ca_label
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

#: *mris_ca_label_* input specification.
CAS_LABEL_INPUT_SPECIFICATION = {
    "canonsurf": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input canonical surface file.",  # noqa: E501
        "is_configuration": False,
    },
    "classifier": {
        "type": FileInputDefinition,
        "description": "Classifier array input file.",  # noqa: E501
        "required": True,
    },
    "curv": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Implicit input {hemisphere}.curv.",
    },
    "hemisphere": {
        "type": StringInputDefinition,
        "choices": ["lh", "rh"],
        "required": True,
        "description": "Hemisphere (‘lh’ or ‘rh’).",  # noqa: E501
    },
    "smoothwm": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Implicit input {hemisphere}.smoothwm.",  # noqa: E501
    },
    "subject_id": {
        "type": StringInputDefinition,
        "required": True,
        "description": "Subject name or ID.",  # noqa: E501
    },
    "sulc": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Implicit input {hemisphere}.sulc.",  # noqa: E501
    },
    "aseg": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Undocumented flag. Autorecon3 uses ../mri/aseg.presurf.mgz as input file.",  # noqa: E501
    },
    "copy_inputs": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Copies implicit inputs to node directory and creates a temp subjects_directory.",
    },
    "label": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Undocumented flag. Autorecon3 uses ../label/{hemisphere}.cortex.label as input file.",
    },
    "out_file": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Annotated surface output file.",  # noqa: E501
    },
    "subjects_dir": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Subjects directory.",  # noqa: E501
    },
}

#: *mris_ca_label_* output specification.
CAS_LABEL_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "Output volume from MRIsCALabel.",
    },
}


# flake8: noqa: E501
