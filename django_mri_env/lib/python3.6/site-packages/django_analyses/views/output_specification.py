from django_analyses.models.output.output_specification import OutputSpecification
from django_analyses.serializers.output.output_specification import (
    OutputSpecificationSerializer,
)
from rest_framework import viewsets


class OutputSpecificationViewSet(viewsets.ModelViewSet):
    queryset = OutputSpecification.objects.order_by("-id").all()
    serializer_class = OutputSpecificationSerializer

