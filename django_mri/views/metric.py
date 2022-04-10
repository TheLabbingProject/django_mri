"""
Definition of the :class:`MetricViewSet` class.
"""
from django_mri.filters.metric_filter import MetricFilter
from django_mri.models.metric import Metric
from django_mri.serializers.metric import MetricSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class MetricViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows metrics to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Metric.objects.order_by("title")
    serializer_class = MetricSerializer
    filter_class = MetricFilter
    search_fields = "id", "title", "description"
    ordering_fields = "id", "title", "description"
