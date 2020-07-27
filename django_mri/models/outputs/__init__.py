"""
Custom :class:`~django_analyses.models.output.output.Output` and
:class:`~django_analyses.models.output.definitions.OutputDefinition` subclasses.

These models expand upon django_analyses_\'
:mod:`~django_analyses.models.output` module to facilitate integration with the
various analysis interfaces.

.. _django_analyses:
   https://github.com/TheLabbingProject/django_analyses/
"""

from django_mri.models.outputs.nifti_output import NiftiOutput
from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)
