"""
Input and output specification dictionaries for MRtrix's *tensor2metric* script.

See Also
--------
* `nipype.interfaces.mrtrix3.utils.TensorMetrics`_

Notes
-----
For more information, see MRtrix3's `tensor2metric reference`_.

.. _dwi2tensor reference:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/tensor2metric.html
.. _nipype.interfaces.mrtrix3.utils.TensorMetrics:
    https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.mrtrix3.utils.html#tensormetrics
"""
from django_analyses.models.input.definitions import (
    FileInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
    TupleInputDefinition,
    FloatInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)

TENSOR2METRICS_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "description": "Input DTI image.",
        "required": True,
        "is_configuration": False,
    },
    "adc": {
        "type": StringInputDefinition,
        "description": "compute the mean apparent diffusion coefficient (ADC) of the diffusion tensor. (sometimes also referred to as the mean diffusivity (MD))",
        "is_output_path": True,
        "is_configuration": False,
        "default": "MD.nii.gz",
    },
    "fa": {
        "type": StringInputDefinition,
        "description": "compute the fractional anisotropy (FA) of the diffusion tensor.",
        "is_output_path": True,
        "is_configuration": False,
        "default": "FA.nii.gz",
    },
    "ad": {
        "type": StringInputDefinition,
        "description": "compute the axial diffusivity (AD) of the diffusion tensor. (equivalent to the principal eigenvalue)",
        "is_output_path": True,
        "is_configuration": False,
        "default": "AD.nii.gz",
    },
    "rd": {
        "type": StringInputDefinition,
        "description": "compute the radial diffusivity (RD) of the diffusion tensor. (equivalent to the mean of the two non-principal eigenvalues)",
        "is_output_path": True,
        "is_configuration": False,
        "default": "RD.nii.gz",
    },
    "cl": {
        "type": StringInputDefinition,
        "description": "compute the linearity metric of the diffusion tensor. (one of the three Westin shape metrics)",
        "is_output_path": True,
        "is_configuration": False,
        "default": "CL.nii.gz",
    },
    "cp": {
        "type": StringInputDefinition,
        "description": "compute the planarity metric of the diffusion tensor. (one of the three Westin shape metrics)",
        "is_output_path": True,
        "is_configuration": False,
        "default": "CP.nii.gz",
    },
    "cs": {
        "type": StringInputDefinition,
        "description": "compute the sphericity metric of the diffusion tensor. (one of the three Westin shape metrics)",
        "is_output_path": True,
        "is_configuration": False,
        "default": "CS.nii.gz",
    },
    "value": {
        "type": StringInputDefinition,
        "description": "compute the selected eigenvalue(s) of the diffusion tensor.",  # noqa: E501
    },
    "vector": {
        "type": StringInputDefinition,
        "description": "compute the selected eigenvector(s) of the diffusion tensor.",  # noqa: E501
    },
    "num": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "specify the desired eigenvalue/eigenvector(s). Note that several eigenvalues can be specified as a number sequence. For example, ‘1,3’ specifies the principal (1) and minor (3) eigenvalues/eigenvectors (default = 1).",
        "default": [1],
    },
    "modulate": {
        "type": StringInputDefinition,
        "description": "specify how to modulate the magnitude of the eigenvectors.",
        "choices": ["FA", "eigval", "none"],
        "default": "FA",
    },
    "mask": {
        "type": StringInputDefinition,
        "description": "only perform computation within the specified binary brain mask image.",
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
}

TENSOR2METRIC_OUTPUT_SPECIFICATION = {
    "adc": {
        "type": FileOutputDefinition,
        "description": "The mean apparent diffusion coefficient (ADC) of the diffusion tensor. (sometimes also referred to as the mean diffusivity (MD))",
    },
    "fa": {
        "type": FileOutputDefinition,
        "description": "The fractional anisotropy (FA) of the diffusion tensor.",
    },
    "ad": {
        "type": FileOutputDefinition,
        "description": "The axial diffusivity (AD) of the diffusion tensor. (equivalent to the principal eigenvalue)",
    },
    "rd": {
        "type": FileOutputDefinition,
        "description": "The radial diffusivity (RD) of the diffusion tensor. (equivalent to the mean of the two non-principal eigenvalues)",
    },
    "cl": {
        "type": FileOutputDefinition,
        "description": "The linearity metric of the diffusion tensor. (one of the three Westin shape metrics)",
    },
    "cp": {
        "type": FileOutputDefinition,
        "description": "The planarity metric of the diffusion tensor. (one of the three Westin shape metrics)",
    },
    "cs": {
        "type": FileOutputDefinition,
        "description": "The sphericity metric of the diffusion tensor. (one of the three Westin shape metrics)",
    },
    "value": {
        "type": FileOutputDefinition,
        "description": "compute the selected eigenvalue(s) of the diffusion tensor.",  # noqa: E501
    },
    "vector": {
        "type": FileOutputDefinition,
        "description": "compute the selected eigenvector(s) of the diffusion tensor.",  # noqa: E501
    },
}
