from django_analyses.models.input.definitions.integer_input_definition import (
    IntegerInputDefinition,
)
from rest_framework import serializers


class IntegerInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegerInputDefinition
        fields = "__all__"

