from django.db import models
from django_analyses.models.input.types.number_input import NumberInput
from django_analyses.models.input.types.input_types import InputTypes


class FloatInput(NumberInput):
    value = models.FloatField()
    definition = models.ForeignKey(
        "django_analyses.FloatInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def get_type(self) -> InputTypes:
        return InputTypes.FLT
