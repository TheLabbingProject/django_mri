from django_filters import rest_framework as filters
from django_mri.models.scan import Scan


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


def filter_by_sequence_type(queryset, field_name, value):
    value = [int(pk) for pk in value]
    filtered_scan_ids = [
        scan.id
        for scan in queryset
        if scan.sequence_type and scan.sequence_type.id in value
    ]
    if -1 in value:
        filtered_scan_ids += [scan.id for scan in queryset if not scan.sequence_type]
    return queryset.filter(id__in=filtered_scan_ids)


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
    scan_time = filters.DateTimeFromToRangeFilter("time")
    created = filters.DateTimeFromToRangeFilter("created")
    institution_name = filters.AllValuesFilter("institution_name")
    dicom_id_in = NumberInFilter(field_name="dicom__id", lookup_expr="in")
    sequence_type = NumberInFilter(method=filter_by_sequence_type)

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
            "institution_name",
            "is_updated_from_dicom",
            "dicom__id",
            "subject",
        )

