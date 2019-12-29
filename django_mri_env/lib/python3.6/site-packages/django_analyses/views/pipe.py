from django_analyses.filters.pipeline.pipe import PipeFilter
from django_analyses.models.pipeline.pipe import Pipe
from django_analyses.serializers.pipeline.pipe import PipeSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class PipeViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Pipe.objects.all()
    filter_class = PipeFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = PipeSerializer
