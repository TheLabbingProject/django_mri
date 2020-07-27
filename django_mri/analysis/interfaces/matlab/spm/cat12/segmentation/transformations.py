"""
Definition of the :obj:`SEGMENTATION_TRANSFORMATIONS` dictionary.
"""


#: Transformation to apply to option values before editing the batch template.
SEGMENTATION_TRANSFORMATIONS = {
    "bias_strength": {"light": 0.25, "medium": 0.5, "strong": 0.75},
    "accuracy": {"average": 0.5, "high": 0.75, "ultra high": 1},
    "affine_preprocessing": {"none": 0, "light": 1, "full": 2, "rough": 1070},
    "local_adaptive_segmentation_strength": {
        "none": 0,
        "light": 0.25,
        "medium": 0.5,
        "strong": 0.75,
    },
    "skull_stripping": {"none": -1, "spm": 0, "gcut": 0.5, "aprg": 2},
    "deformation_fields": {
        "none": "[0 0]",
        "forward": "[1 0]",
        "inverse": "[0 1]",
        "both": "[1 1]",
    },
    "dartel_grey_matter": {"no": 0, "rigid": 1, "affine": 2},
    "dartel_white_matter": {"no": 0, "rigid": 1, "affine": 2},
}
