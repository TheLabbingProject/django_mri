from django_analyses.filters.output.output import OutputFilter
from django_analyses.models.output.output import Output
from django_analyses.serializers.output.output import OutputSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class OutputViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = OutputFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = OutputSerializer

    def get_queryset(self):
        return Output.objects.select_subclasses()
