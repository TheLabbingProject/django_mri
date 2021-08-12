from django_mri.utils.utils import (
    get_group_model,
    get_measurement_model,
    get_subject_model,
)
from rest_framework import serializers

Group = get_group_model()
Measurement = get_measurement_model()
Subject = get_subject_model()


class MiniGroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified serializer class for the :class:`Group` model.
    """

    study_title = serializers.CharField(source="study.title")

    class Meta:
        model = Group
        fields = "id", "study_title", "title"


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
