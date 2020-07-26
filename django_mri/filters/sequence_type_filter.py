from django_filters import rest_framework as filters
from django_mri.models import SequenceType


class CharArrayFilter(filters.BaseCSVFilter, filters.CharFilter):
    pass


class SequenceTypeFilter(filters.FilterSet):
    scanning_sequence = CharArrayFilter(
        "sequence_definition_set__scanning_sequence", lookup_expr="exact"
    )
    sequence_variant = CharArrayFilter(
        "sequence_definition_set__sequence_variant", lookup_expr="exact"
    )

    class Meta:
        model = SequenceType
        fields = ("scanning_sequence", "sequence_variant")
