from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_analyses.models.managers.input_specification import (
    InputSpecificationManager,
)
from django_extensions.db.models import TimeStampedModel


class InputSpecification(TimeStampedModel):
    analysis = models.ForeignKey("django_analyses.Analysis", on_delete=models.CASCADE)
    base_input_definitions = models.ManyToManyField("django_analyses.InputDefinition")

    objects = InputSpecificationManager()

    def __str__(self) -> str:
        formatted_definitions = "\n\t".join(
            [str(definition) for definition in self.input_definitions]
        )
        return f"\n[{self.analysis}]\n\t{formatted_definitions}\n"

    def get_default_input_configurations(self) -> dict:
        return {
            definition.key: definition.default
            for definition in self.input_definitions
            if definition.default is not None
        }

    def validate_keys(self, **kwargs) -> None:
        for key in kwargs:
            try:
                self.input_definitions.get(key=key)
            except ObjectDoesNotExist:
                raise ValidationError(_(f"Invalid input key: '{key}'!"))

    def validate_required(self, **kwargs) -> None:
        for key in self.required_keys:
            if key not in kwargs:
                raise ValidationError(_(f"Value for '{key}' must be provided!"))

    def validate_kwargs(self, **kwargs) -> None:
        self.validate_keys(**kwargs)
        self.validate_required(**kwargs)

    @property
    def default_configuration(self) -> dict:
        return self.get_default_input_configurations()

    @property
    def input_definitions(self) -> models.QuerySet:
        return self.base_input_definitions.select_subclasses()

    @property
    def required_keys(self) -> list:
        required_definitions = self.input_definitions.filter(required=True)
        required_keys = required_definitions.values_list("key", flat=True)
        return list(required_keys)

