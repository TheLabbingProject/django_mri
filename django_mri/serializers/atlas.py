"""
Definition of the :class:`AtlasSerializer` class.
"""
from django_mri.models.atlas import Atlas
from rest_framework import serializers


class AtlasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atlas
        fields = (
            "id",
            "title",
            "description",
            "symmetric",
        )
