"""
Definition of the :class:`RegionSerializer` class.
"""
from django_mri.models.region import Region
from rest_framework import serializers


class RegionSerializer(serializers.ModelSerializer):
    atlas = serializers.CharField(source="atlas.title", read_only=True)

    class Meta:
        model = Region
        fields = (
            "id",
            "atlas",
            "hemisphere",
            "index",
            "title",
            "description",
            "subcortical",
        )
