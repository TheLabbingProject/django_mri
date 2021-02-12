from django.db.models import QuerySet
from django_mri.models.scan import Scan


def get_mprage() -> QuerySet:
    return Scan.objects.filter(description__icontains="mprage").order_by(
        "-time"
    )
