from django.db import models
from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes


class BooleanInput(Input):
    value = models.BooleanField()
    definition = models.ForeignKey(
        "django_analyses.BooleanInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def get_type(self) -> InputTypes:
        return InputTypes.BLN
