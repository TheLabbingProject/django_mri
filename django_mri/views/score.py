"""
Definition of the :class:`ScoreViewSet` class.
"""
from django_mri.filters.score_filter import ScoreFilter
from django_mri.models.score import Score
from django_mri.serializers.score import ScoreSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class ScoreViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows scores to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Score.objects.order_by("-run")
    serializer_class = ScoreSerializer
    filter_class = ScoreFilter
    search_fields = (
        "id",
        "origin__id",
        "region__atlas__title",
        "run__id",
        "region__title",
        "metric__title",
        "origin__description",
    )
    ordering_fields = (
        "id",
        "run__id",
        "metric__title",
        "region__index",
        "region__hemisphere",
        "region__title",
        "region__atlas__title",
    )
