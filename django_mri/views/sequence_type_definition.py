from django_mri.filters.sequence_type_definition_filter import (
    SequenceTypeDefinitionFilter,
)
from django_mri.models.sequence_type_definition import SequenceTypeDefinition
from django_mri.serializers import SequenceTypeDefinitionSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class SequenceTypeDefinitionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = SequenceTypeDefinition.objects.all()
    serializer_class = SequenceTypeDefinitionSerializer
    filter_class = SequenceTypeDefinitionFilter
