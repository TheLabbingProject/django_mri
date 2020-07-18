"""
Input and output specification dictionaries for FSL's fsl_anat_ script.

.. _fsl_anat:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/fsl_anat
"""

from django_analyses.models.input.definitions.boolean_input_definition import (
    BooleanInputDefinition,
)
from django_analyses.models.input.definitions.float_input_definition import (
    FloatInputDefinition,
)
from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)
from django_analyses.models.input.definitions.directory_input_definition import (  # noqa: E501
    DirectoryInputDefinition,
)
from django_analyses.models.output.definitions.file_output_definition import (
    FileOutputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

#: *fsl_anat* input specification dictionary.
FSL_ANAT_INPUT_SPECIFICATION = {
    "image": {
        "type": NiftiInputDefinition,
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
        "type": NiftiOutputDefinition,
        "description": "Linear registration output.",
    },
    "nonlinear_registration": {
        "type": NiftiOutputDefinition,
        "description": "Non-linear registration output.",
    },
    "nonlinear_registration_field": {
        "type": NiftiOutputDefinition,
        "description": "Non-linear warp field.",
    },
    "nonlinear_registration_jacobian": {
        "type": NiftiOutputDefinition,
        "description": "Jacobian of the non-linear warp field.",
    },
    "volume_scales": {
        "type": FileOutputDefinition,
        "description": "A file containing a scaling factor and brain volumes, based on skull-contrained registration, suitable for head-size normalisation (as the scaling is based on the skull size, not the brain size).",  # noqa: E501
    },
    "bias_corrected_brain": {
        "type": NiftiOutputDefinition,
        "description": "Bias-corrected brain extraction result.",
    },
    "bias_corrected_brain_mask": {
        "type": NiftiOutputDefinition,
        "description": "Mask of bias-corrected brain extraction result.",
    },
    "fast_bias_correction": {
        "type": NiftiOutputDefinition,
        "description": "Bias-corrected version used for FAST segmentation.",
    },
    "csf_partial_volume": {
        "type": NiftiOutputDefinition,
        "description": "CSF partial volume segmenetation.",
    },
    "grey_matter_partial_volume": {
        "type": NiftiOutputDefinition,
        "description": "Grey matter partial volume segmenetation.",
    },
    "white_matter_partial_volume": {
        "type": NiftiOutputDefinition,
        "description": "White matter partial volume segmenetation.",
    },
    "segmentation_summary": {
        "type": NiftiOutputDefinition,
        "description": "A summary image showing the tissue with the greatest partial volume fraction per voxel.",  # noqa: E501
    },
    "subcortical_segmentation_summary": {
        "type": NiftiOutputDefinition,
        "description": "A summary image of subcortical segmentation results.",
    },
}
