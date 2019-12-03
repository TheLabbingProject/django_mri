import os

from django.db.models.query import QuerySet
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_dicom.models import Series
from django_mri.data_import import ImportScan, LocalImport
from django_mri.filters.scan_filter import ScanFilter
from django_mri.models import Scan
from django_mri.serializers import ScanSerializer
from django_mri.utils import get_subject_model
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ScanViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
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

    def get_queryset(self) -> QuerySet:
        """
        Filter the returned scans according to the studies the requesting
        user is a collaborator in, unless the user is staff, in which case
        return all scans.

        Returns
        -------
        QuerySet
            Scan instances.
        """

        user = get_user_model().objects.get(username=self.request.user)
        if user.is_staff:
            return Scan.objects.all()
        return Scan.objects.filter(study_groups__study__collaborators=user)

    @action(detail=False, methods=["POST"])
    def from_file(self, request):
        """
        Creates a new scan instance from a file (currently only DICOM format files are accepted).

        Parameters
        ----------
        request :
            A request from the client.

        Returns
        -------
        Response
            A response containing the serialized data or a message.
        """
        file_obj = request.data["file"]
        subject = get_subject_model().objects.get(id=request.data["subject_id"])
        user = get_user_model().objects.get(username=self.request.user)

        if file_obj.name.endswith(".dcm"):
            scan, created = ImportScan(
                subject, file_obj, scan_type="dcm", user=user
            ).run()
            serializer = ScanSerializer(scan, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif file_obj.name.endswith(".zip"):
            content = ContentFile(file_obj.read())
            temp_file_name = default_storage.save("tmp.zip", content)
            temp_file_path = os.path.join(settings.MEDIA_ROOT, temp_file_name)
            LocalImport(subject, temp_file_path, user=user).run()
            os.remove(temp_file_path)
            return Response(
                {"message": "Successfully imported ZIP archive!"},
                status=status.HTTP_201_CREATED,
            )

    @action(detail=True, methods=["GET"])
    def from_dicom(self, request, series_id: int = None):
        """
        Returns scan information from a :class:`~django_dicom.models.series.Series` instance
        without serializing.

        Parameters
        ----------
        request :
            A request from the client.
        series_id : int, optional
            :class:`~django_dicom.models.series.Series` primary key, by default None

        Returns
        -------
        Response
            Serialized data or messagerequirements
        """
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
