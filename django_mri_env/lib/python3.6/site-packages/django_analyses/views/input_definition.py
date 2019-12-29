from django_analyses.filters.input.input_definition import InputDefinitionFilter
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.serializers.input.definitions.input_definition import (
    InputDefinitionSerializer,
)
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class InputDefinitionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = InputDefinitionFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = InputDefinitionSerializer

    def get_queryset(self):
        return InputDefinition.objects.select_subclasses()
