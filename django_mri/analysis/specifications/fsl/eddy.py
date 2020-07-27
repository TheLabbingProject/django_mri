"""
Input and output specification dictionaries for FSL's eddy_ script.

.. _eddy:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/eddy
"""

from django_analyses.models.input.definitions import (
    FloatInputDefinition,
    IntegerInputDefinition,
    StringInputDefinition,
    BooleanInputDefinition,
)

from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)


#: *eddy* input specification dictionary.
EDDY_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "File containing all the images to estimate distortions for.",  # noqa: E501
        "is_configuration": False,
    },
    "in_acqp": {
        "type": StringInputDefinition,
        "required": True,
        "description": "File containing acquisition parameters.",
    },
    "in_bval": {
        "type": StringInputDefinition,
        "required": True,
        "description": "File containing the b-values for all volumes in –imain.",  # noqa: E501
    },
    "in_bvec": {
        "type": StringInputDefinition,
        "required": True,
        "description": "File containing the b-vectors for all volumes in –imain.",  # noqa: E501
    },
    "in_index": {
        "type": StringInputDefinition,
        "required": True,
        "description": "File containing indices for all volumes in –imain into –acqp and –topup.",  # noqa: E501
    },
    "in_mask": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "Mask to indicate brain.",
    },
    "cnr_maps": {
        "type": BooleanInputDefinition,
        "description": "Output CNR-Maps.",
        "default": False,
    },
    "dont_peas": {
        "type": BooleanInputDefinition,
        "description": "Do NOT perform a post-eddy alignment of shells.",
        "default": False,
    },
    "dont_sep_offs_move": {
        "type": BooleanInputDefinition,
        "description": "Do NOT perform a post-eddy alignment of shells.",
        "default": False,
    },
    "estimate_move_by_susceptibility": {
        "type": BooleanInputDefinition,
        "description": "Estimate how susceptibility field changes with subject movement.",  # noqa: E501
        "default": False,
    },
    "fep": {
        "type": BooleanInputDefinition,
        "description": "Fill empty planes in x- or y-directions.",
        "default": False,
    },
    "field": {
        "type": NiftiInputDefinition,
        "description": "Non-topup derived fieldmap scaled in Hz.",
    },
    "field_mat": {
        "type": StringInputDefinition,
        "description": "Matrix specifying the relative positions of the fieldmap, –field, and the first volume of the input file, –imain.",  # noqa: E501
    },
    "flm": {
        "type": StringInputDefinition,
        "choices": ["quadratic", "linear", "cubic"],
        "description": "First level EC model.",
        "default": "quadratic",
    },
    "fudge_factor": {
        "type": FloatInputDefinition,
        "description": "Fudge factor for hyperparameter error variance.",
        "default": 10.0,
    },
    "fwhm": {
        "type": FloatInputDefinition,
        "description": "FWHM for conditioning filter when estimating the parameters.",  # noqa: E501
    },
    "in_topup_fieldcoef": {
        "type": NiftiInputDefinition,
        "description": "opup results file containing the field coefficients.",
    },
    "in_topup_movpar": {
        "type": StringInputDefinition,
        "description": "Topup results file containing the movement parameters (movpar.txt). Requires inputs: in_topup_fieldcoef",  # noqa: E501
    },
    "initrand": {
        "type": BooleanInputDefinition,
        "description": "Resets rand for when selecting voxels.",
    },
    "interp": {
        "type": StringInputDefinition,
        "choices": ["spline", "trilinear"],
        "description": " Interpolation model for estimation step.",
        "default": "spline",
    },
    "is_shelled": {
        "type": BooleanInputDefinition,
        "description": "Override internal check to ensure that date are acquired on a set of b-value shells.",  # noqa: E501
    },
    "json": {
        "type": StringInputDefinition,
        "description": "Name of .json text file with information about slice timing. Mutually exclusive with inputs: slice_order. Requires inputs: mporder.",  # noqa: E501
    },
    "mbs_ksp": {
        "type": IntegerInputDefinition,
        "description": "Knot-spacing for MBS field estimation. Requires inputs: estimate_move_by_susceptibility.",  # noqa: E501
    },
    "mbs_lambda": {
        "type": IntegerInputDefinition,
        "description": "Weighting of regularisation for MBS estimation. Requires inputs: estimate_move_by_susceptibility.",  # noqa: E501
    },
    "mbs_niter": {
        "type": IntegerInputDefinition,
        "description": "Number of iterations for MBS estimation. Requires inputs: estimate_move_by_susceptibility.",  # noqa: E501
    },
    "method": {
        "type": StringInputDefinition,
        "choices": ["jac", "lsr"],
        "description": "Final resampling method (jacobian/least squares).",
        "default": "jac",
    },
    "mporder": {
        "type": IntegerInputDefinition,
        "description": "Order of slice-to-vol movement model.Requires inputs: use_cuda.",  # noqa: E501
    },
    "multiband_factor": {
        "type": IntegerInputDefinition,
        "description": "Multi-band factor.",
    },
    "multiband_offset": {
        "type": IntegerInputDefinition,
        "min_value": -1,
        "max_value": 1,
        "description": "Multi-band offset (-1 if bottom slice removed, 1 if top slice removed. Requires inputs: multiband_factor.",  # noqa: E501
    },
    "niter": {
        "type": IntegerInputDefinition,
        "description": "Number of iterations.",
        "default": 5,
    },
    "num_threads": {
        "type": IntegerInputDefinition,
        "description": "Number of openmp threads to use.",
        "default": 1,
    },
    "nvoxhp": {
        "type": IntegerInputDefinition,
        "description": "# of voxels used to estimate the hyperparameters.",
    },
    "out_base": {
        "type": StringInputDefinition,
        "description": "Basename for output image.",  # noqa: E501
        "default": "eddy_corrected",
    },
    "outlier_nstd": {
        "type": IntegerInputDefinition,
        "description": "Number of std off to qualify as outlier.Requires inputs: repol.",  # noqa: E501
    },
    "outlier_pos": {
        "type": BooleanInputDefinition,
        "description": "Consider both positive and negative outliers if set. Requires inputs: repol.",  # noqa: E501
    },
    "outlier_sqr": {
        "type": BooleanInputDefinition,
        "description": "Consider outliers among sums-of-squared differences if set. Requires inputs: repol.",  # noqa: E501
    },
    "outlier_type": {
        "type": StringInputDefinition,
        "choices": ["sw", "gw", "both"],
        "description": "Type of outliers, slicewise (sw), groupwise (gw) or both (both). Requires inputs: repol.",  # noqa: E501
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
    "repol": {
        "type": BooleanInputDefinition,
        "description": "Detect and replace outlier slices.",
    },
    "residuals": {
        "type": BooleanInputDefinition,
        "description": "Output Residuals.",
    },
    "session": {
        "type": StringInputDefinition,
        "description": "File containing session indices for all volumes in –imain.",  # noqa: E501
    },
    "slice2vol_interp": {
        "type": StringInputDefinition,
        "choices": ["trilinear", "spline"],
        "description": " Slice-to-vol interpolation model for estimation step. Requires inputs: mporder.",  # noqa: E501
    },
    "slice2vol_lambda": {
        "type": IntegerInputDefinition,
        "description": "Regularisation weight for slice-to-vol movement (reasonable range 1-10). Requires inputs: mporder.",  # noqa: E501
    },
    "slice2vol_niter": {
        "type": IntegerInputDefinition,
        "description": "umber of iterations for slice-to-vol. Requires inputs: mporder.",  # noqa: E501
    },
    "slice_order": {
        "type": StringInputDefinition,
        "description": "Name of text file completely specifying slice/group acquisition. Mutually exclusive with inputs: json. Requires inputs: mporder.",  # noqa: E501
    },
    "slm": {
        "type": StringInputDefinition,
        "choices": ["none", "linear", "quadratic"],
        "description": "Second level EC model.",
        "default": "none",
    },
    "use_cuda": {
        "type": BooleanInputDefinition,
        "description": "Run eddy using cuda gpu.",
    },
}

