from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)
from rest_framework import serializers


class StringInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringInputDefinition
        fields = "__all__"
