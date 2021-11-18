"""
Definition of the :class:`SessionFilter` class.
"""
from typing import List

from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from django_mri.filters.scan_filter import NumberInFilter
from django_mri.filters.utils import LOOKUP_CHOICES
from django_mri.models.session import Session


class SessionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_dicom.models.session.Session` class.
    """

    comments = filters.LookupChoiceFilter(
        "comments", lookup_choices=LOOKUP_CHOICES,
    )
    session_date = filters.DateTimeFromToRangeFilter("time__date")
    id_in = NumberInFilter(
        field_name="id", lookup_expr="in", label="Session ID is in"
    )
    study_id_in = NumberInFilter(
        lookup_expr="in",
        label="Associated Study ID is in",
        method="filter_by_study_association",
    )
    subject_id_in = NumberInFilter(
        field_name="subject__id", lookup_expr="in", label="Subject ID is in"
    )
    scan_set = NumberInFilter(
        field_name="scan_set", method="in", label="Contains scan IDs"
    )
    subject_id_number = filters.LookupChoiceFilter(
        "subject__id_number", lookup_choices=LOOKUP_CHOICES,
    )
    subject_first_name = filters.LookupChoiceFilter(
        "subject__first_name", lookup_choices=LOOKUP_CHOICES,
    )
    subject_last_name = filters.LookupChoiceFilter(
        "subject__last_name", lookup_choices=LOOKUP_CHOICES,
    )

    class Meta:
        model = Session
        fields = (
            "id",
            "subject",
            "comments",
            "time",
            "scan_set",
            "session_date",
        )

    def filter_by_study_association(
        self, queryset: QuerySet, name: str, value: List[str]
    ):
        query = Q(scan__study_groups__study__id__in=value) | Q(
            measurement__procedure__study__id__in=value
        )
        return queryset.filter(query).distinct()
