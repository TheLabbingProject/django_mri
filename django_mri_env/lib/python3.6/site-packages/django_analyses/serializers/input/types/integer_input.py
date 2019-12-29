from django_analyses.models.input.types.integer_input import IntegerInput
from rest_framework import serializers


class IntegerInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegerInput
        fields = "id", "key", "value", "run", "definition"
