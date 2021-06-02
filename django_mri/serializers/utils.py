from django_mri.utils.utils import (
    get_measurement_model,
    get_subject_model,
    get_laboratory_model,
)
from rest_framework import serializers

Laboratory = get_laboratory_model()
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


class MiniLaboratorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified serializer class for the :class:`Laboratory` model.
    """

    class Meta:
        model = Laboratory
        fields = "id", "title", "description"
