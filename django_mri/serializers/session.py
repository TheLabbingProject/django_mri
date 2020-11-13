"""
Definition of the :class:`SessionSerializer` class.
"""
from django_mri.models.session import Session
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


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~django_mri.models.session.Session` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    subject = MiniSubjectSerializer()

    class Meta:
        model = Session
        fields = "id", "subject", "comments", "time"
