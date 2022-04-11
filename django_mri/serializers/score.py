"""
Definition of the :class:`ScoreSerializer` class.
"""
from django_mri.models.score import Score
from rest_framework import serializers


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ("id", "origin", "region", "metric", "run")
        depth = 1
