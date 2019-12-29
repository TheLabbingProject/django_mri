from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_filters import rest_framework as filters


class OutputDefinitionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
    model.
    
    """
    output_specification = filters.AllValuesFilter("outputspecification")

    class Meta:
        model = OutputDefinition
        fields = "key", "output_specification"
