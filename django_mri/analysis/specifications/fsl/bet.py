"""
Input and output specification dictionaries for FSL's BET_ script.

See Also
--------
* `nipype.interfaces.fsl.preprocess.BET`_

Notes
-----
For more information about BET, see FSL's `BET documentation`_.

.. _BET documentation:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/BET
.. _nipype.interfaces.fsl.preprocess.BET:
   https://nipype.readthedocs.io/en/1.1.7/interfaces/generated/interfaces.fsl/preprocess.html#bet
"""


from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)

from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

#: *BET* input specification dictionary.
BET_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "A NIfTI format file to skullstrip.",
        "is_configuration": False,
        "value_attribute": "path.__str__",
    },
    "out_file": {
        "type": StringInputDefinition,
        "description": "Desired output file path.",
        "is_output_path": True,
        "default": "brain.nii.gz",
    },
    "outline": {
        "type": BooleanInputDefinition,
        "description": "Whether to create a surface outline image.",
    },
    "mask": {
        "type": BooleanInputDefinition,
        "description": "Whether to create a binary mask image.",
    },
    "skull": {
        "type": BooleanInputDefinition,
        "description": "Whether to create a skull image.",
    },
    "no_output": {
        "type": BooleanInputDefinition,
        "description": "Suppress output creation altogether.",
    },
    "frac": {
        "type": FloatInputDefinition,
        "default": 0.5,
        "description": "Fractional intensity threshold.",
        "min_value": 0,
        "max_value": 1,
    },
    "vertical_gradient": {
        "type": FloatInputDefinition,
        "default": 0,
        "description": "Verical gradient in fractional intensity threshold.",
        "min_value": -1,
        "max_value": 1,
    },
    "radius": {
        "type": IntegerInputDefinition,
        "description": "Head radius.",
        "min_value": 0,
    },
    "center": {
        "type": ListInputDefinition,
        "description": "Center of gravity of initial mesh surface in voxels.",
        "element_type": "INT",
        "min_length": 3,
        "max_length": 3,
    },
    "threshold": {
        "type": BooleanInputDefinition,
        "description": "Whether to apply thresholding to segmented brain image and mask.",  # noqa: E501
    },
    "mesh": {
        "type": BooleanInputDefinition,
        "description": "Whether to generate a VTK mesh brain surface.",
    },
    "robust": {
        "type": BooleanInputDefinition,
        "description": "Whether to coduct a robust brain center estimation, iterating BET several times.",  # noqa: E501
    },
    "padding": {
        "type": BooleanInputDefinition,
        "description": "Whether to improve BET if FOV is very small in Z (by temporarily padding end slices).",  # noqa: E501
    },
    "remove_eyes": {
        "type": BooleanInputDefinition,
        "description": "Whether to remove eyes and optic nerves (can be useful in SIENA).",  # noqa: E501
    },
    "surfaces": {
        "type": BooleanInputDefinition,
        "description": "Whether to run bet2 and then betsurf to get additional skull and scalp surfaces (includes registrations).",  # noqa: E501
    },
    "t2_guided": {
        "type": FileInputDefinition,
        "description": "Include a raw T2 scan.",
    },
    "functional": {
        "type": BooleanInputDefinition,
        "description": "Apply brain extraction to 4D fMRI data.",
    },
    "reduce_bias": {
        "type": BooleanInputDefinition,
        "description": "Bias field and neck cleanup.",
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
}

#: *BET* output specification dictionary.
BET_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the extracted brain file, if generated.",
    },
    "mask_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the binary mask file, if generated.",
    },
    "outline_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outline file, if generated.",
    },
    "meshfile": {
        "type": FileOutputDefinition,
        "description": "The path of the VTK mesh file, if generated.",
    },
    "inskull_mask_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the inward skull mask file, if generated.",
    },
    "inskull_mesh_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the inward skull mesh outline file, if generated.",  # noqa: E501
    },
    "outskull_mask_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outward skull mask file, if generated.",  # noqa: E501
    },
    "outskull_mesh_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outward skull mesh outline file, if generated.",  # noqa: E501
    },
    "outskin_mask_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outward skin mask file, if generated.",
    },
    "outskin_mesh_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outward skin mesh outline file, if generated.",  # noqa: E501
    },
    "skull_mask_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the skull mask file, if generated.",
    },
}
