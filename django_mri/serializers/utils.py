from django_mri.utils.utils import (
    get_group_model,
    get_measurement_model,
    get_study_model,
    get_subject_model,
)
from rest_framework import serializers

Group = get_group_model()
Measurement = get_measurement_model()
Subject = get_subject_model()
Study = get_study_model()


class MiniStudySerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified serializer class for the :class:`Study` model.
    """

    class Meta:
        model = Study
        fields = "id", "title", "description"


class MiniGroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified serializer class for the :class:`Group` model.
    """

    study = MiniStudySerializer()

    class Meta:
        model = Group
        fields = "id", "title", "study"


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

    associated_studies = MiniStudySerializer(
        source="query_associated_studies", many=True,
    )

    class Meta:
        model = Measurement
        fields = "id", "title", "description", "associated_studies"
