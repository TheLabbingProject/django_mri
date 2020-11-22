"""
Definition of the :class:`SessionReadSerializer` class.
"""
from django_mri.models.session import Session
from django_mri.serializers.utils import (
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

    measurement = MiniMeasurementSerializer()
    subject = MiniSubjectSerializer()

    class Meta:
        model = Session
        fields = "id", "subject", "comments", "time", "measurement"


class SessionWriteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~django_mri.models.session.Session` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    measurement = serializers.PrimaryKeyRelatedField(
        queryset=Measurement.objects.all()
    )
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all()
    )

    class Meta:
        model = Session
        fields = "id", "subject", "comments", "time", "measurement"
