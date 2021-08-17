"""
Definition of the :class:`SessionReadSerializer` class.
"""
from django.urls import reverse
from django_mri.models.irb_approval import IrbApproval
from django_mri.models.session import Session
from django_mri.serializers.irb_approval import IrbApprovalSerializer
from django_mri.serializers.utils import (
    MiniGroupSerializer,
    MiniMeasurementSerializer,
    MiniSubjectSerializer,
)
from django_mri.utils import get_measurement_model, get_subject_model
from rest_framework import serializers

Measurement = get_measurement_model()
Subject = get_subject_model()


class SessionReadSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~django_mri.models.session.Session` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    study_groups = MiniGroupSerializer(many=True)
    measurement = MiniMeasurementSerializer()
    subject = MiniSubjectSerializer()
    irb = IrbApprovalSerializer()
    dicom_zip = serializers.SerializerMethodField()
    nifti_zip = serializers.SerializerMethodField()
    n_scans = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = (
            "id",
            "subject",
            "comments",
            "time",
            "measurement",
            "irb",
            "dicom_zip",
            "nifti_zip",
            "n_scans",
            "study_groups",
        )

    def get_dicom_zip(self, instance: Session) -> str:
        return reverse("mri:session_dicom_zip", args=(instance.id,))

    def get_nifti_zip(self, instance: Session) -> str:
        return reverse("mri:session_nifti_zip", args=(instance.id,))

    def get_n_scans(self, instance: Session) -> int:
        return instance.scan_set.count()


class SessionWriteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~django_mri.models.session.Session` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    measurement = MiniMeasurementSerializer()
    measurement_id = serializers.PrimaryKeyRelatedField(
        queryset=Measurement.objects.all(), allow_null=True
    )
    subject = MiniSubjectSerializer()
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all()
    )
    irb = IrbApprovalSerializer()
    irb_id = serializers.PrimaryKeyRelatedField(
        queryset=IrbApproval.objects.all(), allow_null=True
    )
    dicom_zip = serializers.SerializerMethodField()
    nifti_zip = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = (
            "id",
            "subject",
            "subject_id",
            "comments",
            "time",
            "measurement",
            "measurement_id",
            "irb",
            "irb_id",
            "dicom_zip",
            "nifti_zip",
        )

    def update(self, instance, validated_data):
        if validated_data.get("irb"):
            irb = validated_data.pop("irb")
            irb_approval, _ = IrbApproval.objects.get_or_create(
                institution=irb["institution"], number=irb["number"]
            )
            validated_data["irb_id"] = irb_approval.id
        super().update(instance, validated_data)
        return instance

    def get_dicom_zip(self, instance: Session) -> str:
        return reverse("mri:session_dicom_zip", args=(instance.id,))

    def get_nifti_zip(self, instance: Session) -> str:
        return reverse("mri:session_nifti_zip", args=(instance.id,))
