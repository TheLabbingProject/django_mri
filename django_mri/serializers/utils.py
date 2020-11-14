from django_mri.utils.utils import get_subject_model
from rest_framework import serializers


Subject = get_subject_model()


class MiniSubjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    Minified serializer class for the :class:`Subject` model.
    """

    class Meta:
        model = Subject
        fields = "id", "id_number", "first_name", "last_name"
