from django_analyses.models.input.definitions import (
    FileInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

APPLY_TOPUP_INPUT_SPECIFICATION = {
    "in_files": {
        "type": ListInputDefinition,
        "required": True,
        "description": "List of paths to NIfTI files to apply topup's results on.",  # noqa: E501
        "is_configuration": False,
    },
    "encoding_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Path to a file containing images' phase-encoding directions/readout times. Mutually exclusive with inputs: encoding direction.",  # noqa: E501
    },
    "datatype": {
        "type": StringInputDefinition,
        "description": "Force output data type.",
        "choices": ["float", "char", "int", "short", "double"],
    },
    "in_index": {
        "type": ListInputDefinition,
        "description": "Comma separated list of indices corresponding to –datain.",  # noqa: E501
    },
    "in_topup_fieldcoef": {
        "type": NiftiInputDefinition,
        "description": "Path to topup file containing the field coefficients. Requires inputs: in_topup_movpar",  # noqa: E501
    },
    "in_topup_movpar": {
        "type": FileInputDefinition,
        "description": "Path to topup movpar.txt file. Requires input: in_topup_fieldcoef",  # noqa: E501
    },
    "interp": {
        "type": StringInputDefinition,
        "description": "Image interpolation model, linear or spline.",
        "choices": ["spline", "trilinear"],
    },
    "method": {
        "type": StringInputDefinition,
        "description": "Use jacobian modulation (jac) or least-squares resampling (lsr).",  # noqa: E501
        "choices": ["jac", "lsr"],
    },
    "out_corrected": {
        "type": StringInputDefinition,
        "description": "Path to 4D image file with unwarped images.",
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "default": "NIFTI_GZ",
    },
}
APPLY_TOPUP_OUTPUT_SPECIFICATION = {
    "out_corrected": {
        "type": NiftiOutputDefinition,
        "description": "Path to 4D image file with unwarped images.",
    },
}
