from django_filters import rest_framework as filters
from django_mri.models.scan import Scan


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class ScanFilter(filters.FilterSet):
    """
    Provides useful filtering options for the :class:`~django_dicom.models.series.Series`
    class.
    
    """

    description = filters.LookupChoiceFilter(
        "description",
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ],
    )
    number = filters.NumberFilter("number")
    # sequence_type = filters.AllValuesMultipleFilter("sequence_type")
    # spatial_resolution = filters.AllValuesFilter("spatial_resolution")
    scan_time = filters.DateTimeFromToRangeFilter("time")
    created = filters.DateTimeFromToRangeFilter("created")
    institution_name = filters.AllValuesFilter("institution_name")
    dicom_id_in = NumberInFilter(field_name="dicom__id", lookup_expr="in")

    class Meta:
        model = Scan
        fields = (
            "id",
            "description",
            "number",
            "created",
            "scan_time",
            "echo_time",
            "inversion_time",
            "repetition_time",
            # "sequence_type",
            # "spatial_resolution",
            "institution_name",
            "is_updated_from_dicom",
            "dicom__id",
            "subject",
        )

