from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.serializers.analysis_version import AnalysisVersionSerializer
from rest_framework import viewsets


class AnalysisVersionViewSet(viewsets.ModelViewSet):
    queryset = AnalysisVersion.objects.order_by("title").all()
    serializer_class = AnalysisVersionSerializer

