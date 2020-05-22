from django_mri.models.outputs.nifti_output_definition import NiftiOutputDefinition
from rest_framework import serializers


class NiftiOutputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiftiOutputDefinition
        fields = "__all__"
