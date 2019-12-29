from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import JSONField
from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes
from django_analyses.models.input.utils import ListElementTypes, TYPES_DICT


class ListInput(Input):
    value = JSONField()
    definition = models.ForeignKey(
        "django_analyses.ListInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def validate_min_length(self) -> bool:
        min_length = self.definition.min_length
        return len(self.value) >= min_length if min_length else True

    def raise_min_length_error(self) -> None:
        key = self.definition.key
        min_length = self.definition.min_length
        raise ValidationError(f"'{key}' must have at least {min_length} elements!")

    def validate_max_length(self) -> bool:
        max_length = self.definition.max_length
        return len(self.value) <= max_length if max_length else True

    def raise_max_length_error(self) -> None:
        key = self.definition.key
        max_length = self.definition.max_length
        raise ValidationError(f"'{key}' must have at most {max_length} elements!")

    def raise_not_list_error(self) -> None:
        raise ValidationError("ListInput value must be a list instance!")

    def raise_incorrect_type_error(self) -> None:
        raise ValidationError(f"List elements must be of type {self.expected_type}!")

    def validate(self) -> None:
        if not isinstance(self.value, list):
            self.raise_not_list_error()
        if not self.valid_elements:
            self.raise_incorrect_type_error()
        if not self.valid_min_length:
            self.raise_min_length_error()
        if not self.valid_max_length:
            self.raise_max_length_error()

    def get_type(self) -> InputTypes:
        return InputTypes.LST

    @property
    def expected_type_definition(self) -> ListElementTypes:
        return ListElementTypes[self.definition.element_type]

    @property
    def expected_type(self) -> type:
        return TYPES_DICT[self.expected_type_definition]

    @property
    def type_validation_by_element(self) -> list:
        return [isinstance(element, self.expected_type) for element in self.value]

    @property
    def valid_elements(self) -> bool:
        return all(self.type_validation_by_element)

    @property
    def valid_min_length(self) -> bool:
        return self.validate_min_length()

    @property
    def valid_max_length(self) -> bool:
        return self.validate_max_length()
