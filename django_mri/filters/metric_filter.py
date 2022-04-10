"""
Definition of the :class:`MetricFilter` class.
"""
from django_filters import rest_framework as filters
from django_mri.filters.utils import LOOKUP_CHOICES
from django_mri.models.metric import Metric


class MetricFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_dicom.models.metric.Metric` class.
    """

    title = filters.LookupChoiceFilter("title", lookup_choices=LOOKUP_CHOICES,)
    description = filters.LookupChoiceFilter(
        "description", lookup_choices=LOOKUP_CHOICES,
    )

    class Meta:
        model = Metric
        fields = (
            "id",
            "title",
            "description",
        )
