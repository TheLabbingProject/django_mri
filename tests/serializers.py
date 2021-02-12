from rest_framework import serializers

from .models import Subject


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    `HyperlinkedModelSerializer <https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer>`_
    for the :class:`~tests.models.Subject` model.

    """

    class Meta:
        model = Subject
        fields = ("id", "title", "description")
