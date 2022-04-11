"""
Definition of the :class:`AtlasFilter` class.
"""
from django_filters import rest_framework as filters
from django_mri.filters.utils import LOOKUP_CHOICES
from django_mri.models.atlas import Atlas


class AtlasFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_dicom.models.atlas.Atlas` class.
    """

    title = filters.LookupChoiceFilter("title", lookup_choices=LOOKUP_CHOICES,)
    description = filters.LookupChoiceFilter(
        "description", lookup_choices=LOOKUP_CHOICES,
    )
    symmetric = filters.BooleanFilter("symmetric")

    class Meta:
        model = Atlas
        fields = ("id", "title", "description", "symmetric")
