from django_analyses.filters.category import CategoryFilter
from django_analyses.models.category import Category
from django_analyses.serializers.category import CategorySerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class CategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = CategoryFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
