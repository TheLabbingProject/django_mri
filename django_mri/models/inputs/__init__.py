"""
Custom :class:`~django_analyses.models.input.input.Input` and
:class:`~django_analyses.models.input.definitions.InputDefinition` subclasses.

These models expand upon django_analyses_\'
:mod:`~django_analyses.models.input` module to facilitate integration with the
various analysis interfaces.

.. _django_analyses:
   https://github.com/TheLabbingProject/django_analyses/
"""

from django_mri.models.inputs.nifti_input import NiftiInput
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_mri.models.inputs.scan_input import ScanInput
from django_mri.models.inputs.scan_input_definition import ScanInputDefinition
