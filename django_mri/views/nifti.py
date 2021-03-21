import io
import zipfile
from pathlib import Path

from django.http import HttpResponse
from django_mri.models import NIfTI
from django_mri.serializers import NiftiSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

CONTENT_DISPOSITION = "attachment; filename={instance_id}.zip"
ZIP_CONTENT_TYPE = "application/x-zip-compressed"


class NiftiViewSet(DefaultsMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = NIfTI.objects.all()
    serializer_class = NiftiSerializer

    @action(detail=True, methods=["get"])
    def to_zip(self, request: Request, pk: int) -> HttpResponse:
        instance = NIfTI.objects.get(id=pk)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zip_file:
            nii_name = Path(instance.path).name
            zip_file.write(instance.path, nii_name)
            if instance.json_file.exists():
                json_name = Path(instance.json_file).name
                zip_file.write(instance.json_file, json_name)
        response = HttpResponse(
            buffer.getvalue(), content_type=ZIP_CONTENT_TYPE
        )
        content_disposition = CONTENT_DISPOSITION.format(
            instance_id=instance.id
        )
        response["Content-Disposition"] = content_disposition
        return response
