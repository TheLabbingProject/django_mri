from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import ModelFormMixin
from django_dicom.models import Series, Patient
from django_mri.filters.django_dicom import UnreviewedDicomSeriesFilter
from django_mri.filters.scan_filter import ScanFilter
from django_mri.forms import ScanReview
from django_mri.models import Scan
from django_mri.serializers import (
    ScanSerializer,
    DicomSeriesToTreeNode,
    DicomPatientToTreeNode,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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
    filter_class = UnreviewedDicomSeriesFilter


class CreateScanView(CreateView, ModelFormMixin, LoginRequiredMixin):
    model = Scan
    form_class = ScanReview
    success_url = "/data_review/"
    template_name = "django_mri/scan/create_scan.html"


class CreateScanFromDicom(CreateScanView):
    def get_context_data(self, **kwargs):
        series = Series.objects.get(id=self.kwargs.get("pk"))
        self.object = Scan(dicom=series)
        self.object.update_fields_from_dicom()
        return super().get_context_data(**kwargs)

