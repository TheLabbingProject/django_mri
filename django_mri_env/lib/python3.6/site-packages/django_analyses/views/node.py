from django_analyses.filters.pipeline.node import NodeFilter
from django_analyses.models.pipeline.node import Node
from django_analyses.serializers.pipeline.node import NodeSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class NodeViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = NodeFilter
    pagination_class = StandardResultsSetPagination
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
