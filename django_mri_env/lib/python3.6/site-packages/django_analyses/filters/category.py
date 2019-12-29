from django_analyses.models.category import Category
from django_filters import rest_framework as filters


class CategoryFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.category.Category`
    model.

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
    parent = filters.CharFilter(field_name="parent__title")
    is_root = filters.BooleanFilter(field_name="parent", method="filter_is_root")

    class Meta:
        model = Category
        fields = "id", "title", "description", "parent", "is_root"

    def filter_is_root(self, queryset, name: str, value: bool):
        return queryset.filter(parent__isnull=value)
