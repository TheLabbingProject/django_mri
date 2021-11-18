"""
Definition of the :class:`ScanFilter` class.
"""
from django_dicom.models.utils.sequence_type import SEQUENCE_TYPE_CHOICES
from django_filters import rest_framework as filters

from django_mri.filters.utils import LOOKUP_CHOICES, NumberInFilter
from django_mri.models.scan import Scan
from django_mri.utils.utils import get_group_model

Group = get_group_model()


class ScanFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_dicom.models.scan.Scan` class.
    """

    description = filters.LookupChoiceFilter(
        "description", lookup_choices=LOOKUP_CHOICES,
    )
    number = filters.NumberFilter("number")
    scan_time = filters.DateTimeFromToRangeFilter("time")
    created = filters.DateTimeFromToRangeFilter("created")
    institution_name = filters.AllValuesFilter("institution_name")
    dicom_id_in = NumberInFilter(field_name="dicom__id", lookup_expr="in")
    sequence_type = filters.MultipleChoiceFilter(
        field_name="dicom__sequence_type",
        # Exclude the null value choices because it doesn't seem to integrate
        # well with DRF.
        choices=SEQUENCE_TYPE_CHOICES[:-1],
        # Create DRF compatible null filter.
        null_value=None,
        null_label="Unknown",
    )
    subject_id_number = filters.LookupChoiceFilter(
        "session__subject__id_number", lookup_choices=LOOKUP_CHOICES,
    )
    subject_first_name = filters.LookupChoiceFilter(
        "session__subject__first_name", lookup_choices=LOOKUP_CHOICES,
    )
    subject_last_name = filters.LookupChoiceFilter(
        "session__subject__last_name", lookup_choices=LOOKUP_CHOICES,
    )
    study_groups = filters.ModelMultipleChoiceFilter(
        queryset=Group.objects.all()
    )

    class Meta:
        model = Scan
        fields = (
            "id",
            "echo_time",
            "inversion_time",
            "repetition_time",
            "is_updated_from_dicom",
            "dicom__id",
            "session",
        )
