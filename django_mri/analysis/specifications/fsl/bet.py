from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)

from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import NiftiInputDefinition
from django_mri.models.outputs.nifti_output_definition import NiftiOutputDefinition


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
        "description": "Whether to apply thresholding to segmented brain image and mask.",
    },
    "mesh": {
        "type": BooleanInputDefinition,
        "description": "Whether to generate a VTK mesh brain surface.",
    },
    "robust": {
        "type": BooleanInputDefinition,
        "description": "Whether to coduct a robust brain center estimation, iterating BET several times.",
    },
    "padding": {
        "type": BooleanInputDefinition,
        "description": "Whether to improve BET if FOV is very small in Z (by temporarily padding end slices).",
    },
    "remove_eyes": {
        "type": BooleanInputDefinition,
        "description": "Whether to remove eyes and optic nerves (can be useful in SIENA).",
    },
    "surfaces": {
        "type": BooleanInputDefinition,
        "description": "Whether to run bet2 and then betsurf to get additional skull and scalp surfaces (includes registrations).",
    },
    "t2_guided": {"type": FileInputDefinition, "description": "Include a raw T2 scan."},
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
        "description": "The path of the inward skull mesh outline file, if generated.",
    },
    "outskull_mask_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outward skull mask file, if generated.",
    },
    "outskull_mesh_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outward skull mesh outline file, if generated.",
    },
    "outskin_mask_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outward skin mask file, if generated.",
    },
    "outskin_mesh_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the outward skin mesh outline file, if generated.",
    },
    "skull_mask_file": {
        "type": NiftiOutputDefinition,
        "description": "The path of the skull mask file, if generated.",
    },
}
