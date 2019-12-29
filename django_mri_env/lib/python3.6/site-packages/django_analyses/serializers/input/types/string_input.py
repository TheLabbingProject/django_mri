from django_analyses.models.input.types.string_input import StringInput
from rest_framework import serializers


class StringInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringInput
        fields = "id", "key", "value", "run", "definition"
