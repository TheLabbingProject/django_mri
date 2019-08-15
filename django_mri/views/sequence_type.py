from django_mri.filters.sequence_type_filter import SequenceTypeFilter
from django_mri.models.sequence_type import SequenceType
from django_mri.serializers import SequenceTypeSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class SequenceTypeViewSet(DefaultsMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = SequenceType.objects.all()
    serializer_class = SequenceTypeSerializer
    filter_class = SequenceTypeFilter
