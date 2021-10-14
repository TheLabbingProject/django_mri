"""
Definition of the :class:`SessionReadSerializer` and `SessionWriteSerializer`
classes.
"""
from typing import Tuple

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

SESSION_SERIALIZER_FIELDS: Tuple[str] = (
    "id",
    "subject",
    "comments",
    "time",
    "measurement",
    "irb",
)
SESSION_READ_FIELDS: Tuple[str] = (
    "dicom_zip",
    "nifti_zip",
    "n_scans",
    "study_groups",
)
SESSION_WRITE_FIELDS: Tuple[str] = (
    "subject_id",
    "measurement_id",
    "irb_id",
)


class SessionSerializer(serializers.ModelSerializer):
    measurement = MiniMeasurementSerializer()
    subject = serializers.PrimaryKeyRelatedField(read_only=True)
    irb = IrbApprovalSerializer()

    class Meta:
        model = Session
        fields = SESSION_SERIALIZER_FIELDS


class SessionReadSerializer(SessionSerializer):
    """
    Serializer class for the :class:`~django_mri.models.session.Session` model.
    """

    dicom_zip = serializers.SerializerMethodField()
    nifti_zip = serializers.SerializerMethodField()
    n_scans = serializers.SerializerMethodField()
    study_groups = MiniGroupSerializer(many=True)

    class Meta:
        model = Session
        fields = tuple(
            list(SESSION_SERIALIZER_FIELDS) + list(SESSION_READ_FIELDS)
        )

    def get_dicom_zip(self, instance: Session) -> str:
        return reverse("mri:session_dicom_zip", args=(instance.id,))

    def get_nifti_zip(self, instance: Session) -> str:
        return reverse("mri:session_nifti_zip", args=(instance.id,))

    def get_n_scans(self, instance: Session) -> int:
        return instance.scan_set.count()


class AdminSessionReadSerializer(SessionReadSerializer):
    subject = MiniSubjectSerializer()


class SessionWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class for the :class:`~django_mri.models.session.Session` model.
    """

    measurement_id = serializers.PrimaryKeyRelatedField(
        queryset=Measurement.objects.all(), allow_null=True
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all()
    )
    irb_id = serializers.PrimaryKeyRelatedField(
        queryset=IrbApproval.objects.all(), allow_null=True
    )

    class Meta:
        model = Session
        fields = tuple(
            list(SESSION_SERIALIZER_FIELDS) + list(SESSION_WRITE_FIELDS)
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
