from django_analyses.filters.pipeline.pipeline import PipelineFilter
from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.serializers.pipeline.pipeline import PipelineSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class PipelineViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Pipeline.objects.all()
    filter_class = PipelineFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = PipelineSerializer
