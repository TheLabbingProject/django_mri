"""
Default values for the various keys required in the batch template.
"""

SEGMENTATION_DEFAULTS = {
    "n_processes": 4,
    "affine_regularisation": "mni",
    "bias_strength": "medium",
    "accuracy": "average",
    "affine_preprocessing": "rough",
    "local_adaptive_segmentation_strength": "medium",
    "skull_stripping": "aprg",
    "normalized_image_voxel_size": 1.5,
    "internal_resampling": 1,
    "surface_estimation": False,
    "neuromorphometrics": True,
    "lpba40": False,
    "cobra": False,
    "hammers": False,
    "native_grey_matter": False,
    "modulated_grey_matter": True,
    "dartel_grey_matter": False,
    "native_white_matter": False,
    "modulated_white_matter": True,
    "dartel_white_matter": False,
    "native_pve": True,
    "warped_image": True,
    "jacobian_determinant": False,
    "deformation_fields": "none",
}
