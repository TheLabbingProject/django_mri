"""
Definition of the :class:`MetricSerializer` class.
"""
from django_mri.models.metric import Metric
from rest_framework import serializers


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = (
            "id",
            "title",
            "description",
        )
