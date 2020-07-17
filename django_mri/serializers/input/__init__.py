"""
Serializers for the :class:`~django_mri.models.inputs.nifti_input.NiftiInput`,
:class:`~django_mri.models.inputs.nifti_input_definition.NiftiInputDefinition`,
:class:`~django_mri.models.inputs.scan_input.ScanInput`, and
:class:`~django_mri.models.inputs.scan_input_definition.ScanInputDefinition`
models.
"""

from django_mri.serializers.input.nifti_input import NiftiInputSerializer
from django_mri.serializers.input.scan_input import ScanInputSerializer
