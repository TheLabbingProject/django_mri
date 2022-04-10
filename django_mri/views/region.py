"""
Definition of the :class:`RegionViewSet` class.
"""
from django_mri.filters.region_filter import RegionFilter
from django_mri.models.region import Region
from django_mri.serializers.region import RegionSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class RegionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows regions to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Region.objects.order_by("atlas", "hemisphere", "index", "title")
    serializer_class = RegionSerializer
    filter_class = RegionFilter
    search_fields = "id", "title", "description", "index"
    ordering_fields = (
        "id",
        "title",
        "description",
        "hemisphere",
        "index",
        "subcortical",
    )
