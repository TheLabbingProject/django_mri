from django_analyses.filters.analysis import AnalysisFilter
from django_analyses.models.analysis import Analysis
from django_analyses.serializers.analysis import AnalysisSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class AnalysisViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = AnalysisFilter
    pagination_class = StandardResultsSetPagination
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