#: *eddy* input specification dictionary.
EDDY_OUTPUT_SPECIFICATION = {
    "out_cnr_maps": {
        "type": NiftiOutputDefinition,
        "description": "Path/name of file with the cnr_maps.",
    },
    "out_corrected": {
        "type": NiftiOutputDefinition,
        "description": "4D image file containing all the corrected volumes.",
    },
    "out_movement_over_time": {
        "type": FileOutputDefinition,
        "description": "Text file containing translations (mm) and rotations (radians) for each excitation.",  # noqa: E501
    },
    "out_movement_rms": {
        "type": NiftiOutputDefinition,
        "description": "Summary of the ‘total movement’ in each volume.",
    },
    "out_outlier_free": {
        "type": NiftiOutputDefinition,
        "description": "4D image file not corrected for susceptibility or eddy-current distortions or subject movement but with outlier slices replaced.",  # noqa: E501
    },
    "out_outlier_map": {
        "type": FileOutputDefinition,
        "description": "Matrix where rows represent volumes and columns represent slices. “0” indicates that scan-slice is not an outlier and “1” indicates that it is.",  # noqa: E501
    },
    "out_outlier_n_sqr_stdev_map": {
        "type": FileOutputDefinition,
        "description": "Matrix where rows represent volumes and columns represent slices. Values indicate number of standard deivations off the square root of the mean squared difference between observation and prediction is.",  # noqa: E501
    },
    "out_outlier_n_stdev_map": {
        "type": FileOutputDefinition,
        "description": "Matrix where rows represent volumes and columns represent slices. Values indicate number of standard deviations off the mean difference between observation and prediction is.",  # noqa: E501
    },
    "out_outlier_report": {
        "type": FileOutputDefinition,
        "description": "Text file with a plain language report on what outlier slices eddy has found.",  # noqa: E501
    },
    "out_parameter": {
        "type": FileOutputDefinition,
        "description": "Text file with parameters defining the field and movement for each scan.",  # noqa: E501
    },
    "out_residuals": {
        "type": NiftiOutputDefinition,
        "description": "Path/name of file with the residuals.",
    },
    "out_restricted_movement_rms": {
        "type": NiftiOutputDefinition,
        "description": "Summary of the ‘total movement’ in each volume disregarding translation in the PE direction.",  # noqa: E501
    },
    "out_rotated_bvecs": {
        "type": FileOutputDefinition,
        "description": "File containing rotated b-values for all volumes.",
    },
    "out_shell_alignment_parameters": {
        "type": FileOutputDefinition,
        "description": " Text file containing rigid body movement parameters between the different shells as estimated by a post-hoc mutual information based registration.",  # noqa: E501
    },
    "out_shell_pe_translation_parameters": {
        "type": FileOutputDefinition,
        "description": "Text file containing translation along the PE-direction between the different shells as estimated by a post-hoc mutual information based registration.",  # noqa: E501
    },
}
