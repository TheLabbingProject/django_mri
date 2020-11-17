from django_mri.utils.utils import get_subject_model, get_measurement_model
from rest_framework import serializers


Measurement = get_measurement_model()
Subject = get_subject_model()


class MiniSubjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified serializer class for the :class:`Subject` model.
    """

    class Meta:
        model = Subject
        fields = "id", "id_number", "first_name", "last_name"


class MiniMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified serializer class for the :class:`Measurement` model.
    """

    class Meta:
        model = Measurement
        fields = "id", "title", "description"
