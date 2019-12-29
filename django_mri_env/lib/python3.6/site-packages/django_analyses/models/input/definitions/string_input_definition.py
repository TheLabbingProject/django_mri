from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.types.string_input import StringInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions


class StringInputDefinition(InputDefinition):
    min_length = models.IntegerField(blank=True, null=True)
    max_length = models.IntegerField(blank=True, null=True)
    default = models.CharField(max_length=500, blank=True, null=True)
    choices = ArrayField(
        models.CharField(max_length=255, blank=True, null=True), blank=True, null=True
    )
    is_output_path = models.BooleanField(default=False)

    INPUT_CLASS = StringInput

    def raise_default_not_in_choices_error(self) -> None:
        raise ValidationError(_(f"{self.default} not in {self.choices}!"))

    def validate(self) -> None:
        if self.default and self.choices:
            if self.default not in self.choices:
                self.raise_default_not_in_choices_error()

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.STR
