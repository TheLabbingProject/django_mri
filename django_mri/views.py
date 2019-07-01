from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_dicom.data_import import ImportImage
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
from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

subject_app_label, subject_model_name = settings.SUBJECT_MODEL.split(".")
Subject = apps.get_model(app_label=subject_app_label, model_name=subject_model_name)


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

    # def put(self, request, format=None):
    #     file_obj = request.data["file"]
    #     if file_obj.name.endswith(".dcm"):
    #         dicom_image, created = ImportImage(file_obj).run()
    #         scan, created = Scan.objects.get_or_create(dicom=dicom_image)
    #         if created:
    #             scan.update_fields_from_dicom()
    #     # elif file_obj.name.endswith(".zip"):
    #     #     content = ContentFile(file_obj.read())
    #     #     temp_file_name = default_storage.save("tmp.zip", content)
    #     #     temp_file_path = opj(settings.MEDIA_ROOT, temp_file_name)
    #     #     LocalImport.import_local_zip_archive(temp_file_path, verbose=False)
    #     #     return Response(
    #     #         {"message": "Successfully imported ZIP archive!"},
    #     #         status=status.HTTP_201_CREATED,
    #     #     )
    #     if created:
    #         return Response(
    #             {"message": f"Success! [Scan #{scan.id}]"},
    #             status=status.HTTP_201_CREATED,
    #         )
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["GET", "POST"])
    def from_dicom(self, request, series_id: int = None, subject_id: int = None):
        if request.method == "GET":
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
        elif request.method == "PUT":
            file_obj = request.data["file"]
            if file_obj.name.endswith(".dcm"):
                print("recognized dcm")
                dicom_image, created = ImportImage(file_obj).run()
                if created:
                    print("created image instance")
                    subject = Subject.objects.get(id=subject_id)
                    scan, created = Scan.objects.get_or_create(
                        dicom=dicom_image.series, subject=subject
                    )
                    if created:
                        print("created scan instance")
                        scan.update_fields_from_dicom()
                        scan.save()
                        serializer = ScanSerializer(scan, context={"request": request})
                        print('updated scan instance')
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_204_NO_CONTENT)


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
