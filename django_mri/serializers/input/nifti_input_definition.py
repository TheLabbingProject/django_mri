from django_mri.models.inputs.nifti_input_definition import NiftiInputDefinition
from rest_framework import serializers


class NiftiInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiftiInputDefinition
        fields = "__all__"
