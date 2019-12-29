from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_filters import rest_framework as filters


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class InputDefinitionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
    model.

    """

    input_specification = filters.AllValuesFilter("inputspecification")

    class Meta:
        model = InputDefinition
        fields = "key", "required", "is_configuration", "input_specification"

