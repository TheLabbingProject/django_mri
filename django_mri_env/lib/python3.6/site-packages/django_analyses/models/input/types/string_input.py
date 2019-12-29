from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes
from pathlib import Path


class StringInput(Input):
    value = models.CharField(max_length=1000)
    definition = models.ForeignKey(
        "django_analyses.StringInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def validate_min_length(self) -> bool:
        min_length = self.definition.min_length
        return len(self.value) >= min_length if min_length else True

    def raise_min_length_error(self) -> None:
        min_length = self.definition.min_length
        raise ValidationError(f"{self.key} must be {min_length} characters or longer!")

    def validate_max_length(self) -> bool:
        max_length = self.definition.max_length
        return len(self.value) <= max_length if max_length else True

    def raise_max_length_error(self) -> None:
        max_length = self.definition.max_length
        raise ValidationError(f"{self.key} must be {max_length} characters or shorter!")

    def validate_from_choices(self) -> bool:
        choices = self.definition.choices
        return self.value in choices if choices else True

    def raise_invalid_choice_error(self) -> None:
        choices = self.definition.choices
        raise ValidationError(
            f"{self.key} must be one of the following choices: {choices}!"
        )

    def fix_output_path(self) -> str:
        if self.value:
            if not Path(self.value).is_absolute():
                path = self.default_output_directory / self.value
        else:
            if self.definition.default:
                path = self.default_output_directory / self.definition.default
            else:
                path = self.default_output_directory / self.definition.key
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path)

    def pre_save(self) -> None:
        if self.definition.is_output_path:
            self.value = self.fix_output_path()

    def validate(self) -> None:
        if not self.valid_min_length:
            self.raise_min_length_error()
        if not self.valid_max_length:
            self.raise_max_length_error()
        if not self.valid_choice:
            self.raise_invalid_choice_error()

    def get_type(self) -> InputTypes:
        return InputTypes.STR

    @property
    def valid_min_length(self) -> bool:
        return self.validate_min_length()

    @property
    def valid_max_length(self) -> bool:
        return self.validate_max_length()

    @property
    def valid_choice(self) -> bool:
        return self.validate_from_choices()

    @property
    def default_output_directory(self) -> Path:
        return Path(settings.ANALYSIS_BASE_PATH) / str(self.run.id)
