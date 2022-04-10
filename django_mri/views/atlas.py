"""
Definition of the :class:`AtlasViewSet` class.
"""
from django_mri.filters.atlas_filter import AtlasFilter
from django_mri.models.atlas import Atlas
from django_mri.serializers.atlas import AtlasSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class AtlasViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows atlases to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Atlas.objects.order_by("title")
    serializer_class = AtlasSerializer
    filter_class = AtlasFilter
    search_fields = "id", "title", "description"
    ordering_fields = "id", "title", "description", "symmetric"
