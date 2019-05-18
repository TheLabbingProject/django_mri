from django_filters import rest_framework as filters
from django_dicom.models import Series


class UnreviewedDicomSeriesFilter(filters.FilterSet):
    class Meta:
        model = Series
        fields = ("patient__id",)
