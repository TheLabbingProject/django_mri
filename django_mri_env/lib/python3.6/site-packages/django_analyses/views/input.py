from django_analyses.filters.input.input import InputFilter
from django_analyses.models.input.input import Input
from django_analyses.serializers.input.input import InputSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class InputViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = InputFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = InputSerializer

    def get_queryset(self):
        return Input.objects.select_subclasses()
