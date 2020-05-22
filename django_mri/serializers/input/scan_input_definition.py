from django_mri.models.inputs.scan_input_definition import ScanInputDefinition
from rest_framework import serializers


class ScanInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanInputDefinition
        fields = "__all__"
