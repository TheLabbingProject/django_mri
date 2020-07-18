"""
Input and output specification dictionaries for FSL's FAST_ script.

.. _FAST:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST
"""

from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    StringInputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)


#: *FAST* input specification dictionary.
FAST_INPUT_SPECIFICATION = {
    "in_files": {
        "type": NiftiInputDefinition,
        "description": "Path to NIfTI format image file to be segmented.",
        "value_attribute": "path.__str__",
        "required": True,
    },
    "args": {
        "type": StringInputDefinition,
        "description": "Additional parameters to the command.",
        "required": False,
    },
    "bias_iters": {
        "type": IntegerInputDefinition,
        "required": False,
        "description": "Number of main-loop iterations during bias-field removal.",  # noqa: E501
        "min_value": 1,
        "max_value": 10,
    },
    "bias_lowpass": {
        "type": IntegerInputDefinition,
        "required": False,
        "description": "Bias field smoothing extent (FWHM) in millimeters.",
        "min_value": 4,
        "max_value": 40,
    },
    "hyper": {
        "type": FloatInputDefinition,
        "required": False,
        "description": "Segmentation spatial smoothness.",
        "min_value": 0,
        "max_value": 1,
    },
    "img_type": {
        "type": IntegerInputDefinition,
        "required": False,
        "description": "Integer specifying type of image: (1=T1, 2=T2, 3=PD).",
        "min_value": 1,
        "max_value": 3,
    },
    "init_seg_smooth": {
        "type": FloatInputDefinition,
        "required": False,
        "description": "Initial segmentation spatial smoothness (during bias field estimation).",  # noqa: E501
        "min_value": 0.0001,
        "max_value": 0.1,
    },
    "init_transform": {
        "type": FileInputDefinition,
        "required": False,
        "description": "<standard2input.mat> initialise using priors.",
    },
    "iters_afterbias": {
        "type": IntegerInputDefinition,
        "required": False,
        "description": "Number of main-loop iterations after bias-field removal.",  # noqa: E501
        "min_value": 1,
        "max_value": 20,
    },
    "manual_seg": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Filename containing intensities.",
    },
    "mixel_smooth": {
        "type": FloatInputDefinition,
        "required": False,
        "description": "Spatial smoothness for mixeltype.",
        "min_value": 0,
        "max_value": 1,
    },
    "no_bias": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Do not remove bias field.",
    },
    "no_pve": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Turn off PVE (partial volume estimation).",
    },
    "number_classes": {
        "type": IntegerInputDefinition,
        "required": False,
        "description": "Number of tissue-type classes.",
        "min_value": 1,
        "max_value": 10,
        "default": 3,
    },
    "out_basename": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Base name of output files.",
        "default": "segmented",
    },
    "output_biascorrected": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Output restored image (bias-corrected image).",
    },
    "output_biasfield": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Output estimated bias-field.",
    },
    "probability_maps": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Outputs individual probability maps.",
    },
    "segment_iters": {
        "type": IntegerInputDefinition,
        "required": False,
        "description": "Number of segmentation-initialisation iterations.",
        "min_value": 1,
        "max_value": 50,
    },
    "segments": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Outputs a separate binary image for each tissue type.",
    },
    "use_priors": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Use priors throughout.",
    },
    "output_type": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
}

#: *FAST* output specification dictionary.
FAST_OUTPUT_SPECIFICATION = {
    "tissue_class_map": {
        "type": NiftiOutputDefinition,
        "description": "An image of all tissue classes represented as 1, 2, and 3.",  # noqa: E501
    },
    "mixeltype": {
        "type": NiftiOutputDefinition,
        "description": "Path/name of mixeltype volume file _mixeltype.",
    },
    "partial_volume_0": {"type": NiftiOutputDefinition, "description": ""},
    "partial_volume_1": {"type": NiftiOutputDefinition, "description": ""},
    "partial_volume_2": {"type": NiftiOutputDefinition, "description": ""},
}
