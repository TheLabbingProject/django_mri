"""
Definition of the :class:`SessionViewSet` class.
"""
import io
import zipfile
from pathlib import Path
from typing import Tuple

from django.http import HttpResponse
from django_dicom.views.utils import CONTENT_DISPOSITION, ZIP_CONTENT_TYPE
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from django_mri.filters.session_filter import SessionFilter
from django_mri.models.session import Session
from django_mri.serializers import (AdminSessionReadSerializer,
                                    SessionReadSerializer,
                                    SessionWriteSerializer)
from django_mri.utils.utils import get_mri_root
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from django_mri.views.utils import ReadWriteSerializerMixin

ORDERING_FIELDS: Tuple[str] = (
    "id",
    "subject",
    "subject__id_number",
    "subject__first_name",
    "subject__last_name",
    "time__date",
    "time__time",
)
SEARCH_FIELDS: Tuple[str] = ("id", "subject", "comments", "time", "scan_set")


class SessionViewSet(
    DefaultsMixin, ReadWriteSerializerMixin, viewsets.ModelViewSet
):
    """
    API endpoint that allows :class:`~django_mri.models.session.Session`
    instances to be viewed and edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Session.objects.order_by("-time__date", "-time__time")
    write_serializer_class = SessionWriteSerializer
    filter_class = SessionFilter
    search_fields = SEARCH_FIELDS
    ordering_fields = ORDERING_FIELDS

    def get_read_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminSessionReadSerializer
        return SessionReadSerializer

    def filter_queryset(self, queryset):
        user = self.request.user
        queryset = super().filter_queryset(queryset)
        if user.is_superuser:
            return queryset
        user_collaborations = set(user.study_set.values_list("id", flat=True))
        by_procedure = queryset.filter(
            measurement__procedure__study__id__in=user_collaborations
        )
        by_scan_association = queryset.filter(
            scan__study_groups__study__id__in=user_collaborations
        )
        return (by_procedure | by_scan_association).distinct()

    @action(detail=True, methods=["get"])
    def dicom_zip(self, request: Request, pk: int) -> HttpResponse:
        instance = Session.objects.get(id=pk)
        subject = instance.subject.id_number
        date = instance.time.date().strftime("%Y%m%d")
        name = f"{date}_{subject}_{instance.id}"
        buffer = io.BytesIO()
        base_dir = Path(f"{date}_{instance.id}")
        with zipfile.ZipFile(buffer, "w") as zip_file:
            for scan in instance.scan_set.all():
                scan_base_dir = base_dir / f"{scan.number}_{scan.description}"
                for dcm in Path(scan.dicom.path).iterdir():
                    dcm_path = scan_base_dir / dcm.name
                    zip_file.write(dcm, dcm_path)
        response = HttpResponse(
            buffer.getvalue(), content_type=ZIP_CONTENT_TYPE
        )
        content_disposition = CONTENT_DISPOSITION.format(name=name)
        response["Content-Disposition"] = content_disposition
        return response

    @action(detail=True, methods=["get"])
    def nifti_zip(self, request: Request, pk: int) -> HttpResponse:
        instance = Session.objects.get(id=pk)
        buffer = io.BytesIO()
        nifti_root = get_mri_root() / "NIfTI"
        with zipfile.ZipFile(buffer, "w") as zip_file:
            for scan in instance.scan_set.all():
                try:
                    path = str(scan.nifti.path)
                except AttributeError:
                    continue
                relative_path = Path(path).relative_to(nifti_root)
                zip_file.write(path, relative_path)
        response = HttpResponse(
            buffer.getvalue(), content_type=ZIP_CONTENT_TYPE
        )
        name = str(instance.id)
        content_disposition = CONTENT_DISPOSITION.format(name=name)
        response["Content-Disposition"] = content_disposition
        return response
