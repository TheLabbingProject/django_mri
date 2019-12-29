from django_analyses.models.input.definitions.float_input_definition import (
    FloatInputDefinition,
)
from rest_framework import serializers


class FloatInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatInputDefinition
        fields = "__all__"
