"""
Definition of the :class:`SessionSerializer` class.
"""
from django_mri.models.session import Session
from django_mri.serializers.utils import MiniSubjectSerializer
from rest_framework import serializers


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
