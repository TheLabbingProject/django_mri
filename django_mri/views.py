import os

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_mri.data_import import ImportScan, LocalImport
from django_dicom.models import Series
from django_filters.rest_framework import DjangoFilterBackend
from django_mri.filters.scan_filter import ScanFilter
from django_mri.filters.sequence_type_filter import SequenceTypeFilter
from django_mri.models import Scan, NIfTI
from django_mri.models.sequence_type import SequenceType
from django_mri.serializers import (
    NiftiSerializer,
    ScanSerializer,
    SequenceTypeSerializer,
)
from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

subject_app_label, subject_model_name = settings.SUBJECT_MODEL.split(".")
Subject = apps.get_model(app_label=subject_app_label, model_name=subject_model_name)


class DefaultsMixin:
    """
    Default settings for view authentication, permissions and filtering.
    
    """

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"


class ScanViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    queryset = Scan.objects.all().order_by("-time")
    serializer_class = ScanSerializer
    filter_class = ScanFilter
    pagination_class = StandardResultsSetPagination
    search_fields = (
        "id",
        "description",
        "number",
        "created",
        "scan_time",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "sequence_type",
        "spatial_resolution",
        "institution_name",
        "is_updated_from_dicom",
    )
    ordering_fields = (
        "id",
        "description",
        "number",
        "created",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "sequence_type",
        "spatial_resolution",
        "institution_name",
    )

    @action(detail=False, methods=["POST"])
    def from_file(self, request):
        file_obj = request.data["file"]
        subject = Subject.objects.get(id=request.data["subject_id"])

        if file_obj.name.endswith(".dcm"):
            scan, created = ImportScan(subject, file_obj).run()
            serializer = ScanSerializer(scan, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif file_obj.name.endswith(".zip"):
            content = ContentFile(file_obj.read())
            temp_file_name = default_storage.save("tmp.zip", content)
            temp_file_path = os.path.join(settings.MEDIA_ROOT, temp_file_name)
            LocalImport(subject, temp_file_path).run()
            os.remove(temp_file_path)
            return Response(
                {"message": "Successfully imported ZIP archive!"},
                status=status.HTTP_201_CREATED,
            )

    @action(detail=True, methods=["GET"])
    def from_dicom(self, request, series_id: int = None, subject_id: int = None):
        try:
            series = Series.objects.get(id=series_id)
        except ObjectDoesNotExist:
            return Response(
                "Invalid DICOM primary key!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            scan = Scan.objects.get(dicom=series)
            return Response(
                ScanSerializer(scan, context={"request": request}).validated_data
            )
        except ObjectDoesNotExist:
            scan = Scan(dicom=series)
            scan.update_fields_from_dicom()
            serializer = ScanSerializer(scan, context={"request": request})
            return Response(serializer.data)


class NiftiViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = NIfTI.objects.all()
    serializer_class = NiftiSerializer


class SequenceTypeViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = SequenceType.objects.all()
    serializer_class = SequenceTypeSerializer
    filter_class = SequenceTypeFilter
