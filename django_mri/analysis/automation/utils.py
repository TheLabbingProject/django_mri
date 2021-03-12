from django.db.models import Q, QuerySet
from django_mri.models.scan import Scan

MPRAGE_FILTER = {
    "dicom__scanning_sequence": ["GR", "IR"],
    "dicom__sequence_variant": ["SK", "SP", "MP"],
}
ANATOMICAL_QUERY = Q(**MPRAGE_FILTER) | Q(description__icontains="SPGR")


def get_t1_weighted() -> QuerySet:
    return Scan.objects.filter(ANATOMICAL_QUERY).order_by("-time")


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
