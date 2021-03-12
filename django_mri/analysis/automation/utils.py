from django.db.models import Q, QuerySet
from django_mri.models.scan import Scan

MPRAGE_FILTER = {
    "dicom__scanning_sequence": ["GR", "IR"],
    "dicom__sequence_variant": ["SK", "SP", "MP"],
}
ANATOMICAL_QUERY = Q(**MPRAGE_FILTER) | Q(description__icontains="SPGR")


def get_anatomicals() -> QuerySet:
    return Scan.objects.filter(ANATOMICAL_QUERY).order_by("-time")
