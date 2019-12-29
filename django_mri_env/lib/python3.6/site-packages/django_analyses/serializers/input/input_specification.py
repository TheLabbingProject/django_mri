from django_analyses.models.analysis import Analysis
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.serializers.input.definitions.input_definition import (
    InputDefinitionSerializer,
)
from rest_framework import serializers


class InputSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="analysis:inputspecification-detail"
    )
    analysis = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysis-detail", queryset=Analysis.objects.all()
    )
    input_definitions = InputDefinitionSerializer(many=True)

    class Meta:
        model = InputSpecification
        fields = (
            "id",
            "analysis",
            "input_definitions",
            "created",
            "modified",
            "url",
        )

