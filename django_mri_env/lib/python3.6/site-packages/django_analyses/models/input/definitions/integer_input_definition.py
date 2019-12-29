from django.db import models
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.types.integer_input import IntegerInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions


class IntegerInputDefinition(InputDefinition):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)
    default = models.IntegerField(blank=True, null=True)

    INPUT_CLASS = IntegerInput

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.INT
