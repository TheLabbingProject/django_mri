"""
Input and output specification dictionaries for FreeSurfer's mris_anatomical_stats_ script.

.. _mris_anatomical_stats:
   https://surfer.nmr.mgh.harvard.edu/fswiki/mris_anatomical_stats
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

#: *mris_anatomical_stats_* input specification.
PARCELLATION_STATS_INPUT_SPECIFICATION = {
    "aseg": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Undocumented flag. Autorecon3 uses ../mri/aseg.presurf.mgz as input file.",  # noqa: E501
    },
    "brainmask": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/mri/brainmask.mgz.",  # noqa: E501
    },
    "hemisphere": {
        "type": StringInputDefinition,
        "choices": ["lh", "rh"],
        "required": True,
        "description": "Hemisphere (‘lh’ or ‘rh’).",  # noqa: E501
    },
    "lh_pial": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/surf/lh.pial.",  # noqa: E501
    },
    "lh_white": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/surf/lh.white.",  # noqa: E501
    },
    "rh_pial": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/surf/rh.pial.",  # noqa: E501
    },
    "rh_white": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/surf/rh.white.",  # noqa: E501
    },
    "ribbon": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/mri/ribbon.mgz.",  # noqa: E501
    },
    "subject_id": {
        "type": StringInputDefinition,
        "required": True,
        "description": "Subject name or ID.",  # noqa: E501
    },
    "thickness": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/surf/?h.thickness.",  # noqa: E501
    },
    "transform": {
        "type": BooleanInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/mri/transforms/talairach.xfm.",
    },
    "wm": {
        "type": BooleanInputDefinition,
        "required": True,
        "description": "Input file must be <subject_id>/mri/wm.mgz.",
    },
    "copy_inputs": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Copies implicit inputs to node directory and creates a temp subjects_directory.",
    },
    "cortex_label": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Implicit input file {hemi}.cortex.label.",
    },
    "in_annotation": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Compute properties for each label in the annotation file separately.",
    },
    "in_cortex": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Input cortex label.",
    },
    "in_label": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Limit calculations to specified label.",
    },
    "mgz": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Look for mgz files.",  # noqa: E501
    },
    "out_color": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Output annotation files’s colortable to text file.",  # noqa: E501
    },
    "out_table": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Table output to tablefile.",  # noqa: E501
    },
    "subjects_dir": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Subjects directory.",  # noqa: E501
    },
    "tabular_output": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Tabular output.",  # noqa: E501
    },
    "ths3": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Turns on new vertex-wise volume calc for mris_anat_stats.",  # noqa: E501
    },
}

#: *mris_anatomical_stats_* output specification.
PARCELLATION_STATS_OUTPUT_SPECIFICATION = {
    "out_color": {
        "type": FileOutputDefinition,
        "description": "Output annotation files’s colortable to text file.",
    },
    "out_table": {
        "type": FileOutputDefinition,
        "description": "Table output to tablefile.",
    },
}


# flake8: noqa: E501
