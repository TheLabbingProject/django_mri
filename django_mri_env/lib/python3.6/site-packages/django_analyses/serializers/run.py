from django.contrib.auth import get_user_model
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.run import Run
from django_analyses.serializers.input.input import InputSerializer
from django_analyses.serializers.output.output import OutputSerializer
from rest_framework import serializers


User = get_user_model()


class RunSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:run-detail")
    user = serializers.HyperlinkedRelatedField(
        view_name="accounts:user-detail", queryset=User.objects.all()
    )
    analysis_version = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysisversion-detail",
        queryset=AnalysisVersion.objects.all(),
    )
    input_set = InputSerializer(many=True)
    output_set = OutputSerializer(many=True)

    class Meta:
        model = Run
        fields = (
            "id",
            "user",
            "analysis_version",
            "input_set",
            "output_set",
            "created",
            "modified",
            "url",
        )

