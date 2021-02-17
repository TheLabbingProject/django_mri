"""
Input and output specification dictionaries for FSL's fsl_anat_ script.

.. _fsl_anat:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/fsl_anat
"""

from django_analyses.models.input.definitions.boolean_input_definition import (
    BooleanInputDefinition,
)
from django_analyses.models.input.definitions.directory_input_definition import (
    DirectoryInputDefinition,
)
from django_analyses.models.input.definitions.file_input_definition import (
    FileInputDefinition,
)
from django_analyses.models.input.definitions.float_input_definition import (
    FloatInputDefinition,
)
from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)
from django_analyses.models.output.definitions.file_output_definition import (
    FileOutputDefinition,
)

#: *fsl_anat* input specification dictionary.
FSL_ANAT_INPUT_SPECIFICATION = {
    "image": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input image for preprocessing.",
        "is_configuration": False,
        "run_method_input": True,
    },
    "destination": {
        "type": DirectoryInputDefinition,
        "description": "Run output destination.",
        "required": False,
        "is_configuration": False,
        "is_output_directory": True,
        "run_method_input": True,
    },
    "weak_bias": {
        "type": BooleanInputDefinition,
        "description": "Used for images with little and/or smooth bias fields.",  # noqa: E501
    },
    "no_reorient": {
        "type": BooleanInputDefinition,
        "description": "Turn off `fslreorient2std` execution.",
    },
    "no_crop": {
        "type": BooleanInputDefinition,
        "description": "Turn off automated cropping (`robustfov`).",
    },
    "no_bias": {
        "type": BooleanInputDefinition,
        "description": "Turn off FAST bias field correction.",
    },
    "no_registration": {
        "type": BooleanInputDefinition,
        "description": "Turn off registration to standard using FLIRT and FNIRT.",  # noqa: E501
    },
    "no_nonlinear_registration": {
        "type": BooleanInputDefinition,
        "description": "Turn off non-linear registration to standard using FNIRT.",  # noqa: E501
    },
    "no_segmentation": {
        "type": BooleanInputDefinition,
        "description": "Turn off tissue-type segmentation using FAST.",
    },
    "no_subcortical_segmentation": {
        "type": BooleanInputDefinition,
        "description": "Turn off subcortical segmentation using FIRST.",
    },
    "no_search": {
        "type": BooleanInputDefinition,
        "description": "Specify that linear registration uses the -nosearch option (FLIRT).",  # noqa: E501
    },
    "bias_field_smoothing": {
        "type": FloatInputDefinition,
        "description": "Specify the value for bias field smoothing (the -l option in FAST).",  # noqa: E501
    },
    "image_type": {
        "type": StringInputDefinition,
        "description": "Specify the type of image (T1, T2, or PD, default is T1).",  # noqa: E501
        "choices": ["T1", "T2", "PD"],
        "default": "T1",
    },
    "no_cleanup": {
        "type": BooleanInputDefinition,
        "description": "Do not remove intermediate files.",
    },
}

#: *fsl_anat* output specification dictionary.
FSL_ANAT_OUTPUT_SPECIFICATION = {
    "linear_registration": {
        "type": FileOutputDefinition,
        "description": "Linear registration output.",
    },
    "nonlinear_registration": {
        "type": FileOutputDefinition,
        "description": "Non-linear registration output.",
    },
    "nonlinear_registration_field": {
        "type": FileOutputDefinition,
        "description": "Non-linear warp field.",
    },
    "nonlinear_registration_jacobian": {
        "type": FileOutputDefinition,
        "description": "Jacobian of the non-linear warp field.",
    },
    "volume_scales": {
        "type": FileOutputDefinition,
        "description": "A file containing a scaling factor and brain volumes, based on skull-contrained registration, suitable for head-size normalisation (as the scaling is based on the skull size, not the brain size).",  # noqa: E501
    },
    "bias_corrected_brain": {
        "type": FileOutputDefinition,
        "description": "Bias-corrected brain extraction result.",
    },
    "bias_corrected_brain_mask": {
        "type": FileOutputDefinition,
        "description": "Mask of bias-corrected brain extraction result.",
    },
    "fast_bias_correction": {
        "type": FileOutputDefinition,
        "description": "Bias-corrected version used for FAST segmentation.",
    },
    "csf_partial_volume": {
        "type": FileOutputDefinition,
        "description": "CSF partial volume segmenetation.",
    },
    "grey_matter_partial_volume": {
        "type": FileOutputDefinition,
        "description": "Grey matter partial volume segmenetation.",
    },
    "white_matter_partial_volume": {
        "type": FileOutputDefinition,
        "description": "White matter partial volume segmenetation.",
    },
    "segmentation_summary": {
        "type": FileOutputDefinition,
        "description": "A summary image showing the tissue with the greatest partial volume fraction per voxel.",  # noqa: E501
    },
    "subcortical_segmentation_summary": {
        "type": FileOutputDefinition,
        "description": "A summary image of subcortical segmentation results.",
    },
}
