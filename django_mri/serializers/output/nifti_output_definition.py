"""
Definition of the
:class:`~django_mri.serializers.output.nifti_output_definition.NiftiOutputDefinitionSerializer`
class.
"""

from django_mri.models.outputs.nifti_output_definition import (
    NiftiOutputDefinition,
)
from rest_framework import serializers


class NiftiOutputDefinitionSerializer(serializers.ModelSerializer):
    """
    Serializer for the
    :class:`~django_mri.models.outputs.nifti_output_definition.NiftiOutputDefinition`
    model.
    """

    class Meta:
        model = NiftiOutputDefinition
        fields = "__all__"
