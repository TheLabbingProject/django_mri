from django_filters import rest_framework as filters

LOOKUP_CHOICES = [
    ("contains", "Contains (case-sensitive)"),
    ("icontains", "Contains (case-insensitive)"),
    ("exact", "Exact"),
]


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass
