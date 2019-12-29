from django_analyses.models.input.definitions.file_input_definition import (
    FileInputDefinition,
)
from rest_framework import serializers


class FileInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileInputDefinition
        fields = "__all__"
