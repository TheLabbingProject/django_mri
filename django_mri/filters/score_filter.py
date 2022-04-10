"""
Definition of the :class:`ScoreFilter` class.
"""
from django_analyses.models.run import Run
from django_filters import rest_framework as filters
from django_mri.models.metric import Metric
from django_mri.models.region import Region
from django_mri.models.scan import Scan
from django_mri.models.score import Score


class ScoreFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_dicom.models.score.Score` class.
    """

    origin = filters.ModelMultipleChoiceFilter(queryset=Scan.objects.all())
    region = filters.ModelMultipleChoiceFilter(queryset=Region.objects.all())
    metric = filters.ModelMultipleChoiceFilter(queryset=Metric.objects.all())
    run = filters.ModelMultipleChoiceFilter(queryset=Run.objects.all())

    class Meta:
        model = Score
        fields = (
            "id",
            "origin",
            "region",
            "metric",
            "run",
        )
