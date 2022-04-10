"""
Definition of the :class:`RegionFilter` class.
"""
from django_filters import rest_framework as filters
from django_mri.filters.scan_filter import NumberInFilter
from django_mri.filters.utils import LOOKUP_CHOICES
from django_mri.models.region import Region


class RegionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_dicom.models.region.Region` class.
    """

    atlas = NumberInFilter(
        field_name="atlas", lookup_expr="in", label="Atlas ID is in",
    )
    title = filters.LookupChoiceFilter("title", lookup_choices=LOOKUP_CHOICES,)
    description = filters.LookupChoiceFilter(
        "description", lookup_choices=LOOKUP_CHOICES,
    )

    class Meta:
        model = Region
        fields = (
            "id",
            "title",
            "description",
            "index",
            "subcortical",
        )
