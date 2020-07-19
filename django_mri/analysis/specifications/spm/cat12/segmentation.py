"""
Input and output specification dictionaries for CAT12 segmentation interface.

See Also
--------
* :class:`CAT12 segmentation interface
  <django_mri.analysis.interfaces.matlab.spm.cat12.segmentation.segmentation.Segmentation>`

"""

from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    DirectoryInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    StringInputDefinition,
)

from django_analyses.models.output.definitions import FileOutputDefinition


#: CAT12 segmentation interface input specification dictionary.
CAT12_SEGMENTATION_INPUT_SPECIFICATION = {
    "path": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Anatomical high resolution raw data to be segmented.",
        "is_configuration": False,
        "run_method_input": True,
    },
    "destination": {
        "type": DirectoryInputDefinition,
        "description": "Where to output the results.",
        "is_configuration": False,
        "is_output_directory": True,
        "run_method_input": True,
    },
    "n_processes": {
        "type": IntegerInputDefinition,
        "required": False,
        "default": 4,
        "description": "Whether to implement multi-threading and with how many processes.",  # noqa: E501
        "is_configuration": False,
    },
    "tpm_path": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Tissue probability map to be used.",
        "is_configuration": True,
    },
    "affine_regularisation": {
        "type": StringInputDefinition,
        "required": False,
        "description": "",
        "choices": ["mni", "eastern", "none"],
        "default": "mni",
        "is_configuration": True,
    },
    "bias_strength": {
        "type": StringInputDefinition,
        "required": False,
        "description": "",
        "choices": ["light", "medium", "strong"],
        "default": "medium",
        "is_configuration": True,
    },
    "accuracy": {
        "type": StringInputDefinition,
        "required": False,
        "description": "",
        "choices": ["average", "high", "ultra high"],
        "default": "average",
        "is_configuration": True,
    },
    "affine_preprocessing": {
        "type": StringInputDefinition,
        "required": False,
        "description": "",
        "choices": ["none", "light", "full", "rough"],
        "default": "rough",
        "is_configuration": True,
    },
    "local_adaptive_segmentation_strength": {
        "type": StringInputDefinition,
        "required": False,
        "description": "",
        "choices": ["none", "light", "medium", "strong"],
        "default": "medium",
        "is_configuration": True,
    },
    "skull_stripping": {
        "type": StringInputDefinition,
        "required": False,
        "description": "",
        "choices": ["none", "spm", "gcut", "aprg"],
        "default": "aprg",
        "is_configuration": True,
    },
    "normalized_image_voxel_size": {
        "type": FloatInputDefinition,
        "required": False,
        "description": "",
        "default": 1.5,
        "is_configuration": True,
    },
    "internal_resampling": {
        "type": FloatInputDefinition,
        "required": False,
        "description": "",
        "default": 1.5,
        "is_configuration": True,
    },
    "surface_estimation": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "neuromorphometrics": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": True,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "lpba40": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "cobra": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "hammers": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "native_grey_matter": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "modulated_grey_matter": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": True,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "dartel_grey_matter": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "native_white_matter": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "modulated_white_matter": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": True,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "dartel_white_matter": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "native_pve": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": True,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "warped_image": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": True,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "jacobian_determinant": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "",
        "default": False,
        "is_configuration": False,
        "is_output_switch": True,
    },
    "deformation_fields": {
        "type": StringInputDefinition,
        "required": False,
        "description": "",
        "choices": ["none", "forward", "inverse", "both"],
        "default": "none",
        "is_configuration": False,
        "is_output_switch": True,
    },
}

#: CAT12 segmentation interface output specification dictionary.
CAT12_SEGMENTATION_OUTPUT_SPECIFICATION = {
    "left_hemisphere_central_surface": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "left_hemisphere_spherical_surface": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "left_hemisphere_spherical_registered_surface": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "left_hemisphere_cortical_thickness": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "right_hemisphere_central_surface": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "right_hemisphere_spherical_surface": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "right_hemisphere_spherical_registered_surface": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "right_hemisphere_cortical_thickness": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "labels_mat": {"type": FileOutputDefinition, "description": ""},
    "labels_xml": {"type": FileOutputDefinition, "description": ""},
    "native_grey_matter": {"type": FileOutputDefinition, "description": ""},
    "modulated_grey_matter": {"type": FileOutputDefinition, "description": ""},
    "dartel_grey_matter": {"type": FileOutputDefinition, "description": ""},
    "native_white_matter": {"type": FileOutputDefinition, "description": ""},
    "modulated_white_matter": {
        "type": FileOutputDefinition,
        "description": "",
    },
    "dartel_white_matter": {"type": FileOutputDefinition, "description": ""},
    "native_pve": {
        "type": FileOutputDefinition,
        "description": "Labeled version of the segmentation in native space.",
    },
    "warped_image": {
        "type": FileOutputDefinition,
        "description": "The image in normalised space without any modulation.",
    },
    "jacobian_determinant": {
        "type": FileOutputDefinition,
        "description": "A value representing local volume changes.",
    },
    "forward_deformation_field": {
        "type": FileOutputDefinition,
        "description": "The deformation field from the image to the template.",
    },
    "inverse_deformation_field": {
        "type": FileOutputDefinition,
        "description": "The deformation field from the template to the image.",
    },
    "batch_file": {
        "type": FileOutputDefinition,
        "description": "The MATLAB .m file used to run the CAT12 segmentation.",  # noqa: E501
    },
    "report_mat": {
        "type": FileOutputDefinition,
        "description": "MATLAB format .mat file containing the run's log.",
    },
    "report_xml": {
        "type": FileOutputDefinition,
        "description": "XML log of the run.",
    },
    "report_txt": {
        "type": FileOutputDefinition,
        "description": "Text format log file.",
    },
    "report_pdf": {
        "type": FileOutputDefinition,
        "description": "PDF log of the run.",
    },
    "report_jpg": {
        "type": FileOutputDefinition,
        "description": "JPG log of the run.",
    },
}
