"""
Definition of the :class:`SessionFilter` class.
"""

from django_filters import rest_framework as filters
from django_mri.filters.scan_filter import NumberInFilter
from django_mri.models.session import Session


class SessionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_dicom.models.session.Session` class.

    """

    comments = filters.LookupChoiceFilter(
        "comments",
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ],
    )
    session_date = filters.DateTimeFromToRangeFilter("time__date")
    subject_id_in = NumberInFilter(field_name="subject__id", lookup_expr="in")
    scan_set = NumberInFilter(field_name="scan_set", method="in")
    id_in = NumberInFilter(field_name="id", lookup_expr="in")

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
