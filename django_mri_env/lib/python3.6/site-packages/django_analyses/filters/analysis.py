from django_analyses.models.analysis import Analysis
from django_filters import rest_framework as filters


class AnalysisFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.analysis.Analysis` model.

    """

    title = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    description = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    created = filters.DateTimeFromToRangeFilter("created")

    class Meta:
        model = Analysis
        fields = "id", "title", "description", "created"

