from django_analyses.models.output.definitions.file_output_definition import (
    FileOutputDefinition,
)
from rest_framework import serializers


class FileOutputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileOutputDefinition
        fields = "__all__"
