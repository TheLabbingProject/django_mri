"""
Definition of the :class:`ScanSerializer` class.
"""
from django_dicom.models import Series
from rest_framework import serializers

from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from django_mri.models.session import Session
from django_mri.serializers.utils import MiniSubjectSerializer
from django_mri.utils.utils import get_group_model

Group = get_group_model()


class ScanSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~django_mri.models.scan.Scan` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    dicom = serializers.PrimaryKeyRelatedField(
        queryset=Series.objects.all(), allow_null=True
    )
    session = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all(), allow_null=False,
    )
    nifti = serializers.PrimaryKeyRelatedField(
        source="_nifti",
        queryset=NIfTI.objects.all(),
        required=False,
        allow_null=True,
    )
    study_groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), many=True, allow_null=True,
    )
    sequence_type = serializers.CharField(read_only=True)
    subject = MiniSubjectSerializer(source="session.subject")

    class Meta:
        model = Scan
        fields = (
            "id",
            "dicom",
            "session",
            "nifti",
            "study_groups",
            "institution_name",
            "time",
            "description",
            "number",
            "echo_time",
            "repetition_time",
            "inversion_time",
            "spatial_resolution",
            "comments",
            "sequence_type",
            "subject",
        )

    def create(self, data: dict):
        """
        Gets or creates an instance of the
        :class:`~django_mri.models.scan.Scan` model based on the provided data.

        Parameters
        ----------
        data : dict
            Instance data

        Returns
        -------
        ~django_mri.models.scan.Scan
            Matching scan
        """

        scan, created = Scan.objects.get_or_create(**data)
        if created and scan.dicom and len(data) == 1:
            scan.update_fields_from_dicom()
            scan.save()
        return scan
