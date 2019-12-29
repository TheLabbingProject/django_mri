from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.serializers.pipeline.node import NodeSerializer
from django_analyses.serializers.pipeline.pipe import PipeSerializer
from rest_framework import serializers


class PipelineSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:pipe-detail")
    node_set = NodeSerializer(many=True)
    pipe_set = PipeSerializer(many=True)

    class Meta:
        model = Pipeline
        fields = (
            "id",
            "title",
            "description",
            "node_set",
            "pipe_set",
            "created",
            "modified",
            "url",
        )

