"""
Definition of the :class:`~django_mri.serializers.scan.ScanSerializer` class.
"""

from django_dicom.models import Series
from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from django_mri.serializers.sequence_type import SequenceTypeSerializer
from django_mri.utils.utils import get_subject_model, get_group_model
from rest_framework import serializers


class ScanSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~accounts.models.user.User` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    url = serializers.HyperlinkedIdentityField(view_name="mri:scan-detail")
    dicom = serializers.HyperlinkedRelatedField(
        view_name="dicom:series-detail", queryset=Series.objects.all()
    )
    subject = serializers.HyperlinkedRelatedField(
        view_name="research:subject-detail",
        queryset=get_subject_model().objects.all(),
        required=False,
    )
    nifti = serializers.HyperlinkedRelatedField(
        source="_nifti",
        view_name="mri:nifti-detail",
        queryset=NIfTI.objects.all(),
        required=False,
        allow_null=True,
    )
    study_groups = serializers.HyperlinkedRelatedField(
        view_name="research:group-detail",
        queryset=get_group_model().objects.all(),
        many=True,
        required=False,
    )
    sequence_type = SequenceTypeSerializer(
        source="infer_sequence_type_from_dicom", read_only=True
    )

    class Meta:
        model = Scan
        fields = (
            "id",
            "url",
            "dicom",
            "subject",
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
