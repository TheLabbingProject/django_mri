from django.core.exceptions import ValidationError
from django_analyses.models.input.input import Input


class NumberInput(Input):
    def validate_min_value(self) -> bool:
        min_value = self.definition.min_value
        return self.value >= min_value if min_value or min_value == 0 else True

    def raise_min_value_error(self) -> None:
        key = self.definition.key
        min_value = self.definition.min_value
        raise ValidationError(f"{key} must be greater than {min_value}!")

    def validate_max_value(self) -> bool:
        max_value = self.definition.max_value
        return self.value <= max_value if max_value or max_value == 0 else True

    def raise_max_value_error(self) -> None:
        key = self.definition.key
        max_value = self.definition.max_value
        raise ValidationError(f"{key} must be less than {max_value}!")

    def validate(self) -> None:
        if not self.valid_min_value:
            self.raise_min_value_error()
        if not self.valid_max_value:
            self.raise_max_value_error()

    @property
    def valid_min_value(self) -> bool:
        return self.validate_min_value()

    @property
    def valid_max_value(self) -> bool:
        return self.validate_max_value()

