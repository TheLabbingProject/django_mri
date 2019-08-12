from django_filters import rest_framework as filters
from django_mri.models.sequence_type import SequenceType


class CharArrayFilter(filters.BaseCSVFilter, filters.CharFilter):
    pass


class SequenceTypeFilter(filters.FilterSet):
    scanning_sequence = CharArrayFilter("scanning_sequence", lookup_expr="exact")
    sequence_variant = CharArrayFilter("sequence_variant", lookup_expr="exact")

    class Meta:
        model = SequenceType
        fields = ("title", "scanning_sequence", "sequence_variant")
