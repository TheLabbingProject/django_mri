"""
Definition of the
:class:`~django_mri.serializers.input.nifti_input_definition.NiftiInputDefinitionSerializer`
class.
"""

from rest_framework import serializers

from django_mri.models.inputs.nifti_input_definition import \
    NiftiInputDefinition


class NiftiInputDefinitionSerializer(serializers.ModelSerializer):
    """
    Serializer for the
    :class:`~django_mri.models.inputs.nifti_input_definition.NiftiInputDefinition`
    model.
    """

    class Meta:
        model = NiftiInputDefinition
        fields = "__all__"
