from django_analyses.filters.output.output_definition import OutputDefinitionFilter
from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_analyses.serializers.output.definitions.output_definition import (
    OutputDefinitionSerializer,
)
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class OutputDefinitionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = OutputDefinitionFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = OutputDefinitionSerializer

    def get_queryset(self):
        return OutputDefinition.objects.select_subclasses()
