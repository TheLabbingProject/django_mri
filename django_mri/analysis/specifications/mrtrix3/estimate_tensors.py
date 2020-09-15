"""
Input and output specification dictionaries for MRtrix's *dwi2tensor* script.

See Also
--------
* `nipype.interfaces.mrtrix3.reconst.FitTensor`_

Notes
-----
For more information, see MRtrix3's `dwi2fod reference`_.

.. _dwi2tensor reference:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/dwi2tensor.html
.. _nipype.interfaces.mrtrix3.reconst.FitTensor:
    https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.mrtrix3.reconst.html#fittensor
"""
from django_analyses.models.input.definitions import (
    FileInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
    TupleInputDefinition,
    FloatInputDefinition,
    BooleanInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

DWI2TENSOR_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "description": "Input DWI image.",
        "required": True,
        "is_configuration": False,
    },
    "ols": {
        "type": BooleanInputDefinition,
        "description": "perform initial fit using an ordinary least-squares (OLS) fit",
        "default": False,
    },
    "b0": {
        "type": StringInputDefinition,
        "description": "the output b0 image.",
        "is_output_path": True,
    },
    "dkt": {
        "type": StringInputDefinition,
        "description": "the output dkt image.",
        "is_output_path": True,
    },
    "iter": {
        "type": IntegerInputDefinition,
        "description": "number of iterative reweightings for IWLS algorithm",
        "default": True,
    },
    "predicted_signal": {
        "type": StringInputDefinition,
        "description": "the predicted dwi image",
        "is_output_path": True,
    },
    "grad": {
        "type": StringInputDefinition,
        "description": "Dw gradient scheme (MRTrix format). Mutually exclusive with inputs: grad_fsl.",  # noqa: E501
    },
    "fslgrad": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "dw gradient scheme (FSL format).List of paths to [bvec, bval] files. Mutually exclusive with inputs: grad_file.",  # noqa: E501
    },
    "mask": {"type": StringInputDefinition, "description": "Mask image."},
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
    "tensor_file": {
        "type": StringInputDefinition,
        "description": "The output tensor image",
        "is_output_path": True,
        "default": "tensor.mif",
    },
}

DWI2TENSOR_OUTPUT_SPECIFICATION = {
    "out_file": {
        "type": FileOutputDefinition,
        "description": "The output DTI file.",
    },
}
