"""
Definition of the :class:`SessionViewSet` class.
"""
import io
import zipfile
from pathlib import Path

from django.http import HttpResponse
from django_dicom.views.utils import CONTENT_DISPOSITION, ZIP_CONTENT_TYPE
from django_mri.filters.session_filter import SessionFilter
from django_mri.models.session import Session
from django_mri.serializers import (
    SessionReadSerializer,
    SessionWriteSerializer,
)
from django_mri.utils.utils import get_mri_root
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from django_mri.views.utils import ReadWriteSerializerMixin
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request


class SessionViewSet(
    DefaultsMixin, ReadWriteSerializerMixin, viewsets.ModelViewSet
):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Session.objects.order_by("-time__date", "-time__time")
    read_serializer_class = SessionReadSerializer
    write_serializer_class = SessionWriteSerializer
    filter_class = SessionFilter
    search_fields = ("id", "subject", "comments", "time", "scan_set")
    ordering_fields = (
        "id",
        "subject",
        "time__date",
        "time__time",
    )

    def filter_queryset(self, queryset):
        user = self.request.user
        queryset = super().filter_queryset(queryset)
        if user.is_superuser:
            return queryset
        user_collaborations = set(user.study_set.values_list("id", flat=True))
        ids = [
            session.id
            for session in queryset
            if any(
                [
                    study_id in user_collaborations
                    for study_id in session.query_studies(id_only=True)
                ]
            )
        ]
        return queryset.filter(id__in=ids)

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
