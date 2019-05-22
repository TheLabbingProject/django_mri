from django_dicom.models import Series, Patient
from django_mri.filters.scan_filter import ScanFilter
from django_mri.models import Scan, NIfTI
from django_mri.models.sequence_type import SequenceType
from django_mri.serializers import (
    ScanSerializer,
    NiftiSerializer,
    SequenceTypeSerializer,
    DicomSeriesToTreeNode,
    DicomPatientToTreeNode,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, filters, permissions, viewsets


class DefaultsMixin:
    """
    Default settings for view authentication, permissions, filtering and pagination.
    
    """

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 25
    paginate_by_param = "page_size"
    max_paginate_by = 100
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


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


class NiftiViewSet(viewsets.ModelViewSet):
    queryset = NIfTI.objects.all()
    serializer_class = NiftiSerializer


class SequenceTypeViewSet(viewsets.ModelViewSet):
    queryset = SequenceType.objects.all()
    serializer_class = SequenceTypeSerializer


class UnreviewedDicomPatientViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = DicomPatientToTreeNode

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
    serializer_class = DicomSeriesToTreeNode
    filter_fields = ("patient__id",)

