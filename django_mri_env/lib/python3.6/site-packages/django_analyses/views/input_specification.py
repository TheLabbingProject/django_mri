from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.serializers.input.input_specification import (
    InputSpecificationSerializer,
)
from rest_framework import viewsets


class InputSpecificationViewSet(viewsets.ModelViewSet):
    queryset = InputSpecification.objects.order_by("-id").all()
    serializer_class = InputSpecificationSerializer

