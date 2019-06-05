from django_dicom.models import Series, Patient
from django_dicom.serializers import PatientSerializer, SeriesSerializer
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
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class DefaultsMixin:
    """
    Default settings for view authentication, permissions, filtering and pagination.
    
    """

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    paginate_by = 25
    paginate_by_param = "page_size"
    max_paginate_by = 100
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)


class ScanViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    queryset = Scan.objects.all().order_by("-time")
    serializer_class = ScanSerializer
    filter_class = ScanFilter
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

    # Should be removed (remained from previous workflow)
    @action(detail=False)
    def get_fields_from_dicom_series(self, request, series_id: int):
        series = Series.objects.get(id=series_id)
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


class UnreviewedDicomPatientViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):
        patients_with_unreviewed_series = (
            Series.objects.filter(scan__isnull=True)
            .order_by()
            .values_list("patient", flat=True)
            .distinct()
        )
        return Patient.objects.filter(id__in=patients_with_unreviewed_series)


class UnreviewedDicomSeriesViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Series.objects.filter(scan__isnull=True)
    serializer_class = SeriesSerializer
    filter_fields = ("patient__id",)
