from django_analysis.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)

from django_analysis.models.output.definitions import FileOutputDefinition

FLIRT_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": "A NIfTI format file to register to the reference.",
        "is_configuration": False,
    },
    "reference": {
        "type": FileInputDefinition,
        "required": True,
        "description": "A NIfTI format file to register the input file with.",
    },
    "out_file": {
        "type": StringInputDefinition,
        "description": "The resulting registered image.",
        "is_output_path": True,
        "default": "registered.nii.gz",
    },
    "out_matrix_file": {
        "type": StringInputDefinition,
        "required": False,
        "description": "The calculated affine transformation that registers the input to the reference which is saved as a 4x4 affine matrix.",
        "is_output_path": True,
        "default": "affine_matrix.txt",
    },
    "out_log": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Path to save a log of the run if required.",
        "is_output_path": True,
        "default": "log.txt",
    },
    "in_matrix_file": {
        "type": FileInputDefinition,
        "required": False,
        "description": "An 4x4 affine transformation matrix to apply.",
    },
    "apply_xfm": {
        "type": BooleanInputDefinition,
        "description": "Whether to apply an existing affine transformation.",
    },
    "apply_isoxfm": {
        "type": FloatInputDefinition,
        "description": "Whether to apply an affine transformation with isotropic resampling.",
    },
    "datatype": {
        "type": StringInputDefinition,
        "description": "Output data type.",
        "choices": ["char", "short", "int", "float", "double"],
    },
    "cost": {
        "type": StringInputDefinition,
        "description": "Type of cost function to apply.",
        "choices": [
            "mutualinfo",
            "corratio",
            "normcorr",
            "normmi",
            "leastsq",
            "labeldiff",
            "bbr",
        ],
    },
    "uses_qform": {
        "type": BooleanInputDefinition,
        "description": "Whether to initialize using sform or qform.",
    },
    "display_init": {
        "type": BooleanInputDefinition,
        "description": "Whether to display the initial matrix.",
    },
    "angle_rep": {
        "type": StringInputDefinition,
        "description": "Rotation angles representation.",
        "choices": ["quaternion", "euler"],
    },
    "interp": {
        "type": StringInputDefinition,
        "description": "Final interpolation method used in reslicing.",
        "choices": ["trilinear", "nearestneighbour", "sinc", "spline"],
    },
    "sinc_width": {
        "type": IntegerInputDefinition,
        "description": "Full width in voxels.",
    },
    "sinc_window": {
        "type": StringInputDefinition,
        "description": "Final interpolation method used in reslicing.",
        "choices": ["rectangular", "hanning", "blackman"],
    },
    "bins": {
        "type": IntegerInputDefinition,
        "description": "Number of histogram bins.",
    },
    "dof": {
        "type": IntegerInputDefinition,
        "description": "Tranform degrees of freedom.",
    },
    "no_resample": {
        "type": BooleanInputDefinition,
        "description": "Whether to not change input sampling.",
    },
    "force_scaling": {
        "type": BooleanInputDefinition,
        "description": "Force rescaling even for low resolution images.",
    },
    "min_sampling": {
        "type": FloatInputDefinition,
        "description": "Minimum voxel dimensions for resampling.",
    },
    "padding_size": {
        "type": IntegerInputDefinition,
        "description": "Interpolates outside image when using apply_xfm.",
    },
    "searchr_x": {
        "type": ListInputDefinition,
        "description": "Search angles along X-axis in degrees.",
        "element_type": "INT",
        "min_length": 2,
        "max_length": 2,
    },
    "searchr_y": {
        "type": ListInputDefinition,
        "description": "Search angles along Y-axis in degrees.",
        "element_type": "INT",
        "min_length": 2,
        "max_length": 2,
    },
    "searchr_z": {
        "type": ListInputDefinition,
        "description": "Search angles along Z-axis in degrees.",
        "element_type": "INT",
        "min_length": 2,
        "max_length": 2,
    },
    "no_search": {
        "type": BooleanInputDefinition,
        "description": "Set all angular search ranges to [0, 0].",
    },
    "coarse_search": {
        "type": IntegerInputDefinition,
        "description": "Coarse search delta angle.",
    },
    "fine_search": {
        "type": IntegerInputDefinition,
        "description": "Fine search delta angle.",
    },
    "schedule": {
        "type": FileInputDefinition,
        "description": "Replace default schedule.",
    },
    "ref_weight": {
        "type": FileInputDefinition,
        "description": "Refernce file for weighting.",
    },
    "in_weight": {
        "type": FileInputDefinition,
        "description": "Input file for weighting.",
    },
    "no_clamp": {
        "type": BooleanInputDefinition,
        "description": "Whether to not use intensity clamping.",
    },
    "no_resample_blur": {
        "type": BooleanInputDefinition,
        "description": "Whether to not use blurring on downsampling.",
    },
    "rigid2D": {
        "type": BooleanInputDefinition,
        "description": "Whether to use 2D rigid body mode (ignores DOF).",
    },
    "save_log": {
        "type": BooleanInputDefinition,
        "default": False,
        "description": "Whether to save a run log.",
    },
    "verbose": {
        "type": IntegerInputDefinition,
        "description": "Verbosity level (0 is the least verbose).",
    },
    "bgvalue": {
        "type": FloatInputDefinition,
        "description": "Use a specified background value for points outside FOV.",
    },
    # BBR Options
    "wm_seg": {
        "type": FileInputDefinition,
        "description": "White matter segmentation volume needed by BBR cost function.",
    },
    "wmcoords": {
        "type": FileInputDefinition,
        "description": "White matter boundary coordinates for BBR cost function.",
    },
    "wmnorms": {
        "type": FileInputDefinition,
        "description": "White matter boundary normals for BBR cost function.",
    },
    "fieldmap": {
        "type": FileInputDefinition,
        "description": "Fieldmap image in radians per second. Must be already registered to the reference image.",
    },
    "fieldmapmask": {
        "type": FileInputDefinition,
        "description": "Mask for fieldmap image.",
    },
    "pedir": {
        "type": IntegerInputDefinition,
        "description": "Phase encode direction of EPI - 1/2/3=x/y/z & -1/-2/-3=-x/-y/-z.",
    },
    "echospacing": {
        "type": FloatInputDefinition,
        "description": "Value of EPI echo spacing in seconds.",
    },
    "bbrtype": {
        "type": StringInputDefinition,
        "description": "Type of BBR cost function.",
        "choices": ["signed", "global_abs", "local_abs"],
    },
    "bbr_slope": {"type": FloatInputDefinition, "description": "Value of BBR slope."},
}


FLIRT_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "Path to registered file (if generated).",
    },
    "out_matrix_file": {
        "type": FileOutputDefinition,
        "description": "Path to the calculated affine transform (if generated).",
    },
    "out_log": {
        "type": FileOutputDefinition,
        "description": "Path to the run log (if generated).",
    },
}
