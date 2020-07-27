"""
Input and output specification dictionaries for FSL's topup_ script.

.. _topup:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/topup/TopupUsersGuide
"""

from django_analyses.models.input.definitions import (
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)

from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    ListOutputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)
from pathlib import Path
import os


FSLDIR = os.environ["FSLDIR"]

#: *topup* input specification.
TOPUP_INPUT_SPECIFICATION = {
    "dwi_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "Raw DWI image with corresponding json file.",
        "is_configuration": False,
    },
    "phasediff_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "Raw opposite-encoded (phasediff) image with corresponding json file.",  # noqa: E501
        "is_configuration": False,
    },
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "A 4D NIfTI file containing images of dual-phase encoded images.",  # noqa: E501
        "is_configuration": False,
        "value_attribute": "path.__str__",
    },
    "encoding_direction": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "Encoding direction for automatic generation of encoding file. Mutually exclusive with inputs: encoding_file. Requires inputs: readout_times.",  # noqa: E501
    },
    "encoding_file": {
        "type": FileInputDefinition,
        "description": "Path to a file containing images' phase-encoding directions/readout times. Mutually exclusive with inputs: encoding direction.",  # noqa: E501
    },
    "readout_times": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "A list of readout times (floats). Requires inputs: encoding_direction.",  # noqa: E501
    },
    "config": {
        "type": FileInputDefinition,
        "description": "Path to configuration files specifying command line arguments.",  # noqa: E501
        "default": Path(Path(FSLDIR) / "etc" / "flirtsch" / "b02b0.cnf"),
    },
    "estmov": {
        "type": IntegerInputDefinition,
        "description": "Estimate movements if set.",
        "min_value": 0,
        "max_value": 1,
    },
    "fwhm": {
        "type": FloatInputDefinition,
        "description": "FWHM (in mm) of gaussian smoothing kernel.",
    },
    "interp": {
        "type": StringInputDefinition,
        "description": "Image interpolation model, linear or spline.",
        "choices": ["spline", "linear"],
    },
    "max_iter": {
        "type": IntegerInputDefinition,
        "description": "Max # of non-linear iterations.",
    },
    "minmet": {
        "type": IntegerInputDefinition,
        "description": "Minimisation method 0=Levenberg-Marquardt, 1=Scaled Conjugate Gradient.",  # noqa: E501
        "min_value": 0,
        "max_value": 1,
    },
    "numprec": {
        "type": FloatInputDefinition,
        "description": "Precision for representing Hessian, double or float.",
    },
    "out_base": {
        "type": StringInputDefinition,
        "description": "Base-name of output files (spline coefficients (Hz) and movement parameters).",  # noqa: E501
        "default": "topup",
    },
    "out_corrected": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "Path to 4D image file with unwarped images.",
        "default": "out_corrected.nii.gz",
    },
    "out_field": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "Path to image file with field (Hz).",
        "default": "out_field.nii.gz",
    },
    "out_jac_prefix": {
        "type": StringInputDefinition,
        "description": " Prefix for the warpfield images.",
        "default": "jac_",
    },
    "out_mat_prefix": {
        "type": StringInputDefinition,
        "description": "Prefix for the realignment matrices.",
        "default": "xfm",
    },
    "out_warp_prefix": {
        "type": StringInputDefinition,
        "description": "Prefix for the warpfield images (in mm).",
        "default": "warpfield",
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
    "reg_lambda": {
        "type": FloatInputDefinition,
        "description": "Weight of regularisation, default depending on –ssqlambda and –regmod switches.",  # noqa: E501
    },
    "regmod": {
        "type": StringInputDefinition,
        "description": "Regularisation term implementation. Defaults to bending_energy. Note that the two functions have vastly different scales. The membrane energy is based on the first derivatives and the bending energy on the second derivatives. The second derivatives will typically be much smaller than the first derivatives, so input lambda will have to be larger for bending_energy to yield approximately the same level of regularisation.",  # noqa: E501
        "choices": ["bending_energy", "membrane_energy"],
    },
    "regrid": {
        "type": IntegerInputDefinition,
        "description": "If set (=1), the calculations are done in a different grid.",  # noqa: E501
        "min_value": 0,
        "max_value": 1,
    },
    "scale": {
        "type": IntegerInputDefinition,
        "description": "If set (=1), the images are individually scaled to a common mean.",  # noqa: E501
        "min_value": 0,
        "max_value": 1,
    },
    "splineorder": {
        "type": IntegerInputDefinition,
        "description": "Order of spline, 2->Qadratic spline, 3->Cubic spline.",
    },
    "ssqlambda": {
        "type": IntegerInputDefinition,
        "description": "Weight lambda by the current value of the ssd. If used (=1), the effective weight of regularisation term becomes higher for the initial iterations, therefore initial steps are a little smoother than they would without weighting. This reduces the risk of finding a local minimum.",  # noqa: E501
        "min_value": 0,
        "max_value": 1,
    },
    "subsamp": {
        "type": IntegerInputDefinition,
        "description": "Sub-sampling scheme.",
    },
    "warp_res": {
        "type": FloatInputDefinition,
        "description": "(approximate) resolution (in mm) of warp basis for the different sub-sampling levels.",  # noqa: E501
    },
}

#: *topup*  output specification.
TOPUP_OUTPUT_SPECIFICATION = {
    "out_corrected": {
        "type": NiftiOutputDefinition,
        "description": "Path to 4D image file with unwarped images.",
    },
    "out_enc_file": {
        "type": FileOutputDefinition,
        "description": "Encoding directions file output for applytopup.",
    },
    "out_field": {
        "type": NiftiOutputDefinition,
        "description": "Path to image file containing field (Hz).",
    },
    "out_fieldcoef": {
        "type": FileOutputDefinition,
        "description": "Path to file containing the field coefficients.",
    },
    "out_jacs": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "List of paths to jacobian images.",
    },
    "out_logfile": {
        "type": FileOutputDefinition,
        "description": "Path to topup's log-file.",
    },
    "out_mats": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "List of paths to realignment matrices.",
    },
    "out_movpar": {
        "type": FileOutputDefinition,
        "description": "Path to movement parameters text file (Movpar.txt).",
    },
    "out_warps": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "List of paths to warpfield images.",
    },
}
