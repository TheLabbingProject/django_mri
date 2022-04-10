"""
Definition of the :class:`IrbApprovalFilter` class.
"""
from django_filters import rest_framework as filters
from django_mri.filters.utils import LOOKUP_CHOICES
from django_mri.models.irb_approval import IrbApproval


class IrbApprovalFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_dicom.models.irb_approval.IrbApproval` class.
    """

    institution = filters.LookupChoiceFilter(
        "institution", lookup_choices=LOOKUP_CHOICES,
    )

    number = filters.LookupChoiceFilter(
        "number", lookup_choices=LOOKUP_CHOICES,
    )

    class Meta:
        model = IrbApproval
        fields = (
            "id",
            "institution",
            "number",
        )
