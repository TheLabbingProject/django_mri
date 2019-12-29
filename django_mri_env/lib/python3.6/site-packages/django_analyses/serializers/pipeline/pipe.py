from django_analyses.models.pipeline.node import Node
from django_analyses.models.pipeline.pipe import Pipe
from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.serializers.input.definitions.input_definition import (
    InputDefinitionSerializer,
)
from django_analyses.serializers.output.definitions.output_definition import (
    OutputDefinitionSerializer,
)
from rest_framework import serializers


class PipeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:pipe-detail")
    pipeline = serializers.HyperlinkedRelatedField(
        view_name="analysis:pipeline-detail", queryset=Pipeline.objects.all(),
    )
    source = serializers.HyperlinkedRelatedField(
        view_name="analysis:node-detail", queryset=Node.objects.all()
    )
    source_port = OutputDefinitionSerializer()
    destination = serializers.HyperlinkedRelatedField(
        view_name="analysis:node-detail", queryset=Node.objects.all()
    )
    destination_port = InputDefinitionSerializer()

    class Meta:
        model = Pipe
        fields = (
            "id",
            "pipeline",
            "source",
            "source_port",
            "destination",
            "destination_port",
            "url",
        )

