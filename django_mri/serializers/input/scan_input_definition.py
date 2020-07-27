"""
Definition of the
:class:`~django_mri.serializers.input.scan_input_definition.ScanInputDefinitionSerializer`
class.
"""

from django_mri.models.inputs.scan_input_definition import ScanInputDefinition
from rest_framework import serializers


class ScanInputDefinitionSerializer(serializers.ModelSerializer):
    """
    Serializer for the
    :class:`~django_mri.models.inputs.scan_input_definition.ScanInputDefinition`
    model.
    """

    class Meta:
        model = ScanInputDefinition
        fields = "__all__"
